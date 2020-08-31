import pygame
import pygame_gui

from cliente_interface import Client
from cliente_interface import DaemonThread
from threading import Thread
from pygame_gui.elements.ui_selection_list import UISelectionList




chat = Client()
daemonThread = DaemonThread(chat)
daemonThread.start()
chat.start_conexao()
chat.createChatHistory()
agenda = chat.getAgenda()
agenda.remove(chat.nick)
pygame.init()
html = """"""
html = html + chat.chat_history
screen = pygame.display.set_mode([600, 680])
manager = pygame_gui.UIManager((600, 680), "style.JSON")
manager2 = pygame_gui.UIManager((600, 680), "style2.JSON")
apelido = chat.nick

recieve = len(chat.chat_history)


button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((140, 75), (90, 30)),
                                            text='offline',
                                            manager=manager)

chat_textBox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(245, 10, 350, 600),
                                             html_text=html,
                                             manager=manager)


chat_entryText = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((245, 610), (350, 200)),
    manager=manager)

button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 75), (90, 30)),
                                            text='online',
                                            manager=manager)

button3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((42, 25), (180, 30)),
                                            text=apelido,
                                            manager=manager)



lista = UISelectionList(relative_rect=pygame.Rect(60, 200, 150, 150),
                        item_list=agenda,
                        manager=manager)

screen.fill([203, 237, 216])
clock = pygame.time.Clock()


manager.draw_ui(screen)
manager2.draw_ui(screen)
pygame.display.flip()

chat_context = None

running = True
while running:

    time_delta = clock.tick(60) / 1000.0

    if recieve < len(chat.chat_history) and chat_context != None:
        chat_textBox.kill()
        html = chat.chat_history
        chat_textBox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((245, 10), (350, 600)),
                                             html_text=html,
                                             manager=manager)
        recieve = len(chat.chat_history)



    for event in pygame.event.get():
        #fechar a aplicação
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                texto = chat_entryText.get_text()
                #salvar input também no dicionario de chatHistory
                chat.chat_history = chat.chat_history + str('<font  color=#0000FF>' + apelido + ":" + " " + str(texto) + '<br>' + '</font>')
                #print(chat.chat_history)
                chat_entryText.set_text('')
                if t:
                    n = [d for d, e in enumerate(chat.client_context) if e["name"] == t]
                    m = n[0]
                    chat.client_context[m]["chatHistory"] = chat.chat_history
                    chat.send(texto,t)
        if event.type == pygame.USEREVENT:
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == button:
                    chat.setOffline()
                elif event.ui_element == button2:
                    chat.setOnline()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == lista:
                    t = lista.get_single_selection()
                    n = [d for d, e in enumerate(chat.client_context) if e["name"] == t]
                    m = n[0]
                    chat_context = chat.client_context[m]["name"]
                    chat.contexto = chat_context
                    chat.chat_history = chat.client_context[m]["chatHistory"]
                    recieve = len(chat.client_context[m]["chatHistory"])
                    if recieve == 0:
                        chat.chat_history = chat.chat_history + str('<font  color=#0000FF>' + 'chat iniciado com ' + t + '<br>' + '</font>')
                    else:
                        print(chat.chat_history)
                        recieve = 0

        manager.process_events(event)
        manager2.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(screen)
    manager2.draw_ui(screen)
    pygame.display.flip()
    pygame.event.pump()








