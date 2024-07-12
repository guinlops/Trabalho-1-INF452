import socket 
import threading 
import sys 
import time


host = '200.235.131.66' #ip Servidor
porta = 10001           
try:
    # Cria o socket TCP/IP
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta ao servidor
    serverSocket.connect((host, porta))
    
    print("Conectado ao servidor com sucesso")

    # Aqui você pode continuar com o restante do seu código para enviar/receber mensagens, etc.

except socket.error as err:
    print(f"Erro ao conectar ao servidor: {err}")
    # Trate o erro aqui, como fechar o socket se necessário
finally:
    msg=input("Digite a mensagem inicial\n")
    msg=msg+"\r\n"
    
    sentBytes=serverSocket.send(msg.encode())
    if(sentBytes==-1):
        print("Erro ao enviar mensagem")

    serverSocket.send(str.encode("LIST\r\n"))
    responseMsg = serverSocket.recv(1024)

    if responseMsg:
        print("Mensagem Recebida com sucesso")
        #print(responseMsg.decode())


try:
    # Cria o socket de cliente
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Especifica o endereço e a porta desejados
    endereco = 'localhost'
    porta = 20000

    # Verifica se a porta está dentro do intervalo permitido
    if porta < 0 or porta > 65535:
        raise ValueError("Porta fora do intervalo válido (0-65535)")

    # Tenta vincular o socket ao endereço e porta especificados
    clientSocket.bind((endereco, porta))

except OSError as err:
    print(f"Erro ao vincular o socket: {err}")
    # Trate o erro de bind específico aqui

except ValueError as ve:
    print(f"Erro de valor: {ve}")
    # erro relacionado à porta fora do intervalo válido

finally:
   clientSocket.listen(1)









def handlePeerConnection(peerSocket):
    try:
            conn, addr = peerSocket.accept()
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
                    print("<{}>:".format(nome_recebido.decode()), responseMsg.decode())
                except:
                    break
    except socket.error as e:
        print(f"Erro de conexao com peer {e}")

            


thread_receber = threading.Thread(target=handlePeerConnection, args=(clientSocket,)) 
thread_receber.start() #Start do recebimento 

while True:
    
   
    
    inputMsg=input("Digite o comando\n")


    


    if(inputMsg=="/list"):
        sentBytes=serverSocket.send(("LIST"+"\r\n").encode())
        if(sentBytes==-1):
            print("Erro ao enviar mensagem")
        responseMsg = serverSocket.recv(1024)
        print(responseMsg.decode())

    if(inputMsg=="/chat"):
        inputMsg=input("Com quem você quer se conectar?")
        sentBytes=serverSocket.send(("ADDR " +inputMsg+"\r\n").encode())
        if(sentBytes==-1):
            print("Erro ao enviar mensagem")
        responseMsg = serverSocket.recv(1024)
        ipv4string=responseMsg.decode().replace("ADDR","").replace(" ","")
        #print(ipv4string)
        ip, port = ipv4string.split(':')
        #print(ip)
        #print(porta)
        try:
                peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                peerSocket.connect((ip, port))
                peerResponseThread = threading.Thread(target=handlePeerConnection, args=(peerSocket,)) 
                peerResponseThread.start() #detach da thread
        except socket.error as err:
            print(f"Erro ao conectar ao servidor: {err}")
        finally:

                while True:
                    inputMsg=input("Escreva sua mensagem ao peer")
                    if(inputMsg=="/bye"):
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
       

    



