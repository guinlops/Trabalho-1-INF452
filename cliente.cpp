

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
    serverAddress.sin_port = htons(10000); 
    //serverAddress.sin_addr.s_addr = INADDR_ANY; 
    serverAddress.sin_addr.s_addr = inet_addr("127.0.0.1"); // mMEU PRÓPRIO IP


    // sending connection request 
    connect(clientSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)); 
    std::cout<<"Digite a mensagem ao servidor \n";
    while(true){
        const char* message; 
        std::string msg;

        std::cin>>msg;
        message=msg.c_str();
        send(clientSocket, message, strlen(message), 0); 
  
    }
    // sending data 
    
    
  
    // closing socket 
    close(clientSocket); 
  
    return 0; 
}
