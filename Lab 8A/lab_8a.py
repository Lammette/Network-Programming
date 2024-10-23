
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
        
        self.discAllButton = tk.Button(self.groupClientControl, text='Disconnect All', command = disconnectAll, width= 15)
        self.discAllButton.pack(side="top", pady = 15,padx=15)

        self.discSelButton = tk.Button(self.groupClientControl, text='Disconnect Selected', command = disconnectSel, width= 15)
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
        
        self.msgClientBtn = tk.Button(self.groupMsgClient, text='Send to selected client', command = whisperButton,)
        self.msgClientBtn.pack(side="left", padx=15)
        
        
        
        # set the focus on the IP and Port text field
        self.ipPort.focus_set()
        
#
#   Clear Terminal
#
def clearButtonClick():
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.delete(1.0, tk.END)
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

#
#   Server status handling
#
def statusButtonClick():
    statusHandler(g_app)

def statusHandler(master):
    if g_bRunning:
        shutdown()
    else:
        tryToOpen()
       
#
#   Warning server not running
#
def warningNotRunning():
    tkmsgbox.showwarning("Warning", "Server is not running")


#
#   Print to text box
#        
def printToMessages(message):
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

#
#   Closing stuff
#
def on_closing():
    if g_bRunning:
        if tkmsgbox.askokcancel("Quit",
            "Server is running. If you quit the server will be"
            + " shutdown."):
            myQuit()
    else:
        myQuit()
   
def myQuit():
    shutdown()
    g_root.destroy()

# utility address formatting
def myAddrFormat(addr):
    return '{}:{}'.format(addr[0], addr[1])

#
#   Server Open / Shutdown
#
def shutdown():
    global g_bRunning
    global g_sock

    if g_bRunning:
        try:
            g_sock.close()
        except:
            printToMessages("Failed to shutdown")
        else:
            printToMessages("Server shutdown")
            g_bRunning = False
            updateClientList()
            
    g_app.connectButton['text'] = 'open'

    
def tryToOpen():
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
    except:
        printToMessages("Failed to connect")
    else:
        printToMessages(f"Server opened: {HOST}:{addr}")
        g_sock.setblocking(False)
        g_bRunning = True
        g_app.connectButton['text'] = 'shutdown'
        
    
#
#   Client list stuff
#        
def warningNotSelected():
    tkmsgbox.showwarning("Warning", "No Client selected")
    
def updateClientList():
    clearClientList()
    if g_bRunning:
        for socket in listOfSockets[1:]:
            client = ":".join(map(str,socket.getpeername()))
            g_app.clientList.insert(tk.END,f"[{client}]")
    
def clearClientList():
    g_app.clientList.delete(0,tk.END)
    
def selectClient():
    try:
        for i in g_app.clientList.curselection():
            client = listOfSockets[i+1]
        return client
    except:
        return None

#
#   Client disconnection
#        
def disconnectAll():
    if g_bRunning:
        for client in listOfSockets[1:]:
            disconnectClient(client)
        updateClientList()
    else:
        warningNotRunning()
    
def disconnectSel():
    if g_bRunning:
        disconnectClient(selectClient())
    else:
        warningNotRunning()
    
def disconnectClient(client):
    if client is not None:
        listOfSockets.remove(client)
        client.close()
        updateClientList()
    else:
        warningNotSelected()
        
#
#   Clear 
#
def clearTextIn():
    g_app.textIn.delete(0, tk.END)

def clearMsgClient():
    g_app.textMsgClient.delete(0, tk.END)
        
#
#   Broadcast handling
#
def broadcastButtonClick():
    broadcastHandler(g_app)

def broadcastHandler(master):
    if g_bRunning:
        data = g_app.textIn.get()
        if data:
            msg = f"[Server] {data}"
            broadcast(msg)
            clearTextIn()
    else:
        warningNotRunning()

#
#   Communication stuff
#
def broadcast(data):
    try:
        printToMessages(data)
        msg = bytearray(data,"ASCII")
        for c in listOfSockets[1:]:
            c.send(msg)
    except:
        printToMessages("(Failed to send)")
        shutdown()

def whisperButton():
    whisper(g_app)
        
def whisper(master):
    if g_bRunning:
        client = selectClient()
        if client:
            try:
                data = g_app.textMsgClient.get()
                if data and client:
                    msg = bytearray(f"[Server](whisper) {data}", "ASCII")
                    client.send(msg)
                    clearMsgClient()
            except socket.error:
                printToMessages("A message failed to send")
        else:
            warningNotSelected()
    else:
        warningNotRunning()

#
#   Poll messages
#
def listener():
    # reschedule the next polling event
    g_root.after(g_pollFreq, listener)
    
    if g_bRunning:
        try:
            tup = select.select(listOfSockets, [], [], 0.0)
            if tup[0] != []:
                sock = tup[0][0]
                if sock== g_sock:
                    try:
                        client, addr = g_sock.accept()
                    except:
                        #client not accepted
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
                updateClientList()
        except:
            printToMessages("Error")
            shutdown()
        
HOST = "0.0.0.0"

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
g_root.after(g_pollFreq, listener)

# if attempt to close the window, handle it in the on-closing method
g_root.protocol("WM_DELETE_WINDOW", on_closing)

# start the main loop
# (which handles the gui and will frequently call pollMessages)
g_app.mainloop()
