import socket 
import threading 
import sys 
import time


host_ip = '200.235.131.66' #ip Servidor
host_port = 10000


expectedPeerName=""
expectedPeerPort=""

def print_help():
    print("/list para listar peers online")
    print("/chat para comunicar com outro peer")
    print("/help para lista de comandos")
    print("/info para informacoes de conexão")
    print("\n")

def extract_name(initial_msg):
    # Remove o prefixo 'USER ' e o sufixo '\r\n' (se houver) da mensagem inicial
    if initial_msg.startswith("USER "):
        # Remove o prefixo 'USER '
        myname = initial_msg[5:]
        
        # Remove o sufixo '\r\n' se ele existir
        if myname.endswith("\r\n"):
            myname = myname[:-2]
            
        return myname
    else:
        raise ValueError("Formato de mensagem inválido")
    


def handlePeerConnection(myServerSocket):
    try:
            conn, addr = myServerSocket.accept()
            #print(addr.decode())
            print(f"Conexão estabelecida com peer de porta {addr[1]}")
            
            peerName=extract_name(conn.recv(1024).decode()) #Primeira mensagem que recebe é o nome do usuário que fará a conexão
           
            #peerName=extrair_nome(peerName_obj.decode()) #extrai o peer name da mensagem inicial USER <nome>
            peerPort=addr[1]
            print("\nConexão estabelecida com <{}>\n".format(peerName))
            while True:
                try:
                    responseMsg = conn.recv(1024) #As próximas mensagens chegarão aqui
                    if responseMsg.decode() == "DISC":
                        print("{} saiu do chat :(".format(peerName))   
                        break               
                    #print(f"ExpectedPeerName: {expectedPeerName} and ReceivedPeerName:{peerName}")
                    #print(f"ExpectedPeerPort: {expectedPeerPort} and ReceivedPeerPort:{peerPort}")
                    if(expectedPeerName==""):
                        print("<{}>:".format(peerName), responseMsg.decode())
                    elif(expectedPeerName==peerName):
                        print("<{}>:".format(peerName), responseMsg.decode())
                    #else nao printa, mas recebe.
                except:
                    print("Erro de conexao")
                    break
    except socket.error as e:
        print(f"(handlePeerConnection)Erro de conexao com peer {e}")
    # except:
    #     print("Conexão encerrada")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def keep(serverSocket):
    while True:
        try:
           serverSocket.send(str.encode("KEEP\r\n"))
        
        except:
            print("Falha ao mandar Keep para o servidor")
        
        time.sleep(5)
    

def main():
    #print_help()
  
    try:
        # Cria o socket que funciona como servidor próprio, serve para conexao com peer
        myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_ip = 'localhost' #para teste local
        myServerSocket.bind((my_ip, 0)) #teste ip e porta atribuido automaticamente   
        #myServerSocket.bind(('', 0)) #Descomentar para teste com conexão externa    
        tendereco, tporta = myServerSocket.getsockname()  
    except OSError as err:
        print(f"Erro ao vincular o socket: {err}")
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    finally:
        myServerSocket.listen(2)
        print("Tentando conexao com o servidor central....")

    try:
    # Cria o socket TCP/IP
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta ao servidor/ conecta ao socket do Servidor  
        global host
        global porta
        serverSocket.connect((host_ip, host_port))
    
        print("Conectado ao servidor com sucesso\n")
        print_help()
    except socket.error as err:
         print("Erro ao conectar com servidor\nExecute a aplicação novamente")
         sys.exit()
    finally:
        msg="USER grilo:"+str(tporta)
        myname="grilo"
        msg=msg+"\r\n"
        
        
        
    sentBytes=serverSocket.send(msg.encode())
    if(sentBytes==-1):
        print("Erro ao enviar mensagem")

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
                    #peerSocket.connect((ip, port)) # Descomentar para teste com conexão externa    
                    peerSocket.connect(('localhost',port)) # se conecta a um peer na mesma maquina (mesmo ip)
                    
                    peerSocket.send(("USER "+myname).encode()) # send USER <nome>
                    
            except socket.error as err:
                print(f"Erro ao conectar ao peer: {err}")
                continue
            except:
                print("Erro ao enviar mensagem ao peer")
            finally:
                    while True:
                        inputMsg=input(f"Escreva sua mensagem a(o) {expectedPeerName} ou digite /bye para voltar ao menu\n")
                        if(inputMsg=="/bye"):
                            try:
                                peerSocket.send(("DISC").encode())
                            except:
                                print("Erro ao encerrar conexao")
                            finally:
                                
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

    



