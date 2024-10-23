
import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt
import socket
import select

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
    
        #-------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        #-------------------------------------------------------------------
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top",pady=5)
        #
        self.ipPortLbl = tk.Label(self.groupCon, text='Server Port', padx=10)
        self.ipPortLbl.pack(side="left")
        #
        self.ipPort = tk.Entry(self.groupCon, width=20)
        self.ipPort.insert(tk.END, '60003')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.ipPort.bind('<Return>', statusHandler)
        self.ipPort.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        self.connectButton = tk.Button(self.groupCon,
            command = statusButtonClick, width=10)
        self.connectButton.pack(side="left",padx=5)
        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")
        #
        self.clearButton = tk.Button(self.groupCon, text='clr msg',
            command = clearButtonClick)
        self.clearButton.pack(side="left",padx=5)
        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=20, width=90,
            state=tk.DISABLED)
        self.msgText.pack(side="top",padx=(15,0))

        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top",pady=5)
        #
        self.textInLbl = tk.Label(self.groupSend, text='broadcast message',width=20)
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=40)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', broadcastHandler)
        self.textIn.pack(side="left"),
        #
        self.sendButton = tk.Button(self.groupSend, text = 'send',
            command = broadcastButtonClick,width= 5)
        self.sendButton.pack(side="left",padx=55)
        
        #-------------------------------------------------------------------
        # row 4: client list
        #-------------------------------------------------------------------
        self.groupClient = tk.LabelFrame(bd=0)
        self.groupClient.pack(side="top",pady=5)
        
        self.textClientList = tk.Label(self.groupClient, text='Connected clients',width=20)
        self.textClientList.pack(side="left")
        
        self.groupList= tk.LabelFrame(self.groupClient,width=40, bd=0)
        self.groupList.pack(side="left",)
        self.clientList = tk.Listbox(self.groupList,height=10, width= 40)
        self.clientList.pack(side="left", fill = "y")
        self.scrollbar = tk.Scrollbar(self.groupList, orient="vertical")
        self.scrollbar.config(command=self.clientList.yview)
        self.scrollbar.pack(side="right",fill="y")
        
        self.groupClientControl = tk.LabelFrame(self.groupClient, bd=0)
        self.groupClientControl.pack(side="left")
        
        self.discAllButton = tk.Button(self.groupClientControl, text='Disconnect All', command = "", width= 15)
        self.discAllButton.pack(side="top", pady = 15,padx=15)

        self.discSelButton = tk.Button(self.groupClientControl, text='Disconnect Selected', command = "", width= 15)
        self.discSelButton.pack(side="top", pady = 15,padx=15)      
        
        #-------------------------------------------------------------------
        # row 5: Be weird
        #-------------------------------------------------------------------
        self.groupMsgClient = tk.LabelFrame(bd=0)
        self.groupMsgClient.pack(side= "top", pady= 5)
        
        self.labelMsgClient = tk.Label(self.groupMsgClient, text='Message individual client',width=20)
        self.labelMsgClient.pack(side="left")
        
        self.textMsgClient = tk.Entry(self.groupMsgClient, width=40)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textMsgClient.bind('<Return>', whisper)
        self.textMsgClient.pack(side="left"),
        
        self.msgClientBtn = tk.Button(self.groupMsgClient, text='Send to selected client', command = "",)
        self.msgClientBtn.pack(side="left", padx=15)
        
        
        
        # set the focus on the IP and Port text field
        self.ipPort.focus_set()

def clearButtonClick():
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.delete(1.0, tk.END)
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

def clearMsgText():
    g_app.msgText.delete(1.0, tk.END)

def statusButtonClick():
    # forward to the connect handler
    statusHandler(g_app)

def broadcastButtonClick():
    broadcastHandler()

def broadcastHandler():
    data = g_app.textIn.get()
    msg = f"[Server] {data}"
    broadcast(msg)

# the connectHandler toggles the status between connected/disconnected
def statusHandler(master):
    if g_bRunning:
        shutdown()
    else:
        tryToOpen()

# a utility method to print to the message field        
def printToMessages(message):
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

