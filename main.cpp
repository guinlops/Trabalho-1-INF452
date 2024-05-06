#include <iostream>
#include <cstring>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string>
#include <thread>

void handleServerConnection(int serverSocket) {
    while (true) {
        char buffer[1024] = {0};
        std::string msg;
        std::cout<<"Digite alguma coisa para mandar ao servidor\n";
        std::getline(std::cin, msg);
        if (msg == "sair")
            break;

        ssize_t bytesSent = send(serverSocket, msg.data(), msg.size(), 0);
        if (bytesSent == -1) {
            std::cerr << "Erro ao enviar mensagem\n";
            break;
        }

        // Receiving data from server
        
        ssize_t bytesReceived = recv(serverSocket, buffer, sizeof(buffer), 0);
        if (bytesReceived == -1) {
            std::cerr << "Erro ao receber mensagem do servidor\n";
            break;
        } else if (bytesReceived == 0) {
            std::cout << "Conexão encerrada pelo servidor\n";
            break;
        }

        std::cout << "Mensagem do servidor: " << buffer << std::endl;

       
    }

    close(serverSocket);
}
void handleClientConnection(int clientSocket) {
    std::cout << "Novo cliente conectado na porta 20000" << std::endl;

    
    
    while (true) {
        char buffer[1024] = {0};
        
        // Receiving data from client
        ssize_t bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
        if (bytesReceived == -1) {
            std::cerr << "Erro ao receber mensagem do cliente" << std::endl;
            break;
        } else if (bytesReceived == 0) {
            std::cout << "Conexão encerrada pelo cliente" << std::endl;
            break;
        }

        //std::cout << "Mensagem do peer: " << buffer << std::endl;
    }

    close(clientSocket);
}


int main() {
    // Conexão com o servidor
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0); //CRIA SOCKET, AF_INET DEFINE QUE É IPV4, SOCK_STREAM DEFINE QUE É TCP
    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(10001); //PORTA NA QUAL VAI SE CONECTAR
    //serverAddress.sin_addr.s_addr = inet_addr("200.235.131.66"); // SERVIDOR DO VICTOR
    serverAddress.sin_addr.s_addr = inet_addr("127.0.0.1"); //SERVIDOR LOCAL PARA TESTE DE THREADS


    if (connect(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) == -1) { //TENTA CONEXAO
        std::cerr << "Conexão com o servidor falhou" << std::endl;
        return -1;
    }

    std::cout << "Conectado ao servidor" << std::endl;

    //CONEXAO COM OUTRO PEER
    int clientListenerSocket = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in clientListenerAddress;
    clientListenerAddress.sin_family = AF_INET;
    clientListenerAddress.sin_port = htons(20000); // PORTA PARA ACEITAR CONEXAO COM OUTROS CLIENTES
    clientListenerAddress.sin_addr.s_addr = INADDR_ANY;

    if (bind(clientListenerSocket, (struct sockaddr*)&clientListenerAddress, sizeof(clientListenerAddress)) == -1) {
        std::cerr << "Erro ao vincular o socket à porta" << std::endl;
        return -1;
    }

    if (listen(clientListenerSocket, 5) == -1) {
        std::cerr << "Erro ao ouvir conexões de entrada" << std::endl;
        return -1;
    }

    std::cout << "Pronto para aceitar conexões de outros clientes na porta 20000" << std::endl;
    /////////////////////////////////////////////////////////////////////////////////////



    // Lidar com a comunicação com o servidor em uma thread separada
    std::thread serverThread(handleServerConnection, serverSocket);
    ///////////////////////////////////////////////////////////////



    // Loop para aceitar conexões de outros clientes
    while (true) {
        sockaddr_in clientAddress;
        socklen_t clientAddrSize = sizeof(clientAddress);
        int clientSocket = accept(clientListenerSocket, (struct sockaddr*)&clientAddress, &clientAddrSize);
        if (clientSocket == -1) {
            std::cerr << "Erro ao aceitar conexão de cliente" << std::endl;
            continue;
        }

        // Lidar com a conexão do cliente em uma thread separada
        std::thread clientThread(handleClientConnection, clientSocket);
        clientThread.detach(); // Não bloquear o thread principal
    }

    // Fechar sockets
    close(serverSocket);
    close(clientListenerSocket);

    return 0;
}