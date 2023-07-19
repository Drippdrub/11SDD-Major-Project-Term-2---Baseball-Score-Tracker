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
app.iconbitmap("Assets/ball_icon.ico")
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

# main menu screen
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
    MMImage = ctk.CTkImage(dark_image=Image.open("Assets/Baseball.png"), size=(400, 400))
    MMImgObj = ctk.CTkLabel(mainMenu, image=MMImage, text="")
    MMImgObj.pack(padx=50, side=tk.RIGHT)

# team info screen
def proceedRequest(name1, name2):
    proceed = msgbox.askokcancel(title="Confirm Action", message="Do you wish to proceed?\n\nTeam batting orders cannot be changed from this point onward.")
    if proceed:
        homeName = name1.get()
        awayName = name2.get()
        gamescoreSetup(homeName, awayName)
        changeScreen(gameScreen)

def teamInfoSetup():

    global T1Members
    global T2Members
    T1Members = []
    T2Members = []

    tLT1 = ctk.CTkFrame(teamLineups, fg_color=bgClr)
    tLT2 = ctk.CTkFrame(teamLineups, fg_color=bgClr)
    tLMid = ctk.CTkFrame(teamLineups, fg_color=bgClr)

    tLT1.columnconfigure(0, weight=1)
    tLT1.columnconfigure(1, weight=1)
    tLT1.columnconfigure(2, weight=1)

    T1Text = ctk.CTkLabel(tLT1, text="Home Team", font=fontH2)
    T1Text.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E,
                pady=10)
    T2Text = ctk.CTkLabel(tLT2, text="Away Team", font=fontH2)
    T2Text.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E,
                pady=10)
    

    Name1Lbl = ctk.CTkLabel(tLT1, text="Team Name:", font=fontB2)
    Name1Lbl.grid(row=1, column=0, sticky=tk.E,
                padx=10, pady=10)
    Name1Ent = ctk.CTkEntry(tLT1, placeholder_text="Home Team", font=fontB1, height=40)
    Name1Ent.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E,
                padx=40, pady=10)
    for i in range(9):
        PlayerName = ctk.CTkLabel(tLT1, text=f"Player {i+1} Name:", font=fontB2)
        PlayerName.grid(row=i+2, column=0, sticky=tk.E,
                        padx=10, pady=10)
        P1NameEnt = ctk.CTkEntry(tLT1, placeholder_text=f"Player {i+1}", font=fontB1, height=40)
        P1NameEnt.grid(row=i+2, column=1, columnspan=2, sticky=tk.W+tk.E,
                    padx=40, pady=10)
        T1Members.append(P1NameEnt)

    tLT2.columnconfigure(0, weight=1)
    tLT2.columnconfigure(1, weight=1)
    tLT2.columnconfigure(2, weight=1)

    Name2Lbl = ctk.CTkLabel(tLT2, text="Team Name:", font=fontB2)
    Name2Lbl.grid(row=1, column=0, sticky=tk.E,
                padx=10, pady=10)
    Name2Ent = ctk.CTkEntry(tLT2, placeholder_text="Away Team", font=fontB1, height=40)
    Name2Ent.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E,
                padx=40, pady=10)
    for i in range(9):
        PlayerName = ctk.CTkLabel(tLT2, text=f"Player {i+1} Name:", font=fontB2)
        PlayerName.grid(row=i+2, column=0, sticky=tk.E,
                        padx=10, pady=10)
        P2NameEnt = ctk.CTkEntry(tLT2, placeholder_text=f"Player {i+1}", font=fontB1, height=40)
        P2NameEnt.grid(row=i+2, column=1, columnspan=2, sticky=tk.W+tk.E,
                    padx=40, pady=10)
        T2Members.append(P2NameEnt)



    tLT1.pack(padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
    tLT2.pack(padx=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)

    tLText = ctk.CTkLabel(tLMid, text="Make sure the players have been ordered into batting order",
                          font=fontB1, wraplength=300, justify=tk.CENTER)
    tLStartGame = ctk.CTkButton(tLMid, text="Start", command=lambda: proceedRequest(Name1Ent, Name2Ent))

    tLText.pack(pady=15, anchor=tk.CENTER)
    tLStartGame.pack(pady=30, anchor=tk.CENTER)
    teamLineups.update()
    tLMid.pack(pady=app.winfo_height()/2-200, anchor=tk.CENTER)

# scoring system screen

inningNum = tk.StringVar()
inningNum.set(1)
inningNum.trace("w", lambda name, index, mode, inningNum=inningNum: callback(inningNum))
inningOld = ""

def callback(sv):
    global inningNum
    global inningOld
    if sv.get().isdigit() or sv.get() == "":
        inningOld = inningNum.get()
    else:
        inningNum.set(inningOld)

def innAdd(var):
    if int(var.get()) < 9:
        var.set(int(var.get())+1)
    elif int(var.get()) == 9:
        endGame = msgbox.askyesno(title="Finishing Game", message="Do you wish to proceed?\n\nThis will end the game, or move the game into overtime.")

def innSub(var):
    if int(var.get()) > 1:
        var.set(int(var.get())-1)

def updateDevMode(devToggle, battingTeam):
    if devToggle.get() == 1:
        battingTeam.configure(state="normal")
    else:
        battingTeam.configure(state="disabled")


def gamescoreSetup(homeTeamName, awayTeamName):
    print(f"{homeTeamName} vs {awayTeamName}")

    upArrow = ctk.CTkImage(dark_image=Image.open("Assets/up_arrow.png"), size=(10, 10))
    downArrow = ctk.CTkImage(dark_image=Image.open("Assets/down_arrow.png"), size=(10, 10))

    topFrame = ctk.CTkFrame(master=gameScreen)
    topFrame.pack(padx=20, pady=10, fill=tk.X)

    inningLbl = ctk.CTkLabel(master=topFrame, text="Inning:", font=fontB1)
    inningLbl.grid(row=0, column=0, rowspan=2, padx=5)
    inningEnt = ctk.CTkEntry(master=topFrame, font=fontB1, height=40, textvariable=inningNum)
    inningEnt.grid(row=0, column=1, rowspan=2)
    inningUp = ctk.CTkButton(master=topFrame, image=upArrow, text="", 
                             width=10, height=10, fg_color="#ababab",
                             command=lambda: innAdd(inningNum))
    inningDown = ctk.CTkButton(master=topFrame, image=downArrow, text="",
                               width=10, height=10, fg_color="#ababab",
                               command=lambda: innSub(inningNum))
    inningUp.grid(row=0, column=2, padx=4, pady=2)
    inningDown.grid(row=1, column=2, pady=2)

    BattingTeam = ctk.CTkComboBox(topFrame, values=[f"Home Team ({homeTeamName})", f"Away Team ({awayTeamName})"],
                                  state="disabled")
    BattingTeam.grid(row=0, column=3, rowspan=2, padx=20)

    devModeOn = ctk.IntVar(value=0)
    devOptions = ctk.CTkCheckBox(topFrame, text="Enable DevMode?", command=lambda: updateDevMode(devOptions, BattingTeam), variable=devModeOn, onvalue=1, offvalue=0)
    devOptions.grid(row=0, column=4, rowspan=2, padx=10)

    tabview = ctk.CTkTabview(master=gameScreen)
    tabview.pack(padx=20, pady=5, expand=True, fill=tk.BOTH)

    global allTab 
    allTab = tabview.add("All")
    teamTab1 = tabview.add("Home Team")
    teamTab2 = tabview.add("Away Team")
    overviewTab = tabview.add("Game Overview")
    tabview.set("All")

    #All Tab
    AllT1 = ctk.CTkFrame(allTab, fg_color="#b00b13")
    AllT2 = ctk.CTkFrame(allTab, fg_color="#069420")

    T1Text = ctk.CTkLabel(AllT1, text="Home Team", font=fontB1)
    T1Text.grid(row=0, column=2, columnspan=2, sticky=tk.W+tk.E,
                pady=10)
    T2Text = ctk.CTkLabel(AllT2, text="Away Team", font=fontB1)
    T2Text.grid(row=0, column=2, columnspan=2, sticky=tk.W+tk.E,
                pady=10)
    
    #All Tab Team1 Frame
    

    AllT1.pack(padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
    AllT2.pack(padx=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)


mainMenuSetup()
teamInfoSetup()

changeScreen(mainMenu)
app.mainloop()