import tkinter as tk
from tkinter import messagebox as msgbox
import customtkinter as ctk
from PIL import Image, ImageTk

# initialise window
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
bgClr = "#121212"
app = ctk.CTk(fg_color=bgClr)
app.geometry("1280x720")
app.resizable(width=False, height=False)
app.iconbitmap("ball_icon.ico")
app.title("Baseball Scoring System")

# set fonts
fontH1 = ctk.CTkFont(family="Airstrike Academy", size=72)
fontH2 = ctk.CTkFont(family="Venus Plant", size=32)
fontB1 = ctk.CTkFont(family="Franklin Gothic", size=18)
fontB2 = ctk.CTkFont(family="Cooper Black", size=24)

# asks user to confirm if they would like to leave
def destroyRequest():
    close = msgbox.askyesno(title="Closing Program", message="Are you sure you want to exit the program?")
    if close == True:
        app.destroy()

# forgets all loaded frames, then packs the new frame
def changeScreen(screen):
    for widget in app.winfo_children():
        widget.forget()
    screen.pack(fill=tk.BOTH, expand=True)

# set screen frames
mainMenu = ctk.CTkFrame(app, fg_color=bgClr)
teamLineups = ctk.CTkFrame(app, fg_color=bgClr)
gameScreen = ctk.CTkFrame(app, fg_color=bgClr)

# main menu frame
def mainMenuSetup():
    MMFrame = ctk.CTkFrame(mainMenu, fg_color=bgClr)
# title
    MMTitle = ctk.CTkLabel(MMFrame, text="BASEBALL\nSTAT\nTRACKER", font=fontH1, bg_color=bgClr)
    MMTitle.pack(padx=30, pady=30)
# start button
    MMStart = ctk.CTkButton(MMFrame, height=75, width=375, corner_radius=40, font=fontH2,
                            text="Start Baseball Game", command=lambda: changeScreen(teamLineups))
    MMStart.pack(pady=50)
# exit program button
    MMClose = ctk.CTkButton(MMFrame, height=75, width=375, corner_radius=40, font=fontH2,
                            text="Close Program", command=destroyRequest)
    MMClose.pack(pady=50)

    MMFrame.pack(padx=50, side=tk.LEFT)

# main menu image
    MMImage = ctk.CTkImage(dark_image=Image.open("Baseball.png"), size=(400, 400))
    MMImgObj = ctk.CTkLabel(mainMenu, image=MMImage, text="")
    MMImgObj.pack(padx=50, side=tk.RIGHT)

# team info screen
def teamInfoSetup():

    global entries1 
    entries1 = []
    entries2 = []

    tLT1 = ctk.CTkFrame(teamLineups, fg_color=bgClr)
    tLT2 = ctk.CTkFrame(teamLineups, fg_color=bgClr)

    tLT1.columnconfigure(0, weight=1)
    tLT1.columnconfigure(1, weight=1)
    tLT1.columnconfigure(2, weight=1)

    T1Text = ctk.CTkLabel(tLT1, text="Team 1", font=fontH2)
    T1Text.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E,
                pady=15)
    T2Text = ctk.CTkLabel(tLT2, text="Team 2", font=fontH2)
    T2Text.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E,
                pady=15)
    

    Name1Lbl = ctk.CTkLabel(tLT1, text="Team Name:", font=fontB2)
    Name1Lbl.grid(row=1, column=0, sticky=tk.E,
                padx=10, pady=15)
    Name1Ent = ctk.CTkEntry(tLT1, placeholder_text="TEAM 1", font=fontB1, height=50)
    Name1Ent.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E,
                padx=40, pady=15)
    for i in range(6):
        PlayerName = ctk.CTkLabel(tLT1, text=f"Player {i+1} Name:", font=fontB2)
        PlayerName.grid(row=i+2, column=0, sticky=tk.E,
                        padx=10, pady=15)
        P1NameEnt = ctk.CTkEntry(tLT1, placeholder_text=f"Player {i+1}", font=fontB1, height=50)
        P1NameEnt.grid(row=i+2, column=1, columnspan=2, sticky=tk.W+tk.E,
                    padx=40, pady=15)
        entries1.append(P1NameEnt)

    tLT2.columnconfigure(0, weight=1)
    tLT2.columnconfigure(1, weight=1)
    tLT2.columnconfigure(2, weight=1)

    Name2Lbl = ctk.CTkLabel(tLT2, text="Team Name:", font=fontB2)
    Name2Lbl.grid(row=1, column=0, sticky=tk.E,
                padx=10, pady=15)
    Name2Ent = ctk.CTkEntry(tLT2, placeholder_text="TEAM 2", font=fontB1, height=50)
    Name2Ent.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E,
                padx=40, pady=15)
    for i in range(6):
        PlayerName = ctk.CTkLabel(tLT2, text=f"Player {i+1} Name:", font=fontB2)
        PlayerName.grid(row=i+2, column=0, sticky=tk.E,
                        padx=10, pady=15)
        P2NameEnt = ctk.CTkEntry(tLT2, placeholder_text=f"Player {i+1}", font=fontB1, height=50)
        P2NameEnt.grid(row=i+2, column=1, columnspan=2, sticky=tk.W+tk.E,
                    padx=40, pady=15)
        entries2.append(P2NameEnt)



    tLT1.pack(padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
    tLT2.pack(padx=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)

    tLStartGame = ctk.CTkButton(teamLineups, text="Start", command=lambda: changeScreen(gameScreen))
    tLStartGame.pack(pady=(app.winfo_height()/2 - 150), anchor=tk.CENTER)



mainMenuSetup()
teamInfoSetup()

def test():
    testStr = ""
    for entry in entries1:
        testStr = testStr + entry.get() + "   "
    testLbl = ctk.CTkLabel(gameScreen, text=testStr, font=fontH1)
    testLbl.pack(padx=30, pady=30)

testBtn = ctk.CTkButton(gameScreen, text="Press", command=test)
testBtn.pack()

changeScreen(mainMenu)
app.mainloop()