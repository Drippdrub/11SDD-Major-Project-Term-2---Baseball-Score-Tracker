import tkinter as tk
from tkinter import messagebox as msgbox
import customtkinter as ctk
from PIL import Image, ImageTk
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20
bgClr = "#121212"

def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.

    `private`     if True, other processes cannot see this font, and this
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

    '''
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    # This function is written for Python 2.x. For 3.x, you
    # have to convert the isinstance checks to bytes and str
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)


class Win(ctk.CTk):

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.geometry("1280x720")
        self.resizable(width=False, height=False)
        self.iconbitmap("Assets/ball_icon.ico")
        self.title("Baseball Scoring System")
        loadfont("fontpath\\airstrikeacad.ttf")
        loadfont("fontpath\Venus Plant.ttf")
        self.fontH1 = ctk.CTkFont(family="Airstrike Academy", size=72)
        self.fontH2 = ctk.CTkFont(family="Venus Plant", size=32)
        # fontH3 = 
        self.fontB1 = ctk.CTkFont(family="Franklin Gothic", size=18)
        self.fontB2 = ctk.CTkFont(family="Cooper Black", size=24)

        # initialise window
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        self.bgClr = "#212121"
        app = ctk.CTkFrame(self, fg_color=self.bgClr)
        app.pack(side="top", fill="both", expand=True)
        app.grid_rowconfigure(0, weight=1)
        app.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartScreen, Lineups, GameScore):
            page_name = F.__name__
            frame = F(parent=app, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartScreen")
    
    def show_frame (self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    

# main menu screen
class StartScreen(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        MMFrame = ctk.CTkFrame(self, fg_color=bgClr)
        # title
        MMTitle = ctk.CTkLabel(MMFrame, text="BASEBALL\nSTAT\nTRACKER", font=controller.fontH1, bg_color=bgClr)
        MMTitle.pack(padx=30, pady=30)
        # start button
        MMStart = ctk.CTkButton(MMFrame, height=75, width=375, corner_radius=40, font=controller.fontH2,
                                text="Start Baseball Game", command=lambda: controller.show_frame("Lineups"))
        MMStart.pack(pady=50)
        # exit program button
        MMClose = ctk.CTkButton(MMFrame, height=75, width=375, corner_radius=40, font=controller.fontH2,
                                text="Close Program", command=lambda: self.destroyRequest())
        MMClose.pack(pady=50)

        MMFrame.pack(padx=50, side=tk.LEFT)

        # main menu image
        MMImage = ctk.CTkImage(dark_image=Image.open("Assets/Baseball.png"), size=(400, 400))
        MMImgObj = ctk.CTkLabel(self, image=MMImage, text="")
        MMImgObj.pack(padx=50, side=tk.RIGHT)
    
    # asks user to confirm if they would like to leave
    def destroyRequest(self):
        close = msgbox.askyesno(title="Closing Program", message="Are you sure you want to exit the program?")
        if close == True:
            self.winfo_parent.destroy()


class Lineups(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        T1Members = []
        T2Members = []

        tLT1 = ctk.CTkFrame(self, fg_color=bgClr)
        tLT2 = ctk.CTkFrame(self, fg_color=bgClr)
        tLMid = ctk.CTkFrame(self, fg_color=bgClr)

        tLT1.columnconfigure(0, weight=1)
        tLT1.columnconfigure(1, weight=1)
        tLT1.columnconfigure(2, weight=1)

        T1Text = ctk.CTkLabel(tLT1, text="Home Team", font=controller.fontH2)
        T1Text.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E,
                    pady=10)
        T2Text = ctk.CTkLabel(tLT2, text="Away Team", font=controller.fontH2)
        T2Text.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E,
                    pady=10)


        Name1Lbl = ctk.CTkLabel(tLT1, text="Team Name:", font=controller.fontB2)
        Name1Lbl.grid(row=1, column=0, sticky=tk.E,
                    padx=10, pady=10)
        Name1Ent = ctk.CTkEntry(tLT1, placeholder_text="Home Team", font=controller.fontB1, height=40)
        Name1Ent.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E,
                    padx=40, pady=10)
        for i in range(9):
            PlayerName = ctk.CTkLabel(tLT1, text=f"Player {i+1} Name:", font=controller.fontB2)
            PlayerName.grid(row=i+2, column=0, sticky=tk.E,
                            padx=10, pady=10)
            P1NameEnt = ctk.CTkEntry(tLT1, placeholder_text=f"Player {i+1}", font=controller.fontB1, height=40)
            P1NameEnt.grid(row=i+2, column=1, columnspan=2, sticky=tk.W+tk.E,
                        padx=40, pady=10)
            T1Members.append(P1NameEnt)

        tLT2.columnconfigure(0, weight=1)
        tLT2.columnconfigure(1, weight=1)
        tLT2.columnconfigure(2, weight=1)

        Name2Lbl = ctk.CTkLabel(tLT2, text="Team Name:", font=controller.fontB2)
        Name2Lbl.grid(row=1, column=0, sticky=tk.E,
                    padx=10, pady=10)
        Name2Ent = ctk.CTkEntry(tLT2, placeholder_text="Away Team", font=controller.fontB1, height=40)
        Name2Ent.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E,
                    padx=40, pady=10)
        for i in range(9):
            PlayerName = ctk.CTkLabel(tLT2, text=f"Player {i+1} Name:", font=controller.fontB2)
            PlayerName.grid(row=i+2, column=0, sticky=tk.E,
                            padx=10, pady=10)
            P2NameEnt = ctk.CTkEntry(tLT2, placeholder_text=f"Player {i+1}", font=controller.fontB1, height=40)
            P2NameEnt.grid(row=i+2, column=1, columnspan=2, sticky=tk.W+tk.E,
                        padx=40, pady=10)
            T2Members.append(P2NameEnt)



        tLT1.pack(padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
        tLT2.pack(padx=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tLText = ctk.CTkLabel(tLMid, text="Make sure the players have been ordered into batting order",
                                font=controller.fontB1, wraplength=300, justify=tk.CENTER)
        tLStartGame = ctk.CTkButton(tLMid, text="Start", command=lambda: self.proceedRequest(controller))

        tLText.pack(pady=15, anchor=tk.CENTER)
        tLStartGame.pack(pady=30, anchor=tk.CENTER)
        self.update()
        tLMid.pack(pady=700/2-200, anchor=tk.CENTER)

    def proceedRequest(self, controller):
        self.controller = controller
        proceed = msgbox.askokcancel(title="Confirm Action", message="Do you wish to proceed?\n\nTeam batting orders cannot be changed from this point onward.")
        if proceed:
            controller.show_frame("GameScore")

# set screen frames


class GameScore(ctk.CTkFrame):
    def __init__(self, parent, controller):
        homeTeamName = "Team 1"
        awayTeamName = "Team 2"

        inningNum = tk.StringVar()
        inningNum.set(1)
        inningNum.trace("w", lambda name, index, mode, inningNum=inningNum: self.callback(inningNum, inningOld))
        inningOld = ""
        
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        upArrow = ctk.CTkImage(dark_image=Image.open("Assets/up_arrow.png"), size=(10, 10))
        downArrow = ctk.CTkImage(dark_image=Image.open("Assets/down_arrow.png"), size=(10, 10))

        topFrame = ctk.CTkFrame(master=self)
        topFrame.pack(padx=20, pady=10, fill=tk.X)

        inningLbl = ctk.CTkLabel(master=topFrame, text="Inning:", font=controller.fontB1)
        inningLbl.grid(row=0, column=0, rowspan=2, padx=5)
        inningEnt = ctk.CTkEntry(master=topFrame, font=controller.fontB1, height=40, textvariable=inningNum)
        inningEnt.grid(row=0, column=1, rowspan=2)
        inningUp = ctk.CTkButton(master=topFrame, image=upArrow, text="", 
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.innAdd(inningNum))
        inningDown = ctk.CTkButton(master=topFrame, image=downArrow, text="",
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.innSub(inningNum))
        inningUp.grid(row=0, column=2, padx=4, pady=2)
        inningDown.grid(row=1, column=2, pady=2)

        BattingTeam = ctk.CTkComboBox(topFrame, values=[f"Home Team ({homeTeamName})", f"Away Team ({awayTeamName})"], command=lambda: self.updateText(BattingTeam))
        BattingTeam.set(f"Away Team ({awayTeamName})")
        BattingTeam.configure(state="disabled") #disabling before setting the value of the ComboBox will leave the selected value as blank
        BattingTeam.grid(row=0, column=3, rowspan=2, padx=20)

        devModeOn = ctk.IntVar(value=0)
        devOptions = ctk.CTkCheckBox(topFrame, text="Enable DevMode?", command=lambda: self.updateDevMode(devOptions, BattingTeam), variable=devModeOn, onvalue=1, offvalue=0)
        devOptions.grid(row=0, column=4, rowspan=2, padx=10)

        tabview = ctk.CTkTabview(master=self)
        tabview.pack(padx=20, pady=5, expand=True, fill=tk.BOTH)

        allTab = tabview.add("All")
        teamTab1 = tabview.add("Home Team")
        teamTab2 = tabview.add("Away Team")
        overviewTab = tabview.add("Game Overview")
        tabview.set("All")

        #All Tab
        AllBat = ctk.CTkFrame(allTab, fg_color="#b00b13")
        AllFld = ctk.CTkFrame(allTab, fg_color="#069420")

        batText = ctk.CTkLabel(AllBat, text=BattingTeam.get(), font=controller.fontB1)
        batText.grid(row=0, column=2, columnspan=2, sticky=tk.W+tk.E,
                    pady=10)
        fldText = ctk.CTkLabel(AllFld, text=f"Fielding Team ({homeTeamName})", font=controller.fontB1)
        fldText.grid(row=0, column=2, columnspan=2, sticky=tk.W+tk.E,
                    pady=10)

        #All Tab Team1 Frame


        AllBat.pack(padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
        AllFld.pack(padx=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def callback(self, sv, old):
        if sv.get().isdigit() or sv.get() == "":
            old = sv.get()
        else:
            sv.set(old)

    def innAdd(self, var):
        if int(var.get()) < 9:
            var.set(int(var.get())+1)
        elif int(var.get()) == 9:
            endGame = msgbox.askyesno(title="Finishing Game", message="Do you wish to proceed?\n\nThis will end the game, or move the game into overtime.")

    def innSub(self, var):
        if int(var.get()) > 1:
            var.set(int(var.get())-1)

    def updateDevMode(self, devOptions, BattingTeam):
        if devOptions.get() == 1:
            BattingTeam.configure(state="normal")
        else:
            BattingTeam.configure(state="disabled")

    def updateText(self, BattingTeam):
        text=BattingTeam.get()


app = Win()
app.mainloop()