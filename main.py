#NOME: Guilherme Nunes Lopes 105462
#Nome: Cicero Cipriano Maciel 102021

import socket 
import threading 
import sys 
import time
import select

host_ip = '200.235.131.66'
host_port = 10000






def print_help():
    print("/list para listar peers online")
    print("/chat para comunicar com outro peer")
    print("/help para lista de comandos")
    print("/info para informacoes de conexão")
    print("Aperte enter para realizar uma ação apos receber mensagem")
    print("\n")

def extract_name(msg):
    if msg.startswith("USER "):
        myname = msg[5:]
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
                        names.pop(s,None)
                        sockets_to_monitor.remove(s)
                    else:
                        print(names[s] + ": " + msg)



def keep(serverSocket):
    while True:
        try:
           serverSocket.send(str.encode("KEEP\r\n"))
        except:
            print("Falha ao mandar Keep para o servidor")
        finally:
            time.sleep(5)    


def handleChat(serverSocket,myName,myAddr,myPort):
    while True:
        inputMsg=input("({})Digite o comando \n".format(myName))
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
            else:
                try:
                    responseMsg = serverSocket.recv(1024)
                except:
                    print("Erro de conexao, desconectado pelo servidor")
                else:
                    print(responseMsg.decode())
        
        if(inputMsg=="/exit"):
            sys.exit("Tchau!")
        
        if(inputMsg=="/chat"):
            inputMsg=input("Com quem você quer se conectar? Caso não queira se conectar com ninguém, aperte enter para voltar ao estado inicial")
            if(inputMsg==""):
                continue
            expectedPeerName=inputMsg
            print(f"Voce deseja-se comunicar com {expectedPeerName}")
            try:
                sentBytes=serverSocket.send(("ADDR " +inputMsg+"\r\n").encode())
            except:
                print("Erro ao enviar mensagem ao servidor\nDesconectado do servidor")
            else:
                try:
                    responseMsg = serverSocket.recv(1024)
                except:
                    print("Erro ao receber mensagem do servidor\nDesconectado do servidor")
                else:
                    ipv4string=responseMsg.decode().replace("ADDR","").replace(" ","")
                    ip, port = ipv4string.split(':')
                    port=int(port)
            try:
                peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                #peerSocket.connect((ip, port)) 
                peerSocket.connect(('localhost',port)) # se conecta a um peer na mesma maquina (mesmo ip)
                peerSocket.send(("USER "+myName).encode()) # send USER <nome>
            except socket.error as err:
                print(f"Erro ao conectar ao peer: {err}")
                continue
            except:
                print("Erro ao enviar mensagem ao peer")
                continue
            else:
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



def main():
    myName = input("Digite seu nome:")
    my_ip = 'localhost' #para teste local
    
    #Criando o servidor local
    try:
        myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Erro ao criar o socket\nExecute a aplicação novamente")
        sys.exit()
    else:
        try:
            myServerSocket.bind((my_ip, 0)) #para teste local  
            #myServerSocket.bind(('', 0)) #Descomentar para teste com conexão externa     
        except OSError as err:
            print("Erro ao fazer o bind\nExecute a aplicação novamente")
            sys.exit()
        else:
            myAddr, myPort = myServerSocket.getsockname()  
     
    myServerSocket.listen()

    #Conecta ao servidor do professor     
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Tentando conexao com o servidor central....")
        print("Conectado ao servidor com sucesso\n")
        print_help()
    except socket.error as err:
         print("Erro ao conectar com servidor\nExecute a aplicação novamente")
         sys.exit()
    else:
        try:
            serverSocket.connect((host_ip, host_port))
        except socket.error as err:  
            print("Erro ao conectar com servidor\nExecute a aplicação novamente")
            sys.exit()
        else:
            msg = "USER " + myName + ":" + str(myPort) + "\r\n"  
            sentBytes=serverSocket.send(msg.encode())
            if(sentBytes==-1):
                print("Erro ao enviar mensagem")
                sys.exit()

    keepAlive_Thread = threading.Thread(target=keep, args=(serverSocket,)) 
    keepAlive_Thread.daemon = True
    keepAlive_Thread.start() 

    listening_thread = threading.Thread(target=handlePeerConnection, args=(myServerSocket,)) 
    listening_thread.daemon = True 
    listening_thread.start() 

    handleChat(serverSocket,myName,myAddr,myPort)

    
if __name__ == "__main__":
    main()
    #sys.exit(0)