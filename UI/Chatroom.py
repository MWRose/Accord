import tkinter

class Chatroom:
    def __init__(self, username):
        # main window
        bg_color = "#C9DFE3"

        self.window = tkinter.Tk()
        self.window.minsize(1000, 600)
        self.window.title("Chatroom")
        self.window['bg'] = '#C9DFE3'
        self.window.resizable(width = False, height = False)

        self.labelHead = tkinter.Label(self.window, bg = bg_color, fg = "#000000", text = username, font = "Helvetica 13 bold", pady = 5) 
        self.labelHead.place(relwidth = 1) 
        self.line = tkinter.Label(self.window, width = 450, bg = bg_color) 
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012) 
                
        self.textCons = tkinter.Text(self.window, width = 20,  height = 2, bg = bg_color, fg = "#000000", font = "Helvetica 14",  padx = 5, pady = 5) 
        self.textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08) 
        self.labelBottom = tkinter.Label(self.window, bg = "#EAECEE", height = 80) 
        self.labelBottom.place(relwidth = 1, rely = 0.825) 

        self.entryMsg = tkinter.Entry(self.labelBottom, bg = bg_color, fg = "#000000", font = "Helvetica 13") 
        self.entryMsg.place(relwidth = 0.74, relheight = 0.06, rely = 0.008, relx = 0.011) 
                
        self.entryMsg.focus() 
                
        # send message button
        self.buttonMsg = tkinter.Button(self.labelBottom, text = "Send", font = "Helvetica 10 bold",  width = 20, bg = bg_color, command = lambda : self.send_button(self.entryMsg.get())) 
        self.buttonMsg.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22) 
                
        self.textCons.config(cursor = "arrow") 
                
        # scroll bar for chat
        self.scrollbar = tkinter.Scrollbar(self.textCons) 
        self.scrollbar.place(relheight = 1, relx = 0.974)   
        self.scrollbar.config(command = self.textCons.yview)             
        self.textCons.config(state = tkinter.DISABLED) 

        self.window.mainloop()

    # TODO: handle send 
    def send_button(self, entryMsg):
        print("Message content", entryMsg)

chatroom = Chatroom("user1")