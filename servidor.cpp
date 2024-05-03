#include <iostream>
#include <sys/socket.h>
#include <string>
#include <netinet/in.h> //https://pubs.opengroup.org/onlinepubs/009695399/basedefs/netinet/in.h.html
#include <arpa/inet.h>
#include <unistd.h> // https://pubs.opengroup.org/onlinepubs/7908799/xsh/unistd.h.html
using namespace std;


//" The sockaddr_in structure is used to store addresses for the Internet address family. 
//Values of this type shall be cast by applications to struct sockaddr for use with socket functions."
/*struct sockaddr_in { 
    sa_family_t sin_family; // Tipo de endereço (AF_INET para IPv4)
    in_port_t sin_port;     // Número da porta do host em ordem de bytes de rede
    struct in_addr sin_addr;// Endereço IP do host em ordem de bytes de rede
    char sin_zero[8];       // Preenchimento para que a estrutura tenha o mesmo tamanho que sockaddr
};*/

int main(){

    int server_socket = socket(AF_INET,SOCK_STREAM, 0); //Define a criação de um sockete, AF_INET USA O IPV4. E SOCK_DGRAM define o protocolo, nesse caso o TCP.
    //AF_INET: It specifies the IPv4 protocol family.
    //SOCK_STREAM: It defines that the TCP type socket.

    //2. Defining Server Address

//We then define the server address using the following set of statements

    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(10000);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    //sockaddr_in: It is the data type that is used to store the address of the socket.
    //htons(): This function is used to convert the unsigned int from machine byte order to network byte order.
    //INADDR_ANY: It is used when we don’t want to bind our socket to any particular IP and instead make it listen to all the available IPs.


    //3. Binding the Server Socket
    bind(server_socket, (struct sockaddr*)&serverAddress, sizeof(serverAddress));
    listen(server_socket, 1);
    int clientSocket = accept(server_socket, nullptr, nullptr);
    
  
    // recieving data 
    char buffer[1024] = { 0 }; 
    recv(clientSocket, buffer, sizeof(buffer), 0); 
    cout << "Message from client: " << buffer << endl; 
  
    // closing the socket. 
    close(server_socket); 
}