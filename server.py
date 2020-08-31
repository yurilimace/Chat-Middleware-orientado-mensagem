import Pyro4
import time
import ast
import pika


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Servidor(object):
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        self.conexao = {}
        self.players = []
        self.turno = 0
        self.MOM = channel
        self.p_name = ['Player 1','Player 2','Player 3','Player 4']


    def getPlayers(self):
        return self.p_name

    def CreateUser(self):
        if len(self.players) > 0:
            user = {"name": self.p_name[len(self.players)], "disponivel": "sim"}
        else:
            print(len(self.players))
            user = {"name": self.p_name[len(self.players)], "disponivel": "sim"}

        return user

    def CreateFilaMensagem(self):
        for player_name in self.p_name:
            self.MOM.queue_declare(queue=player_name + "Filamsg")

    def Connect(self,conexao,callback):
        new_user = self.CreateUser()
        if conexao not in self.conexao:
            self.conexao[conexao] = []
        self.conexao[conexao].append((new_user["name"], callback))
        self.players.append(new_user)
        self.MOM.queue_declare(queue=new_user["name"] + "Filamsg")
        self.Send_server_msg(conexao, new_user["name"], "Conexao com " + new_user["name"] + " iniciada")
        time.sleep(0.2)
        return new_user["name"]


    def Send_server_msg(self, conexao, player, mensagem):
        for (p, c) in self.conexao[conexao]:
            for i in self.players:
                if p == player and p == i['name']:
                    c.message('Servidor', i['name'], mensagem)

    def Send_msg(self, conexao, player_emissor, player_receptor, mensagem):
        for (p, c) in self.conexao[conexao]:
            n = [d for d in self.players if d["name"] == player_receptor]
            if n:
                if p != player_emissor and p == n[0]["name"] and n[0]["disponivel"] == 'sim':
                        c.message(player_emissor, player_receptor, mensagem)
                elif p != player_emissor and p == n[0]["name"] and n[0]["disponivel"] == 'nao':
                    encode_message = player_emissor + ","+ player_receptor +","+mensagem
                    self.MOM.basic_publish(exchange='',routing_key=player_receptor+"Filamsg",body=str(encode_message))
                        #self.Send_server_msg(conexao, player_emissor, player_receptor + " esta offline")
            else:
                encode_message = player_emissor + "," + player_receptor + "," + mensagem
                self.MOM.basic_publish(exchange='', routing_key=player_receptor + "Filamsg", body=str(encode_message))
                pass
                #self.Send_server_msg(conexao, player_emissor, player_receptor + " esta offline")


    def setOffiline(self, conexao, player):
        for i, j in enumerate(self.players):
            print(self.players[i]['name'])
            if player == self.players[i]['name']:
                self.players[i]['disponivel'] = 'nao'
                self.Send_server_msg(conexao, self.players[i]['name'], self.players[i]['name'] + " esta offline")

    def setOnline(self, conexao, player):
        for i, j in enumerate(self.players):
            print(self.players[i]['name'])
            if player == self.players[i]['name']:
                self.players[i]['disponivel'] = 'sim'
                self.Send_server_msg(conexao, self.players[i]['name'], self.players[i]['name'] + " esta online")
                self.MOM.queue_declare(queue=self.players[i]['name'] + "Filamsg")
                self.MOM.basic_publish(exchange='', routing_key=self.players[i]['name'] + "Filamsg", body="server_send_stop_consuming")
                self.MOM.basic_consume(queue=self.players[i]['name'] + "Filamsg", on_message_callback=self.callback, auto_ack=True)
                self.MOM.start_consuming()
                time.sleep(0.2)



    def callback(self,ch,method, properties, body):
        consumidor = body.decode()
        message = consumidor.split(',')
        print(message)
        #self.Send_msg("jogo","Player 1","Player 2","callback")
        if body.decode("utf-8") == 'server_send_stop_consuming':
            print('parou de consumir')
            self.MOM.stop_consuming()
        else:
            self.Send_msg("jogo", message[0], message[1], message[2])
            #self.Send_msg("jogo", "Player 1", "Player 2", "callback")



    def getStatus(self, conexao, player):
        for i, j in enumerate(self.players):
            print(self.players[i]['name'])
            if player == self.players[i]['name']:
                return self.players[i]['disponivel']



def main():
    server = Servidor()
    Pyro4.Daemon.serveSimple({
        Servidor: "Servidor.comunicacao.RPC"
    })


if __name__ == '__main__':
    main()
