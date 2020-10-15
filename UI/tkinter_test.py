import tkinter 

# CHAT ROOM 
window = tkinter.Tk()
window.minsize(1000, 600)
window.title("Chatroom")
window['bg'] = '#C9DFE3'
window.resizable(width = False, height = False)

labelHead = tkinter.Label(window, bg = "#C9DFE3", fg = "#000000", text = "insert username here", font = "Helvetica 13 bold", pady = 5) 
labelHead.place(relwidth = 1) 
line = tkinter.Label(window, width = 450, bg = "#C9DFE3") 
line.place(relwidth = 1, rely = 0.07, relheight = 0.012) 
          
textCons = tkinter.Text(window, width = 20,  height = 2, bg = "#C9DFE3", fg = "#000000", font = "Helvetica 14",  padx = 5, pady = 5) 
textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08) 
labelBottom = tkinter.Label(window, bg = "#EAECEE", height = 80) 
labelBottom.place(relwidth = 1, rely = 0.825) 

entryMsg = tkinter.Entry(labelBottom, bg = "#C9DFE3", fg = "#000000", font = "Helvetica 13") 
          
        # place the given widget 
        # into the gui window 
entryMsg.place(relwidth = 0.74, relheight = 0.06, rely = 0.008, relx = 0.011) 
          
entryMsg.focus() 
          
#TODO: send button, add listener (replace self.sendButton)
buttonMsg = tkinter.Button(labelBottom, text = "Send", font = "Helvetica 10 bold",  width = 20, bg = "#C9DFE3", command = lambda : self.sendButton(self.entryMsg.get())) 
buttonMsg.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22) 
          
textCons.config(cursor = "arrow") 
          
        # create a scroll bar 
scrollbar = tkinter.Scrollbar(textCons) 
          
        # place the scroll bar  
        # into the gui window 
scrollbar.place(relheight = 1, relx = 0.974) 
          
scrollbar.config(command = textCons.yview) 
          
textCons.config(state = tkinter.DISABLED) 







# LOGIN UI
login = tkinter.Toplevel()
login.title("Login")
login.configure(width = 400, height = 400)
login['bg'] = '#C9DFE3'

img_path = "LoginDoodle.png"

welcome = tkinter.Label(login, text = "Welcome to Accord Secure Chat Room", justify = tkinter.CENTER,  font = "Helvetica 16 bold") 
welcome.place(relwidth = 0.7, relheight = 0.15, relx = 0.2, rely = 0.07) 
welcome['bg'] = '#C9DFE3'

instr = tkinter.Label(login, text = "Please login to continue", justify = tkinter.CENTER,  font = "Helvetica 14 bold") 
instr['bg'] = '#C9DFE3'
instr.place(relwidth = 0.7, relheight = 0.15, relx = 0.2, rely = 0.22) 

labelName = tkinter.Label(login, text = "Username: ", font = "Helvetica 12")           
labelName.place(relheight = 0.45, relx = 0.1, rely = 0.2) 
labelName['bg'] = '#C9DFE3'

# TODO: type in user name here
entryName = tkinter.Entry(login, font = "Helvetica 14")        
entryName.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.35) 
entryName.focus() 
          
#TODO: continue button, add listener (replace self.entryName)
go = tkinter.Button(login, text = "continue", font = "Helvetica 14 bold", command = lambda: self.goAhead(self.entryName.get())) 
go.place(relx = 0.4, rely = 0.55) 

#TODO: insert at bottom of login page







# generates both UI screens currently
window.mainloop()