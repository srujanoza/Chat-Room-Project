import socket
import threading
import tkinter 
import tkinter.scrolledtext
from tkinter import simpledialog

host = '127.0.0.1'
port = 55555

class Client : 
    
    def __init__(self, host, port):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.name = simpledialog.askstring("Name", "Choose a name", parent = msg)

        self.gui_done = False

        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self): 
        self.win = tkinter.Tk()
        self.win.configure(bg="lightblue")

        self.chatlabel = tkinter.Label(self.win, text = "Chat:", bg = "lightblue")
        self.chatlabel.config(font = ("Arial", 12))
        self.chatlabel.pack(padx = 20, pady = 5)

        self.textarea = tkinter.scrolledtext.ScrolledText(self.win)
        self.textarea.pack(padx = 20, pady = 5)
        self.textarea.config(state = 'disabled')

        self.msglabel = tkinter.Label(self.win, text = "Chat:", bg = "lightblue")
        self.msglabel.config(font = ("Arial", 12))
        self.msglabel.pack(padx = 20, pady = 5)

        self.inputarea = tkinter.Text(self.win, height = 5)
        self.inputarea.pack(padx = 20, pady = 5)

        self.sendButton = tkinter.Button(self.win, text = "Send", command = self.write)
        self.sendButton.config(font = ("Arial",12))
        self.sendButton.pack(padx = 20, pady = 5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = '{}: {}'.format(self.name, self.inputarea.get('1.0', 'end'))
        self.sock.send(message.encode('ascii'))
        self.inputarea.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('ascii')
                if message == 'CONNECT':
                    self.sock.send(self.name.encode('ascii'))
                else:
                    if self.gui_done:
                        self.textarea.config(state = 'normal')
                        self.textarea.insert('end', message)
                        self.textarea.yview('end')
                        self.textarea.config(state = 'normal')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(host, port)
