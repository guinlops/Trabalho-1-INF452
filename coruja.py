import socket 
import threading 
import sys 
import time


host = '200.235.131.66' #ip Servidor
porta = 10001

           



def handlePeerConnection(myServerSocket):
    try:
            conn, addr = myServerSocket.accept()
            peerName = conn.recv(1024) #Primeira mensagem que recebe é o nome do usuário que fará a conexão
            print("\nConexão estabelecida com <{}>\n".format(peerName.decode()))
            while True:
                try:
                    responseMsg = conn.recv(1024) #As próximas mensagens chegarão aqui
                    if responseMsg.decode() == "/bye":
                        print("\n<{}> encerrou a conexão".format(peerName.decode()))   
                        break
                    elif responseMsg.decode() == "":
                        print("\n<{}> encerrou a conexão".format(peerName.decode()))
                        break
                    print("<{}>:".format(peerName.decode()), responseMsg.decode())
                except:
                    break
    except socket.error as e:
        print(f"Erro de conexao com peer {e}")
    except:
        print("Conexão encerrada")

            
def main():
    try:
    # Cria o socket TCP/IP
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta ao servidor/ conecta ao socket do Servidor  
        global host
        global porta
        serverSocket.connect((host, porta))
    
        print("Conectado ao servidor com sucesso")

    # Aqui você pode continuar com o restante do seu código para enviar/receber mensagens, etc.

    except socket.error as err:
        print(f"Erro ao conectar ao servidor: {err}")
        # Trate o erro aqui, como fechar o socket se necessário
    finally:
        ##msg=input("Digite a mensagem inicial\n")
        msg="USER coruja:20001"
        msg=msg+"\r\n"
        myName="coruja"
        
    sentBytes=serverSocket.send(msg.encode())
    if(sentBytes==-1):
        print("Erro ao enviar mensagem")

    serverSocket.send(str.encode("LIST\r\n"))
    responseMsg = serverSocket.recv(1024)

    if responseMsg:
        print("Mensagem Recebida com sucesso")
        #print(responseMsg.decode())


    try:
        # Cria o socket que funciona como servidor próprio, serve para conexao com peer
        myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Especifica o endereço e a porta desejados
        endereco = 'localhost'
        porta = 20001

        # Verifica se a porta está dentro do intervalo permitido
        if porta < 0 or porta > 65535:
            raise ValueError("Porta fora do intervalo válido (0-65535)")

        # Tenta vincular o socket ao endereço e porta especificados
        myServerSocket.bind((endereco, porta))

    except OSError as err:
        print(f"Erro ao vincular o socket: {err}")
        # Trate o erro de bind específico aqui

    except ValueError as ve:
        print(f"Erro de valor: {ve}")
        # erro relacionado à porta fora do intervalo válido

    finally:
        print("myServerSocket is listening")
        myServerSocket.listen(2)


    while True:
        
    
    
        thread_receber = threading.Thread(target=handlePeerConnection, args=(myServerSocket,)) 
        thread_receber.daemon = True  # Torna o thread daemon para que ele termine quando o programa principal terminar   
        thread_receber.start() #Start do recebimento 
        
        inputMsg=input("Digite o comando\n")

        if(inputMsg=="/list"):
            sentBytes=serverSocket.send(("LIST"+"\r\n").encode())
            if(sentBytes==-1):
                print("Erro ao enviar mensagem")
            responseMsg = serverSocket.recv(1024)
            print(responseMsg.decode())

        if(inputMsg=="/exit"):
            sys.exit("Tchau!")
        
        if(inputMsg=="/chat"):
            inputMsg=input("Com quem você quer se conectar?")
            sentBytes=serverSocket.send(("ADDR " +inputMsg+"\r\n").encode())
            
            if(sentBytes==-1):
                print("Erro ao enviar mensagem")
            responseMsg = serverSocket.recv(1024)
            ipv4string=responseMsg.decode().replace("ADDR","").replace(" ","")
            #print(ipv4string)
            ip, port = ipv4string.split(':')
            port=int(port)
            print(ip)
            print(port)
            try:
                    peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                    #peerSocket.connect((ip, port))
                    peerSocket.connect(('localhost',port))
                    peerSocket.send((myName).encode())
                    
            except socket.error as err:
                print(f"Erro ao conectar ao peer: {err}")
                continue
            finally:
                    while True:
                        inputMsg=input("Escreva sua mensagem ao peer\n")
                        if(inputMsg=="/bye"):
                            sentBytes=serverSocket.send(("DISC"+"\r\n").encode())
                            peerSocket.close()
                            break
                        
                        try:
                            sentBytes=peerSocket.send(inputMsg.encode())
                            if(sentBytes==-1):
                                print("Erro ao enviar mensagem")

                        except socket.error as e:
                            print(f"Erro de conexao com peer {e}")
                            peerSocket.close()
                            break
                        
                        finally:
                            continue
       

if __name__ == "__main__":
    main()
    #sys.exit(0)

    



