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
    
    bytesEnviados=serverSocket.send(msg.encode())
    if(bytesEnviados==-1):
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
    porta = 30000

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