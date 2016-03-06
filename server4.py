from Tkinter import *
import tkMessageBox
import pyaudio
import socket
import threading
def send_audio(soc,stream):
    while 1:
        data = stream.read(8000)
        try:
            soc.send(data)
        except Exception:
            print 'connection problem'
            soc.close()
            break

def Connected_message_box(addr):
    tkMessageBox.showinfo("CONNECTED", "Your Voice Call connected to ip# %s %s"%(addr))           
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open( format = FORMAT, channels = CHANNELS,rate=RATE,input = True,output=True,frames_per_buffer=8000)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.bind(('172.16.45.101',5333))
except Exception:
    print 'unable to start server'
else:
    s.listen(1)
    conn,addr = s.accept()
    Connected_message_box(addr)
    A = threading.Thread(target=send_audio,args = (conn,stream))
    A.daemon = True
    A.start()
    while 1:
        data = conn.recv(8000)
        if not data:
            conn.close()
            break
        stream.write(data)

