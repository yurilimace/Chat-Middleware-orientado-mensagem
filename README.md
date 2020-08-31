# Chat-Middleware-orientado-mensagem
Implementação de chat utilizando python com comunicação tipo RPC e Middleware orientado a mensagem, para construção da comnunicação RPC
foi utilizado a biblioteca Pyro4 do python e no Middleware foi utilizado o RabbitMQ como broker para o gerenciamento das mensagens, a interface grafica foi construida
utilizando a biblioteca pygame em conjunto com o pacote pygame_gui.

## Autor
José Yuri Lima Lira

### Executando o projeto
1.  Instale o Pyro4 e o pygame utilizando os comandos rodando no prompt de comando o  pip, para o pygame insira o comando "pip install pygame" para o Pyro4 "pip install Pyro4" e para o pygame_gui "pip install pygame-gui"
2.  Instale o RabbitMQ através do software chocolatey ou através do arquivo para maiores informações segue o link: https://www.rabbitmq.com/install-windows.html
3.  Para executar o chat é necessário primeiro executar o servidor de nomes através do comando "python -m Pyro4.naming"
4.  Após a execução do servidor de nomes é necessário executar o servidor do chat basta rodar o arquivo server.py
5.  após a execução desses dois arquivos execute o arquivo chat.py e o chat será aberto



