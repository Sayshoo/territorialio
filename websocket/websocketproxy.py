#!/usr/bin/python3
# websocket proxy

import _thread
import argparse
import asyncio
import concurrent.futures
import ctypes
import os
import pathlib
import random
import ssl
import string
import struct
import sys
import time
import traceback
from importlib import reload
from random import randrange

import websocket
import websockets
from aioconsole import ainput

import bot
import dataParser as dataParser
import messageTypes
import recursiveReload
import ws_abstraction

globalSocket = {}
botSockType = 1
botCount = 150
proxy_url = "containerlx"
proxy_port="9050"

async def sendJoin():
    print("sendJoin")
    global globalSocket
    await globalSocket.send(bytearray.fromhex('88'))

async def endSkip():
    print("sendSkip")
    global globalSocket
    await globalSocket.send(bytearray.fromhex('80'))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

async def connectSlaveClients(url, count):
    if(botSockType == 0):
        result = [await websockets.connect(url, ping_timeout=60, ping_interval=5) for _ in range(count)]
    elif(botSockType == 1):
        result = [websocket.create_connection("wss://territorial.io/socket/", http_proxy=id_generator()+"@containerlx", http_port="9050") for _ in range(count)]
    #ws = websocket.create_connection("wss://territorial.io/socket/", http_proxy="localhost", http_port="9050")
    return result

async def sendCs(cs,message):
    if(botSockType == 0):
        await cs.send(message)
    elif(botSockType == 1):
    #    cs.send_binary(message)
       _thread.start_new_thread( cs.send_binary, (message,))

async def inputRoutine():
    line = await ainput(">>> ")
    while line != "q":
        line = await ainput(">>> ")
        if line.startswith("send"):
            if line.find("join") != -1:
                await sendJoin()
            elif line.find("skip") != -1:
                await sendSkip()
        elif line.startswith("print"):
            if line.find("websocket") != -1:
                print(globalSocket)

async def websocketProxy(websocket, path):
    '''Called whenever a new connection is made to the server'''
    print('Connection Established %s' % path)

    url = REMOTE_URL + path
    
    
    #cloneSocks = [await websockets.connect(url, ping_timeout=60, ping_interval=5) for _ in range(3)]
    #cloneSocks = await connectSlaveClients(url, botCount)
    websocketManager = ws_abstraction.WebsocketClientManager(url, proxy_url, proxy_port)
    [ websocketManager.connect(id_generator()) for _ in range(botCount) ]
    #csLen = len(cloneSocks)
    #print("connected %s" %csLen)
    #print(cloneSocks)
    
    
    async with websockets.connect(url) as ws:
        print("Connected to remote server")
        file_object = open("server.log", 'a+')
        file_object.write("=============== Connection Established ===============\n")
        file_object.close()
        taskA = asyncio.create_task(clientToServer(ws, websocket, websocketManager))
        taskB = asyncio.create_task(serverToClient(ws, websocket, websocketManager))
        taskC = asyncio.create_task(reloadParser())
        #await asyncio.create_task(inputRoutine())
        #await asyncio.create_task(sendPingPongCloneSocks)
	
        #[_thread.start_new_thread(botsTraffic, (cs,)) for cs in cloneSocks]
        #[await botsTraffic(cs) for cs in cloneSocks]

        await taskA
        await taskB
        await taskC

async def clientToServer(ws, websocket, websocketManager):
    try:
        async for message in ws:
            file_object = open("server.log", 'a+')
            file_object.write("[client]-%s\n" % message.hex())
            file_object.close()
            #print("[client]-%s" % message.hex())
            try:    
                await websocket.send(message)
            except Exception as e:
                ws.close()
    except Exception as e:
        pass

async def serverToClient(ws, websocket, websocketManager):
    global globalSocket 
    globalSocket = ws
    try:
        async for message in websocket:
            
            try:
                file_object = open("server.log", 'a+')
                file_object.write("[server]-%s\n" % message.hex())
                file_object.close()
            except Exception as e:
                 print("Exception at logging %s" % e)

	#print("[server]-%s" % message.hex())
        #print("[server]-%s" % message)
        #await [ws2.send(message) for ws2 in cloneSocks]    
            try:
                messageOverride = dataParser.parse(bytes(message), "server")
            except Exception as e:
                print("=--------------serverToClient Exception--------------=")
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                #print(exc_type, fname, exc_tb.tb_lineno)        
                print(traceback.format_exc())
                print("=--------------serverToClient Exception--------------=")
            
            #await ws.send(messageOverride)
            await ws.send(message)
            #continue
            try:    
                packet_id = struct.unpack("c", messageOverride[0:1])[0]
                packet_id = dataParser.getHandlerId(packet_id)
                print("CS %s %s" %(packet_id, hex(packet_id)))
                try:    
                    #print("sending for bot %s" % cs.connected)
                    if packet_id != 128:
                        #await cs.send(message)
                        #cs.send(message)
                        #cs.send_binary(message)
                        websocketManager.pushDataToSend(message)
                        continue
                except Exception as ex:
                    print("----- Exception forwarding to clonesock ------")
                    print(traceback.format_exc())
                    print("----- Exception forwarding to clonesock ------")
                    #cloneSocks.remove(cs)
            except Exception as e:
                print("----- Exception forwarding to clonesocks ------")
                print(e)
                print("----- Exception forwarding to clonesocks ------")

    except Exception as e:
        pass            

async def sendPingPongCloneSocks():
    while True:
        for cs in cloneSocks:
            try:    
                await cs.send(0x90.to_bytes(1, "big"))
                await asyncio.sleep(5)
                await cs.send(0x98.to_bytes(1, "big"))
                await asyncio.sleep(5)
            except Exception as ex:
                cloneSocks.remove(cs)

async def reloadParser():
    try:    
        print("reload module started")
        while True:
            #print("reload module")
            recursiveReload.rreload(dataParser)
            await asyncio.sleep(1)
    except Exception as e:
        print("=-------------- Reload Module Exception --------------=")
        print(e)
        print("=-------------- Reload Module Exception --------------=")

if __name__ == '__main__':
    #ctypes.windll.shell32.IsUserAnAdmin()
    conf_file = open('ws.conf', 'r')
    conf_lines = conf_file.readlines()
    parser = argparse.ArgumentParser(description='websocket proxy.')
    parser.add_argument('--host', help='Host to bind to.',
                        default=conf_lines[0].strip())
    parser.add_argument('--port', help='Port to bind to.',
                        default=conf_lines[1].strip())
    parser.add_argument('--remote_url', help='Remote websocket url',
                        default='wss://territorial.io/socket/')
    args = parser.parse_args()

    REMOTE_URL = args.remote_url
    
    print('Starting proxy at %s:%s to %s' %(args.host, args.port, REMOTE_URL))
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(
    pathlib.Path(__file__).with_name('localhost.pem'))
    
    start_server = websockets.serve(websocketProxy, args.host, args.port, ssl=ssl_context)
    #start_server = websockets.serve(websocketProxy, args.host, args.port)
    
    print('Proxy started at %s:%s to %s' %(args.host, args.port, REMOTE_URL))


    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
