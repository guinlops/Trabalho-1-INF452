#NOME: Guilherme Nunes Lopes 105462
#NOME: Cicero Cipriano Maciel 102021

import socket
import threading
import sys
import time
import select

host_ip = '200.235.131.66'
host_port = 10000

def print_help():
    print("******************** IMPORTANTE ********************")
    print("O terminal funciona como um chat, ele imprimira todas as mensagens recebidas.\nPorem, soh eh possivel enviar mensagens para uma pessoa por vez.\n")
    print("  v v v v v v v v v v v v v v v v v v v v v v v v v v v v v v")
    print("> Aperte enter para realizar uma ação apos receber mensagem  <")
    print("> Caso contrario, a interacao com sistema ficara bem confusa <")
    print("  ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^")
    print("********* Comandos *********")
    print("/help -> Abre essa descricao")
    print("/info -> exibe informacoes de conexão")
    print("/list -> listar peers online")
    print("/chat -> iniciar conversa com outro peer (apos rodar o comando, o nome do peer sera solicitado)")
    print("/exit -> termina o programa")
    print("******************** IMPORTANTE ********************")
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
                        print("\n" + name + " se conectou com voce, mensagens enviadas por ele serao impressas no terminal.\n")
                    elif msg == "DISC":
                        print("Conexão finalizada pelo peer " + names[s] + "\n")
                        s.close()
                        names.pop(s, None)
                        sockets_to_monitor.remove(s)
                    else:
                        print(names[s] + ": " + msg)

def keep(serverSocket):
    count = 0
    while True:
        if count == 4:
            serverSocket.shutdown(socket.SHUT_RDWR)
            print("Voce foi desconectado do servidor central\nExecute a aplicação novamente")
            sys.exit()
        try:
           serverSocket.send(str.encode("KEEP\r\n"))
        except:
            print("Falha ao mandar Keep para o servidor")
            count = count + 1
        else:
            count = 0
        finally:
            time.sleep(5)

def handleChat(serverSocket,myName,myAddr,myPort):
    while True:
        inputMsg = input(myName + ", digite o comando:\n")
        if inputMsg == "/help":
            print_help()
        if inputMsg == "/info":
            print("Meu ip:",myAddr)
            print("Minha porta:",myPort)
        if inputMsg == "/list":
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
        if inputMsg == "/exit":
            sys.exit("Tchau!")
        if inputMsg == "/chat":
            inputMsg = input("Com quem você quer conversar?\nCaso não queira conversar com alguém, aperte enter para voltar ao estado inicial\n")
            if inputMsg == "":
                continue
            expectedPeerName = inputMsg
            print(f"Voce deseja conversar com {expectedPeerName}")
            try:
                sentBytes = serverSocket.send(("ADDR " +inputMsg+"\r\n").encode())
            except:
                print("Erro ao enviar mensagem ao servidor\nDesconectado do servidor")
            else:
                try:
                    responseMsg = serverSocket.recv(1024)
                except:
                    print("Erro ao receber mensagem do servidor\nDesconectado do servidor")
                else:
                    ipv4string = responseMsg.decode().replace("ADDR","").replace(" ","")
                    ip, port = ipv4string.split(':')
                    port = int(port)
            try:
                peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #peerSocket.connect((ip, port))
                peerSocket.connect(('localhost',port))
                peerSocket.send(("USER "+myName).encode())
            except socket.error as err:
                print(f"Erro ao conectar ao peer: {err}")
                continue
            except:
                print("Erro ao enviar mensagem ao peer")
                continue
            else:
                while True:
                    inputMsg = input(f"Escreva sua mensagem para {expectedPeerName},\nou digite /bye para finalizar a conexao e voltar ao estado inicial\n")
                    if inputMsg == "/bye":
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
                        if sentBytes == -1:
                            print("Erro ao enviar mensagem")
                    except socket.error as e:
                        print(f"Erro de conexao com peer")
                        peerSocket.close()
                        break

def main():
    myName = input("Digite seu nome: ")
    my_ip = 'localhost'
    # criando o servidor local
    try:
        myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Erro ao criar o socket\nExecute a aplicação novamente")
        sys.exit()
    else:
        try:
            myServerSocket.bind((my_ip, 0))
            #myServerSocket.bind(('', 0))
        except OSError as err:
            print("Erro ao fazer o bind\nExecute a aplicação novamente")
            sys.exit()
        else:
            myAddr, myPort = myServerSocket.getsockname()

    myServerSocket.listen()
    #Conecta ao servidor do professor
    try:
        print("Tentando conexao com o servidor central...")
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                print("Erro ao enviar mensagem inicial para o servidor central\nExecute a aplicacao novamente")
                sys.exit()

    print("Conectado ao servidor com sucesso\n")
    print_help()

    keepAlive_Thread = threading.Thread(target=keep, args=(serverSocket,))
    keepAlive_Thread.daemon = True
    keepAlive_Thread.start()

    listening_thread = threading.Thread(target=handlePeerConnection, args=(myServerSocket,))
    listening_thread.daemon = True
    listening_thread.start()

    handleChat(serverSocket,myName,myAddr,myPort)
    
if __name__ == "__main__":
    main()
