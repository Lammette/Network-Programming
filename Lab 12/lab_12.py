import firebase_admin
from firebase_admin import db
import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt

cred = firebase_admin.credentials.Certificate(r'lab 12\lab_12_key.json')
firebase_admin.initialize_app(cred, {'databaseURL':"https://np-12-634ef-default-rtdb.europe-west1.firebasedatabase.app/"})
ref = firebase_admin.db.reference('/')

def handleMessage(message):
    try:
        name, msg= message.get('name'), message.get('text')
    except:
        print("recv error")
    else:
        printToMessages(f"{name}: {msg}")

def streamHandler(incomingData):
    if incomingData.event_type == 'put':
        if incomingData.path == '/':
        # This is the very first reading just after subscription:
        # we get all messages or None (if no messages exists).
            if incomingData.data != None:
                for key in incomingData.data:
                    message = incomingData.data[key]
                    handleMessage(message)
        else:
            # Not the first reading.
            # Someone wrote a new message that we just got.
            message = incomingData.data
            handleMessage(message)

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
        self.groupCon.pack(side="top")
        #
        self.ipPortLbl = tk.Label(self.groupCon, text='Name', padx=10)
        self.ipPortLbl.pack(side="left")
        #
        self.name = tk.Entry(self.groupCon, width=20)
        self.name.insert(tk.END, '')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.name.bind('<Return>', nameHandler)
        self.name.pack(side="left")

        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=15, width=42,
            state=tk.DISABLED)
        self.msgText.pack(side="top")

        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupSend, text='message', padx=10)
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', sendMessage)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")
        #
        self.sendButton = tk.Button(self.groupSend, text = 'send',
            command = sendButtonClick)
        self.sendButton.pack(side="left")
        
        # set the focus on the IP and Port text field
        self.name.focus_set()

def sendButtonClick():
    # forward to the sendMessage method
    sendMessage(g_app)

# the connectHandler toggles the status between connected/disconnected
def nameHandler(master):
    global g_name
    name = g_app.name.get()
    if name != "":
        g_name = name
    else:
        g_name = None
        tkmsgbox.showwarning("Warning", "Invalid name")

# a utility method to print to the message field        
def printToMessages(message):
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)


# when quitting, do it the nice way    
def myQuit():
    g_root.destroy()

# utility address formatting
def myAddrFormat(addr):
    return '{}:{}'.format(addr[0], addr[1])
    

# attempt to send the message (in the text field g_app.textIn) to the server
def sendMessage(master):

    # your code here
    # a call to g_app.textIn.get() delivers the text field's content
    # if a socket.error occurrs, you may want to disconnect, in order
    # to put the program into a defined state
    msg = g_app.textIn.get()
    nameHandler(master)
    if g_name != None:
        if msg:
            try:
                msg = {'name': g_name, 'text':g_app.textIn.get()}
                ref.child('messages').push(msg)
            except:
                printToMessages("Message ERROR")
                #diconnect




# by default we are not connected
g_name = None

# launch the gui
g_root = tk.Tk()
g_app = Application(master=g_root)

messages_stream = ref.child('messages').listen(streamHandler)

# start the main loop
g_app.mainloop()
