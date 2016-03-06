from Tkinter import *
import tkMessageBox
import pyaudio
import socket
import threading

def send_audio(soc,stream): 
    while 1:
        data = stream.read(8000)
        soc.send(data)

def calling(ip,fw):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,5333))
    except Exception:
        print 'there was some problem during connection. Try again'
    else:
        fw.destroy()
        print 'connected'
        #Connected_message_box(ip)
        A = threading.Thread(target=send_audio,args = (s,stream))
        A.daemon = True
        A.start()
        while 1:
            data = s.recv(8000)
            if not data:
                print 'connection closed'
            stream.write(data)   


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open( format = FORMAT, channels = CHANNELS,rate=RATE,input = True,output=True,frames_per_buffer=8000)

#GUI
first_window = Tk()
var = StringVar()
label = Label( first_window, textvariable=var, relief=RAISED)
var.set("Provide the calling IP")
label.pack()
ip_address = Entry(first_window)
ip_address.pack()
ip_address.focus_set()

def notConnected(text):
    tkMessageBox.showerror("ERROR CONNECTION","COULD NOT CONNECT TO THE IP#"%(text))
    ip_address.delete(0, 'end')
    
def error():
    tkMessageBox.showerror("ERROR","THE IP ADDRESS YOU ENTERED IS NOT VALID")
    ip_address.delete(0, 'end')

def Connected_message_box(text):
    tkMessageBox.showinfo("CONNECTED", "Your Voice Call connected to ip# %s"%(text))

def callback(first_window):
    cont = True
    text=ip_address.get()
    num= text.split('.')
    for i in range(len(num)):
        if num[i].isdigit():
            num[i]=int(num[i])
        else:
            print("the ip should be a number")
            cont=False
            error()
            break
    if cont==True:
        if len(num) != 4:
            cont=False
            error()
        else :
            for i in num:
                if i<0 or i>255:
                    cont=False
                    error()
                    break
    if cont == True:
        calling(text,first_window)
        
b = Button(first_window, text="CALL", width=10, command=lambda:callback(first_window))
b.pack()
mainloop()

