from tkinter import *

# create window
root = Tk()
root.title("NextTrain Software")

#create frame
frame = LabelFrame(root,padx=50,pady=20)
frame.pack(padx=10,pady=10)

frame2 = LabelFrame(root,padx=50,pady=20)
departInput = Entry(frame2)
#def for enter data function
def enterData():
    # x is what user inputs
    x = e.get()
    line = ""
    # get line here
    if x.lower() == "all":
        # honestly not sure what to do here
        line = "All lines"
    elif int(x) > 0:
        # loop through all changes here
        line = "line " + x
    # add lines to lines string with a "\n" in between
    # get output lines to user her/e
    linesLabel = Label(frame2,text=line + " Selected")
    # input for depart times
    departLabel = Label(frame2,text="Input departure Time(eg 13:30):")
    global departInput
    departInput = Entry(frame2, width = 25, borderwidth = 2)
    departButton = Button(frame2, text = "Submit", command = SendToDatabase)
    # output to screen
    frame2.pack(padx=10,pady=10)
    linesLabel.grid(row=0, column=0)
    departLabel.grid(row=1, column=0)
    departInput.grid(row=2, column=0)
    departButton.grid(row=2, column=1)
    frame.pack_forget()

def SendToDatabase():
    # gets user inputted value
    print(departInput.get())
    # TODO: code to connect datacritical

# creating widgets
title = Label(frame, text="NEXTTRAIN")
myLabel1 = Label(frame, text="Please Enter Line or Enter 'ALL' for all:")
inputBTN = Button(frame, text="Enter", command = enterData)
quitBTN = Button(frame, text = "Quit", command = root.quit)
e = Entry(frame, width = 25, borderwidth = 2)
# output to screen
title.grid(row=0, column=0)
myLabel1.grid(row=1, column=0)
e.grid(row=2, column=0)
inputBTN.grid(row=2, column=1)
quitBTN.grid(row=10,column=0)

# loop for UI
root.mainloop()
