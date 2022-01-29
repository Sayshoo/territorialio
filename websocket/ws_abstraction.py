import websocket
from threading import *
import traceback
import struct
import dataParser
import messageTypes
import bot

__all__ = ["WesocketClient", "WebsocketClientManager"]

class WebsocketClient:
    def __init__(self, url, proxy_url, proxy_port):
        self.wsClient = websocket.create_connection(url, http_proxy=proxy_url, http_port=proxy_port)
        self.packetSentId = 0
        self.lock = Lock()

class WebsocketClientManager:
    def __init__(self, url, proxy_url, proxy_port, bot_count):
        self.url = url
        self.proxy_url = proxy_url
        self.proxy_port = proxy_port
        self.wsClients = []
        self.sentData = []
        self.addNewClientLock = Lock()
        self.bot_count = bot_count

    def connect(self, account):
        print("Connecting bot")
        Thread(target=self.connectAndSend,args=(account,)).start()
        
    def connectAndSend(self, account):
        client = WebsocketClient(self.url, account+"@"+self.proxy_url, self.proxy_port)
        self.addNewClientLock.acquire()
        self.wsClients.append(client)
        self.addNewClientLock.release()
        #_thread.start_new_thread(self.sendAllData, (self,client))
        Thread(target=self.sendDataToClient,args=(client,)).start()

    def recv():
        pass

    def pushDataToSend(self, data):
        #print("----------- Sending data %s --------------------" % len(self.sentData))
        
        packet_id = struct.unpack("c", data[0:1])[0]
        packet_id = dataParser.getHandlerId(packet_id)

        if(packet_id == 0x90):
            obj = messageTypes.deserialize(data, messageTypes.seaAttack)
            bot.generateSpawnPointsSquare(obj['X'], obj['Y'], self.bot_count)
            self.sendLocationAll(obj)
        else :
            self.sentData.append(data)
            self.sendDataToAll()

    def sendLocationAll(self, obj):
        copyClients = list(self.wsClients)
        for i in range(len(copyClients)):
            try:
                newX, newY = bot.getNextSpawnPoint(obj['X'], obj['Y'], self.bot_count)
                obj['X'] = newX
                obj['Y'] = newY
                data = bytes(messageTypes.serialize(obj, obj["_schema_"]))
                Thread(target=copyClients[i].wsClient.send_binary,args=(data,)).start()
            except Exception as e:
                print("----- Exception forwarding to clonesock ------")
                print(traceback.format_exc())
                print("----- Exception forwarding to clonesock ------")
                self.wsClients.remove(copyClients[i])

    def sendDataToAll(self):
        for client in list(self.wsClients):
            Thread(target=self.sendDataToClient,args=(client,)).start() 

    def sendDataToClient(self, client : WebsocketClient):
        client.lock.acquire()
        #print("Sending [%s:%s] messages" % (client.packetSentId, len(self.sentData)))
        for index in range(client.packetSentId, len(self.sentData)):
            message = self.sentData[index]
            try:    
                client.wsClient.send_binary(message)
                client.packetSentId += 1
            except Exception as e:
                print("----- Exception forwarding to clonesock ------")
                print(traceback.format_exc())
                print("----- Exception forwarding to clonesock ------")
                self.wsClients.remove(client)
        client.lock.release()
