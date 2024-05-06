#include <iostream>
#include <sys/socket.h>
#include <string>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
using namespace std;

int main() {
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(10001);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    bind(server_socket, (struct sockaddr*)&serverAddress, sizeof(serverAddress));
    listen(server_socket, 1);
    std::cout<<"Servidor on\n";
    const char* bye = "Bye";
    
    int clientSocket = accept(server_socket, nullptr, nullptr);
    

   
    while(true) {
        char buffer[1024] = { 0 }; 
        recv(clientSocket, buffer, sizeof(buffer), 0); 
        cout << "Message from client: " << buffer << endl;

        if(strcmp(bye, buffer) == 0){
            break;
        }

        // Aqui você pode enviar uma mensagem de resposta ao cliente
        const char* response = "Message received!";
        send(clientSocket, response, strlen(response), 0);
    }


    std::cout<<"Servidor off\n";
    close(server_socket); 
    return 0;
}