# if attempt to close the window, it is handled here
def on_closing():
    if g_bRunning:
        if tkmsgbox.askokcancel("Quit",
            "Server is running. If you quit the server will be"
            + " shutdown."):
            myQuit()
    else:
        myQuit()

# when quitting, do it the nice way    
def myQuit():
    shutdown()
    g_root.destroy()

# utility address formatting
def myAddrFormat(addr):
    return '{}:{}'.format(addr[0], addr[1])

# disconnect from server (if connected) and
# set the state of the programm to 'disconnected'
def shutdown():
    # we need to modify the following global variables
    global g_bRunning
    global g_sock

    # your code here
    if g_bRunning:
        try:
            g_sock.close()
        except:
            printToMessages("Failed to disconnect")
        else:
            printToMessages("Disconnected from server")
            g_bRunning = False
            
    # once disconnected, set buttons text to 'connect'
    g_app.connectButton['text'] = 'open'

    
# attempt to connect to server    
def tryToOpen():
    # we need to modify the following global variables
    global g_bRunning
    global g_sock
    global listOfSockets

    g_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listOfSockets = [g_sock]
    
    try:
        g_sock.settimeout(0.1)
        addr = int(g_app.ipPort.get())
        g_sock.bind((HOST,addr))
        g_sock.listen(5)
        print(g_sock)
        print(listOfSockets)
    except:
        printToMessages("Failed to connect")
    else:
        printToMessages(f"Server open on port: {addr}")
        g_sock.setblocking(False)
        g_bRunning = True
        g_app.connectButton['text'] = 'shutdown'

# attempt to send the message (in the text field g_app.textIn) to the server
def broadcast(data):

    # your code here
    # a call to g_app.textIn.get() delivers the text field's content
    # if a socket.error occurrs, you may want to disconnect, in order
    # to put the program into a defined state
    try:
        printToMessages(data)
        msg = bytearray(data,"ASCII")
        for c in listOfSockets[1:]:
            c.send(msg)
    except:
        printToMessages("(Failed to send)")
        shutdown()
    else:
        clearMsgText()
        
def whisper():
    try:
        msg = bytearray(g_app.textMsgClient.get(),"ASCII")
        #client = 
        #client.send(msg)
    except:
        printToMessages("A message failed to send")
    else:
        printToMessages

# poll messages
def pollMessages():
    # reschedule the next polling event
    g_root.after(g_pollFreq, pollMessages)
    # your code here
    # use the recv() function in non-blocking mode
    # catch a socket.error exception, indicating that no data is available
    if g_bRunning:
        try:
            tup = select.select(listOfSockets, [], [], 0.0)
            sock = tup[0][0]
            if sock== g_sock:
                try:
                    client, addr = g_sock.accept()
                except:
                    #client not accepter
                    pass
                else:
                    addr = ":".join(map(str,addr))
                    broadcast(f"[{addr}] (connected)")
                    listOfSockets.append(client)
            else:
                try:
                    data = sock.recv(1024).decode()
                    client = sock.getpeername()
                    addr = ":".join(map(str,client))
                    if not data:
                        msg = f"[{addr}] (disconnected)"
                        sock.close()          
                        listOfSockets.remove(sock)
                    else:
                        msg = f"[{addr}] {data}"   
                except socket.error:
                    #no data available
                    pass
                else:
                    broadcast(msg)
        except:
            #nothing happening on socket, sock = error since tup is null
            pass
        


HOST = "localhost"

# by default we are not connected
g_bRunning = False
g_sock = None

# set the delay between two consecutive calls to pollMessages
g_pollFreq = 200 # in milliseconds

# launch the gui
g_root = tk.Tk()
g_app = Application(master=g_root)

# make sure everything is set to the status 'disconnected' at the beginning
shutdown()

# schedule the next call to pollMessages
g_root.after(g_pollFreq, pollMessages)

# if attempt to close the window, handle it in the on-closing method
g_root.protocol("WM_DELETE_WINDOW", on_closing)

# start the main loop
# (which handles the gui and will frequently call pollMessages)
g_app.mainloop()
