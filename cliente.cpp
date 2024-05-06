

// C++ program to illustrate the client application in the 
// socket programming 
#include <cstring> 
#include <iostream> 
#include <netinet/in.h> 
#include <sys/socket.h> 
#include <unistd.h> 
#include <arpa/inet.h> // Para a função inet_addr
#include <string>
int main() 
{ 
    // creating socket 
    int clientSocket = socket(AF_INET, SOCK_STREAM, 0); 
  
    // specifying address 
    sockaddr_in serverAddress; 
    serverAddress.sin_family = AF_INET; 
    serverAddress.sin_port = htons(20000); 
    //serverAddress.sin_addr.s_addr = INADDR_ANY; 
    //serverAddress.sin_addr.s_addr = inet_addr("200.235.131.66"); //
    serverAddress.sin_addr.s_addr=inet_addr("127.0.0.1");

    // sending connection request 
   
    if( connect(clientSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress))==-1){
        std::cout<<"Conexao falhou\n";
        return -1;
    }
    std::cout<<"Conexao feita\n";
    
   
    while(true){
         /*std::string msg;
        std::cout<<"Digite a mensagem ao peer \n";
        std::getline(std::cin, msg);
        if (msg == "sair")
            break;

        ssize_t bytesSent = send(clientSocket, msg.data(), msg.size(), 0);
        if (bytesSent == -1) {
            std::cerr << "Erro ao enviar mensagem\n";
            break;
        }

        // Receiving data from server
        char buffer[1024] = {0};
        ssize_t bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
        if (bytesReceived == -1) {
            std::cerr << "Erro ao receber mensagem do servidor\n";
            break;
        } else if (bytesReceived == 0) {
            std::cout << "Conexão encerrada pelo servidor\n";
            break;
        }

        std::cout << "Mensagem do servidor: " << buffer << std::endl;*/
    }

    // sending data 
    
    
  
    // closing socket 
    close(clientSocket); 
  
    return 0; 
}
