import socket 
import threading 
import sys 
import time


host = '200.235.131.66' #ip Servidor
porta = 10000


expectedPeerName=""
expectedPeerPort=""

def print_help():
    print("/list para listar peers online")
    print("/chat para comunicar com outro peer")
    print("/help para lista de comandos")
    print("/info para informacoes de conexão")
    print("\n")



def handlePeerConnection(myServerSocket):
    try:
            conn, addr = myServerSocket.accept()
            #print(addr.decode())
            
            print(f"Conexão estabelecida com peer de porta {addr[1]}")
            peerName = conn.recv(1024) #Primeira mensagem que recebe é o nome do usuário que fará a conexão

            peerPort=addr[1]
            print("\nConexão estabelecida com <{}>\n".format(peerName.decode()))
            while True:
                try:
                    responseMsg = conn.recv(1024) #As próximas mensagens chegarão aqui
                    if responseMsg.decode() == "DISC":
                        print("{} saiu do chat :(".format(peerName.decode()))   
                        break               
                    print(f"ExpectedPeerName: {expectedPeerName} and ReceivedPeerName:{peerName.decode()}")
                    print(f"ExpectedPeerPort: {expectedPeerPort} and ReceivedPeerPort:{peerPort}")
                    if(expectedPeerName==""):
                        print("<{}>:".format(peerName.decode()), responseMsg.decode())
                    elif(expectedPeerName==peerName.decode()):
                        print("<{}>:".format(peerName.decode()), responseMsg.decode())
                    #else nao printa, mas recebe.
                except:
                    print("Erro de conexao")
                    break
    except socket.error as e:
        print(f"(handlePeerConnection)Erro de conexao com peer {e}")
    except:
        print("Conexão encerrada")

def keep(serverSocket):
    while True:
        try:
            sentBytes=serverSocket.send(str.encode("KEEP\r\n"))
        
        except:
            print("Falha ao mandar Keep para o servidor")
        
        time.sleep(10)
    

def main():
    #print_help()
  
    try:
        # Cria o socket que funciona como servidor próprio, serve para conexao com peer
        myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Especifica o endereço e a porta desejados
        endereco = 'localhost'
        #porta = 20000
        # Tenta vincular o socket ao endereço e porta especificados
        
        myServerSocket.bind((endereco, 0)) #teste ip e porta atribuido automaticamente
        
        tendereco, tporta = myServerSocket.getsockname()
        
        #print(f"Minha porta:{tporta}")


    except OSError as err:
        print(f"Erro ao vincular o socket: {err}")
        # Trate o erro de bind específico aqui

    except ValueError as ve:
        print(f"Erro de valor: {ve}")
        # erro relacionado à porta fora do intervalo válido

    finally:
        #print("myServerSocket is listening")
        myServerSocket.listen(2)
        print("Tentando conexao com o servidor central....")

    try:
    # Cria o socket TCP/IP
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta ao servidor/ conecta ao socket do Servidor  
        global host
        global porta
        serverSocket.connect((host, porta))
    
        print("Conectado ao servidor com sucesso\n")
        print_help()
    except socket.error as err:
        #print(f"Erro ao conectar ao servidor: {err}")
        # Trate o erro aqui, como fechar o socket se necessário
         print("Erro ao conectar com servidor\nExecute a aplicação novamente")
         sys.exit()
    finally:
        ##msg=input("Digite a mensagem inicial\n")
        msg="USER grilo:"+str(tporta)
        myname="grilo"
        msg=msg+"\r\n"
        
        
        
    sentBytes=serverSocket.send(msg.encode())
    if(sentBytes==-1):
        print("Erro ao enviar mensagem")

    #serverSocket.send(str.encode("LIST\r\n"))
    #responseMsg = serverSocket.recv(1024)

    #if responseMsg:
     #   print("Mensagem Recebida com sucesso")
        #print(responseMsg.decode())
    keepAlive_Thread = threading.Thread(target=keep, args=(serverSocket,)) 
    keepAlive_Thread.daemon = True
    keepAlive_Thread.start() 

    while True:
        listening_thread = threading.Thread(target=handlePeerConnection, args=(myServerSocket,)) 
        listening_thread.daemon = True  # Torna o thread daemon para que ele termine quando o programa principal terminar   
        listening_thread.start() #Start do recebimento  

        

      
        inputMsg=input("({})Digite o comando \n".format(myname))
        if(inputMsg=="/help"):
            print_help()

        if(inputMsg=="/info"):
            print("Meu ip:",tendereco)
            print("Minha porta:",tporta)
            
        
        if(inputMsg=="/list"):
            try:
                sentBytes=serverSocket.send(("LIST"+"\r\n").encode())
            except:            
                print("Erro ao enviar mensagem, desconectado do servidor")
            finally:
                try:
                    responseMsg = serverSocket.recv(1024)
                except:
                    print("Erro de conexao, desconectado pelo servidor")
                finally:
                    print(responseMsg.decode())

        if(inputMsg=="/exit"):
            
            sys.exit("Tchau!")
        
        if(inputMsg=="/chat"):
            inputMsg=input("Com quem você quer se conectar?")
            if(inputMsg==""):
                continue
            global expectedPeerName
            expectedPeerName=inputMsg
            print(f"Voce deseja-se comunicar com {expectedPeerName}")
            
            try:
                sentBytes=serverSocket.send(("ADDR " +inputMsg+"\r\n").encode())
            except:
                print("Erro ao enviar mensagem ao servidor\nDesconectado do servidor")
            
            try:
                responseMsg = serverSocket.recv(1024)
            except:
                 print("Erro ao receber mensagem do servidor\nDesconectado do servidor")
            finally:
                ipv4string=responseMsg.decode().replace("ADDR","").replace(" ","")
                #print(ipv4string)
                ip, port = ipv4string.split(':')
                global expectedPeerPort
                expectedPeerPort=port
                port=int(port)
                print(ip)
                print(port)
            try:
                    peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                    #peerSocket.connect((ip, port))
                    peerSocket.connect(('localhost',port))
                    peerSocket.send((myname).encode())
                    
            except socket.error as err:
                print(f"Erro ao conectar ao peer: {err}")
                continue
            finally:
                    while True:
                        inputMsg=input(f"Escreva sua mensagem a(o) {expectedPeerName} ou digite /bye para voltar ao menu\n")
                        if(inputMsg=="/bye"):
                            peerSocket.send(("DISC").encode())
                            expectedPeerName=""
                            peerSocket.close()
                            break
                        
                       
                        try:
                            sentBytes=peerSocket.send(inputMsg.encode())
                            if(sentBytes==-1):
                                print("Erro ao enviar mensagem")

                        except socket.error as e:
                            print(f"Erro de conexao com peer\n{e}")
                            peerSocket.close()
                            break
                        
                        #finally:
                         #   continue
       

if __name__ == "__main__":
    main()
    #sys.exit(0)

    



