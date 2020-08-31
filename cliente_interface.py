import sys
import threading
import Pyro4


class Client(object):
    def __init__(self):
        self.chat = Pyro4.core.Proxy('PYRONAME:Servidor.comunicacao.RPC')
        self.abort = 0
        self.chat_history = ""
        self.nick = ""
        self.status = ""
        self.conexao = "jogo"
        self.client_context = []
        self.contexto = ""


    @Pyro4.expose
    @Pyro4.oneway
    def message(self, nick_emissor, nick_receptor, msg):

        if nick_emissor != self.nick and nick_emissor != "Servidor":
            n = [d for d, e in enumerate(self.client_context) if e["name"] == nick_emissor]
            m = n[0]
            self.client_context[m]["chatHistory"] += '<font  color=#FF0000>' + nick_emissor + ":" + " " + msg + '<br>' + '</font>'
            if self.contexto == nick_emissor:
                self.chat_history += '<font  color=#FF0000>' + nick_emissor + ":" + " " + msg + '<br>' + '</font>'
            #self.client_context[m]["chatHistory"] = self.chat_history
        elif nick_emissor == "Servidor":
            pass
           # print('errou')
            #self.client_context[m]["chatHistory"] += '<font  color=#437C17>' + '<b>' + nick_emissor + ":" + " " + msg + '</b>' + '<br>' + '<br>' + '</font>'
            #self.chat_history += '<font  color=#437C17>' + '<b>' + nick_emissor + ":" + " " + msg + '</b>' + '<br>' + '<br>' + '</font>'


    def dispatch_broadcast(self, msg):
        self.chat.Broadcast_msg(self.conexao, "Servidor", msg)

    def send(self, msg,player_receptor):
        if msg:
            self.chat.Send_msg(self.conexao, self.nick,player_receptor, msg)

    def start_conexao(self):
        self.nick = self.chat.Connect(self.conexao, self)

    def setOffline(self):
        self.chat.setOffiline(self.conexao, self.nick)

    def setOnline(self):
        self.chat.setOnline(self.conexao, self.nick)

    def getStatus(self):
        self.status = self.chat.getStatus(self.conexao, self.nick)

    def getAgenda(self):
        return self.chat.getPlayers()

    def createChatHistory(self):
        players = self.getAgenda()
        for i in players:
            if i != self.nick:
                self.client_context.append({"name":i,"chatHistory":""})



class DaemonThread(threading.Thread):
    def __init__(self, chat):
        threading.Thread.__init__(self)
        self.chatter = chat
        self.setDaemon(True)


    def run(self):
        with Pyro4.core.Daemon() as daemon:
            daemon.register(self.chatter)
            daemon.requestLoop(lambda: not self.chatter.abort)
