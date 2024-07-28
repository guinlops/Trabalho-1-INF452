#NOME: Guilherme Nunes Lopes 105462
#Nome: Cicero Cipriano Maciel 102021

import socket 
import threading 
import sys 
import time
import select

#socket.setdefaulttimeout(1.0)
host_ip = '200.235.131.66'
host_port = 10000

expectedPeerName=""
expectedPeerPort=""

def print_help():
    print("/list para listar peers online")
    print("/chat para comunicar com outro peer")
    print("/help para lista de comandos")
    print("/info para informacoes de conexão")
    print("Aperte enter para realizar uma açao apos receber mensagem")
    print("\n")

def extract_name(msg):
    if initial_msg.startswith("USER "):
        myname = initial_msg[5:]
        if myname.endswith("\r\n"):
            myname = myname[:-2]
        return myname
    else:
        return ""

def handlePeerConnection(myServerSocket):
    sockets_to_monitor = [myServerSocket]
    names = {}
    while True:
        readable, writable, exceptional = select.select(sockets_to_monitor, [], [])
        for s in readable:
            if s is myServerSocket:
                conn, addr = s.accept()
                print(f"Conexão estabelecida com {addr}")
                sockets_to_monitor.append(conn)
                names[conn] = None
            else:
                data = s.recv(1024)
                if data:
                    msg = data.decode()
                    name = extract_name(msg)
                    if len(name) > 0:
                        names[s] = name
                        print("\nConexão estabelecida com " + name + "\n")
                    elif msg == "DISC":
                        print("Conexão fechada pelo peer " + names[s] + "\n")
                        s.close()
                        sockets_to_monitor.remove(s)
                    else:
                        print(names[s] + ": " + msg)

#def handlePeerConnection(myServerSocket):
    
    # peersList=[]
    
    # while True:
    #     auxPeersList=[]
    #     #print("Iteracao While True")
        
    #     for p in peersList:
    #         if(p[2]==True):
    #             auxPeersList.append(p)
    #     peersList=auxPeersList
    #     print(len(peersList))
        # try:
        #     conn, addr = myServerSocket.accept()   
        # except socket.timeout as e:
        #     print("Nenhuma conexão recebida nessa iteração")   
        # except socket.error as e:
        #     print(f"Erro de conexao com peer")
        # except Exception as e:
        #     print(f"Erro inesperado: {e}")
        # else:
            
        #     peerName=extract_name(conn.recv(1024).decode()) #Primeira mensagem que recebe é o nome do usuário que fará a conexão
        #     peersList.append((conn,peerName,True))
        #     print("\nConexão estabelecida com <{}>\n".format(peerName))
        # finally:
        #     for p in peersList:
        #         if(p[2]==True):
        #             #print("Peers Conectados:"+ p[1]+"\n")
        #             #print("Checando se "+p[1]+" enviou mensagem...")
        #             responseMsg=p[0].recv(1024).decode()
        #             if(responseMsg=="DISC"):
        #                 print("\nConexão encerrada com <{}>\n".format(p[1]))
        #                 p[0].close()
        #                 p[2]=False
        #             else:
        #                 print("<{}>:".format(p[1]), responseMsg.encode())
        #             # print(p[1]+ "nao enviou msg")

            #print("Print Saiu do For")

def keep(serverSocket):
    while True:
        try:
           serverSocket.send(str.encode("KEEP\r\n"))
        except:
            print("Falha ao mandar Keep para o servidor")
        finally:
            time.sleep(5)    

def main():
    nome = input("Digite seu nome:")
    
    try:
        # Cria o socket que funciona como servidor próprio para conexao com peer
        myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_ip = 'localhost' #para teste local
        myServerSocket.bind((my_ip, 0)) #para teste local  
        #myServerSocket.bind(('', 0)) #Descomentar para teste com conexão externa     
        myAddr, myPort = myServerSocket.getsockname()  
    except OSError as err:
        print(f"Erro ao vincular o socket: {err}")
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    else:
        myServerSocket.listen(2)
        
    try:
    # Cria o socket TCP/IP
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Tentando conexao com o servidor central....")
    # Conecta ao servidor/ conecta ao socket do Servidor  
        print("Conectado ao servidor com sucesso\n")
        print_help()
    except socket.error as err:
         print("Erro ao conectar com servidor\nExecute a aplicação novamente")
         sys.exit()
    else:
        serverSocket.connect((host_ip, host_port))
        msg = "USER " + nome + ":" + str(myPort) + "\r\n"
        msg="USER carneiro:"+str(myPort)
        myname="carneiro"
        msg=msg+"\r\n"
        
    sentBytes=serverSocket.send(msg.encode())   
    if(sentBytes==-1):
        print("Erro ao enviar mensagem")
        sys.exit()

    keepAlive_Thread = threading.Thread(target=keep, args=(serverSocket,)) 
    keepAlive_Thread.daemon = True
    keepAlive_Thread.start() 


    listening_thread = threading.Thread(target=handlePeerConnection, args=(myServerSocket,)) 
    listening_thread.daemon = True  # Torna o thread daemon para que ele termine quando o programa principal terminar   
    listening_thread.start() #Start do recebimento  

    while True:
    


        inputMsg=input("({})Digite o comando \n".format(myname))
        if(inputMsg=="/help"):
            print_help()

        if(inputMsg=="/info"):
            print("Meu ip:",myAddr)
            print("Minha porta:",myPort)
            
        
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
                            print(f"Erro de conexao com peer")
                            peerSocket.close()
                            break
if __name__ == "__main__":
    main()
    #sys.exit(0)

    



