# Peer-to-Peer Chat System

Este projeto implementa um sistema de chat P2P (Peer-to-Peer) baseado em sockets TCP, permitindo que os usuários se conectem e conversem diretamente entre si.

## 📌 O que é P2P e TCP?

### 🔄 Peer-to-Peer (P2P)
P2P (Peer-to-Peer) é um modelo de rede onde os dispositivos conectados atuam como clientes e servidores ao mesmo tempo, possibilitando a comunicação direta entre eles sem a necessidade de um servidor central intermediário. Esse tipo de arquitetura é amplamente utilizado em compartilhamento de arquivos, sistemas de comunicação distribuídos e redes descentralizadas.

### 🌐 Transmission Control Protocol (TCP)
TCP (Transmission Control Protocol) é um dos principais protocolos da camada de transporte da internet, garantindo a entrega confiável e ordenada de pacotes de dados entre dispositivos conectados. No contexto deste projeto, o uso de TCP assegura que as mensagens enviadas entre os peers sejam entregues corretamente e na sequência correta, evitando perda de dados durante a comunicação.

## 📌 Funcionalidades
- Listar peers online
- Iniciar chats privados entre peers
- Manter conexão ativa com o servidor central
- Exibir informações da conexão
- Comandos de interação

## 🚀 Como executar
1. **Instale o Python** (versão 3.x).
2. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
3. Acesse a pasta do projeto:
   ```sh
   cd seu-repositorio
   ```
4. Execute o script:
   ```sh
   python3 chat.py
   ```
5. Digite seu nome e siga as instruções do terminal.

## 🔧 Comandos disponíveis
- `/list` → Lista os peers online
- `/chat` → Inicia um chat com outro peer
- `/help` → Exibe a lista de comandos
- `/info` → Exibe informações da conexão
- `/exit` → Sai do programa
- `/bye` → Encerra uma conversa ativa

## 🏗 Estrutura do Código
- `main()`: Inicia o programa e configura a conexão com o servidor central.
- `handleChat()`: Gerencia as interações do usuário.
- `handlePeerConnection()`: Gerencia conexões entre peers.
- `keep()`: Mantém a conexão ativa enviando mensagens periódicas ao servidor.
- `print_help()`: Exibe os comandos disponíveis.

## 🔗 Dependências
Este projeto utiliza apenas a biblioteca padrão do Python.

## 📝 Autores
- Guilherme Nunes Lopes - 105462
- Cícero Cipriano Maciel - 102021

