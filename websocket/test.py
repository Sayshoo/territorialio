import websocket
import _thread
import time

def on_message(ws, message):
    print("message %s" % message)

def on_error(ws, error):
    print("====================(error)================")
    print(error)
    print("====================(/error)================")

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("=================on open==================")
    def run(*args):
        return
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())
    print("=================/on open==================")

if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://territorial.io/socket/",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()