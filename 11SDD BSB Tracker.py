# GUI Libraries
import tkinter as tk
from tkinter import messagebox as msgbox
import customtkinter as ctk
# Image Library
from PIL import Image, ImageTk
# Excel Read/Write Libraries
import xlsxwriter as xl
import openpyxl as openpx

# ctypes used solely for the purpose of imp[orting custom fonts
try:
    from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
    FR_PRIVATE  = 0x10
    FR_NOT_ENUM = 0x20
except ImportError: #for testing on mac, windll does not work on mac, disables the fonts on mac
    pass

global bgClr
bgClr = "#212121" #background colour used for the GUI

# this function loads in fonts from the /fontpath folder, taken from stackoverflow forums.

def loadfont(fontpath, private=True, enumerable=False):
    
    try: #for testing on mac, windll does not work on mac, disables the fonts on mac
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
    except: #for testing on mac, windll does not work on mac, disables the fonts on mac
        pass

# root window class
class Win(ctk.CTk): 

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.geometry("1280x720")
        self.resizable(False, False) #fixed window size
        self.iconbitmap("Assets/ball_icon.ico") #application icon
        self.title("Baseball Scoring System") #window name
        #function allows custom fonts to be used
        loadfont("fonts/Airstrike Academy.ttf")
        loadfont("fonts/Venus Plant.ttf")
        loadfont("fonts/Metropolis-Regular.otf")
        #loading all fonts to be used in the GUI
        self.fontH1 = ctk.CTkFont(family="Airstrike Academy", size=72)
        self.fontH2 = ctk.CTkFont(family="Venus Plant", size=32)
        self.fontB1 = ctk.CTkFont(family="Franklin Gothic", size=18)
        self.fontB2 = ctk.CTkFont(family="Cooper Black", size=24)
        self.fontB3 = ctk.CTkFont(family="Metropolis", size=15)
        self.fontB4 = ctk.CTkFont(family="Metropolis", size=13)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue") #theme of window
        app = ctk.CTkFrame(self, fg_color=bgClr) #first frame, fills root window, parent of all other frames/screens
        app.pack(side="top", fill="both", expand=True)
        app.grid_rowconfigure(0, weight=1)
        app.grid_columnconfigure(0, weight=1)

        # packs all frames/screens to app frame
        self.frames = {}
        for F in (StartScreen, Lineups, Settings, GameScore):
            page_name = F.__name__
            frame = F(parent=app, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # shows startscreen first (when __init__ runs)
        self.show_frame("StartScreen")
    
    # brings the parsed frame to the top (ie changes the displayed screen)
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    

# main menu screen class
class StartScreen(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        MMFrame = ctk.CTkFrame(self, fg_color=bgClr) #menu frame with Title and Menu Buttons (to the left of Main Menu Screen)
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
            self.quit()

# Team Lineup Input Screen Class
class Lineups(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        global HomeEntries #list of Home Team Player Entry Widgets, used to retrieve Player Names
        HomeEntries = []
        global AwayEntries #list of Away Team Player Entry Widgets, used to retrieve Player Names
        AwayEntries = []
        global Name1Ent #Home Team Name Widget, used to retrieve Home Team Name
        global Name2Ent #Away Team Name Widget, used to retrieve Away Team Name

        tLT1 = ctk.CTkFrame(self, fg_color=bgClr) #Frame, packs Home Team Entries to the left side of the screen
        tLT2 = ctk.CTkFrame(self, fg_color=bgClr) #Frame, packs Away Team Entries to the right side of the screen
        tLMid = ctk.CTkFrame(self, fg_color=bgClr) #Frame, separates the left and right sides of the screen, has change screen button

        tLT1.columnconfigure(0, weight=1) #
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
            HomeEntries.append(P1NameEnt)

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
            AwayEntries.append(P2NameEnt)



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
            global HomeMembers
            HomeMembers = []
            for entry in HomeEntries:
                HomeMembers.append(entry.get())
            global AwayMembers
            AwayMembers = []
            for entry in AwayEntries:
                AwayMembers.append(entry.get())
            global HomeName
            HomeName = Name1Ent.get()
            global AwayName
            AwayName = Name2Ent.get()
            if HomeName=="" or AwayName=="":
                msgbox.showerror(title="Error",
                                     message="The Team Name entry fields are empty.\nPlease check that all fields have been filled in.")
                return
            for member in HomeMembers:
                if member=="":
                    msgbox.showerror(title="Error",
                                     message="One or more entry fields under Team 1 are empty.\nPlease check that all fields have been filled in.")
                    return
            for member in AwayMembers:
                if member=="":
                    msgbox.showerror(title="Error",
                                     message="One or more entry fields under Team 2 are empty.\nPlease check that all fields have been filled in.")
                    return
            print(AwayMembers)
            controller.show_frame("Settings")

class Settings(ctk.CTkFrame):
    
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        settingFrame = ctk.CTkFrame(self)

        fileName = tk.StringVar()

        fileNameLbl = ctk.CTkLabel(settingFrame, text="Excel File Name:")
        fileNameEnt = ctk.CTkEntry(settingFrame, textvariable=fileName)
        fileNameLbl.grid(row=0, column=0, padx=10, pady=10)
        fileNameEnt.grid(row=0, column=1, padx=10, pady=10)
        fileInfoLbl = ctk.CTkLabel(self, text="Game results will be automatically\noutput to an excel worksheet in\nthe directory of this program.")
        fileInfoLbl.place(relx=0.75, rely=0.45)

        global gameLength
        gameLengthLbl = ctk.CTkLabel(settingFrame, text="Select A Game Length:")
        gameLengthLbl.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        gameLength = tk.IntVar(value=0)
        Int7Btn = ctk.CTkRadioButton(settingFrame, text="Softball Game (7 Innings)", variable= gameLength, value=7)
        Int9Btn = ctk.CTkRadioButton(settingFrame, text="Baseball Game (9 Innings)", variable= gameLength, value=9)
        Int7Btn.grid(row=2, column=0, padx=10, pady=10)
        Int9Btn.grid(row=2, column=1, padx=10, pady=10)

        settingButton = ctk.CTkButton(settingFrame, text="Proceed", command=lambda: self.openGamescore(controller, fileNameEnt.get()))
        settingButton.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        settingFrame.pack(expand=True, anchor=tk.CENTER)
    
    def openGamescore(self, controller, fileName):
        if fileName=="":
            msgbox.showerror(title="Error",
                                     message="An excel filename has not been selected.\nPlease check you have given a filename.")
            return
        if gameLength==0:
            return

        xlfile = f"{fileName}.xlsx"
        bsbTrack = xl.Workbook(xlfile)
        playerScores = bsbTrack.add_worksheet()
        bsbTrack.close()

        global table
        global sheet

        table = openpx.load_workbook(xlfile)
        sheet = table.active
        sheet.title = "playerScores"

        for column in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]:
            sheet.column_dimensions[column].width = 15

        tableTemplate = [
            ["Home Team", HomeName, "", "", "", "", "", "Away Team", AwayName, "", "", "", ""],
            ["Player ID", "Player Name", "Runs", "Strikes", "Foul Balls", "Balls", "", "Player ID", "Player Name", "Runs", "Strikes", "Foul Balls", "Balls"],
            [1, "", 0, 0, 0, 0, "", 1, "", 0, 0, 0, 0],
            [2, "", 0, 0, 0, 0, "", 2, "", 0, 0, 0, 0],
            [3, "", 0, 0, 0, 0, "", 3, "", 0, 0, 0, 0],
            [4, "", 0, 0, 0, 0, "", 4, "", 0, 0, 0, 0],
            [5, "", 0, 0, 0, 0, "", 5, "", 0, 0, 0, 0],
            [6, "", 0, 0, 0, 0, "", 6, "", 0, 0, 0, 0],
            [7, "", 0, 0, 0, 0, "", 7, "", 0, 0, 0, 0],
            [8, "", 0, 0, 0, 0, "", 8, "", 0, 0, 0, 0],
            [9, "", 0, 0, 0, 0, "", 9, "", 0, 0, 0, 0],
            ["Team Total", "", "", "", "", "", "", "Team Total", "", "", "", "", ""],
        ]
        for row in tableTemplate:
            sheet.append(row)

        for player in HomeMembers:
            index = HomeMembers.index(player)
            cell = f"B{index+3}"
            sheet[cell] = player
        
        for player in AwayMembers:
            index = AwayMembers.index(player)
            cell = f"I{index+3}"
            sheet[cell] = player

        table.save(xlfile)

        controller.show_frame("GameScore")

        global homeTeamName
        homeTeamName = HomeName
        global awayTeamName
        awayTeamName = AwayName

        BattingTeam.configure(values=[f"Home Team ({homeTeamName})", f"Away Team ({awayTeamName})"], width=200)
        BattingTeam.set(f"Away Team ({awayTeamName})")
        BattingTeam.configure(state="disabled") #setting value of comboBox while disabled will not work
        batText.configure(text=f"Away Team ({awayTeamName})")
        fldText.configure(text=f"Home Team ({homeTeamName})")
        batterEntry.configure(values=AwayMembers)
        batterEntry.set(AwayMembers[0])
        fieldEntry.configure(values=HomeMembers)
        fieldEntry.set(HomeMembers[0])



class GameScore(ctk.CTkFrame):

    def __init__(self, parent, controller):
        global teamSwapNum
        teamSwapNum = 0

        global homeTeamName
        homeTeamName = ""
        global awayTeamName
        awayTeamName = ""

        global BattingTeam
        global batText
        global fldText

        global inningNum
        inningNum = tk.StringVar()
        inningNum.set(1)
        inningNum.trace("w", lambda name, index, mode, inningNum=inningNum: self.innCallback(inningNum, inningOld))
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
                                command=lambda: self.entAdd(inningNum, "inningNum"))
        inningDown = ctk.CTkButton(master=topFrame, image=downArrow, text="",
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.entSub(inningNum, "inningNum"))
        inningUp.grid(row=0, column=2, padx=4, pady=2)
        inningDown.grid(row=1, column=2, pady=2)

        BattingTeamLbl = ctk.CTkLabel(topFrame, text="Current Batting Team: ")
        BattingTeamLbl.grid(row=0, column=3, rowspan=2, padx=15)

        BattingTeam = ctk.CTkComboBox(topFrame, values=[f"Home Team ({homeTeamName})", f"Away Team ({awayTeamName})"],
                                      text_color_disabled="gray84")
        BattingTeam.set(f"Away Team ({awayTeamName})")
        BattingTeam.grid(row=0, column=4, rowspan=2, padx=5)
        BattingTeam.configure(command=lambda e: self.updateTeams(batterEntry, fieldEntry))

        devModeOn = ctk.IntVar(value=0)
        devOptions = ctk.CTkCheckBox(topFrame, text="Enable DevMode?", command=lambda: self.updateDevMode(devOptions, BattingTeam), variable=devModeOn, onvalue=1, offvalue=0)
        # devOptions.grid(row=0, column=7, rowspan=2, padx=15)

        tabview = ctk.CTkTabview(master=self, command=lambda: self.updateTabs())
        tabview.pack(padx=20, pady=5, expand=True, fill=tk.BOTH)

        allTab = tabview.add("All")
        teamTab1 = tabview.add("Home Team")
        teamTab2 = tabview.add("Away Team")
        overviewTab = tabview.add("Game Overview")
        tabview.set("All")

        #All Tab
        AllBat = ctk.CTkFrame(allTab, fg_color=bgClr)
        AllBat.columnconfigure(0, weight=2)
        AllBat.columnconfigure(1, weight=3)
        AllBat.columnconfigure(2, weight=1)
        AllBat.columnconfigure(3, weight=2)
        AllBat.columnconfigure(4, weight=3)
        AllBat.columnconfigure(5, weight=1)
        AllBat.columnconfigure(6, weight=2)
        AllBat.columnconfigure(7, weight=2)
        AllBat.columnconfigure(8, weight=2)
        AllFld = ctk.CTkFrame(allTab, fg_color=bgClr)
        AllFld.columnconfigure(0, weight=2)
        AllFld.columnconfigure(1, weight=3)
        AllFld.columnconfigure(2, weight=1)
        AllFld.columnconfigure(3, weight=2)
        AllFld.columnconfigure(4, weight=3)
        AllFld.columnconfigure(5, weight=1)
        AllFld.columnconfigure(6, weight=2)
        AllFld.columnconfigure(7, weight=2)
        AllFld.columnconfigure(8, weight=2)

        batText = ctk.CTkLabel(AllBat, text=BattingTeam.get(), font=controller.fontB1)
        batText.grid(row=0, column=0, columnspan=9, sticky=tk.W+tk.E,
                    pady=20)
        fldText = ctk.CTkLabel(AllFld, text=f"Fielding Team ({homeTeamName})", font=controller.fontB1)
        fldText.grid(row=0, column=0, columnspan=9, sticky=tk.W+tk.E,
                    pady=20)

        #All Tab Batting Frame
        global batterEntry

        batterName = ctk.CTkLabel(AllBat, text="Batter:", font=controller.fontB3)
        batterEntry = ctk.CTkComboBox(AllBat)
        batterName.grid(row=1, column=0, columnspan=3, sticky=tk.W+tk.E, padx=20, pady=30)
        batterEntry.grid(row=1, column=3, columnspan=3, sticky=tk.W+tk.E, padx=10, pady=30)
        subButton = ctk.CTkButton(AllBat, text="Substitute Batter", font=controller.fontB3, width=100)
        subButton.grid(row=1, column=6, columnspan=3, sticky=tk.W+tk.E, padx=(10, 20), pady=30)

        global runs
        runs = tk.StringVar()
        runs.set(0)
        runs.trace("w", lambda name, index, mode, runs=runs: self.callback(runs, runsOld))
        runsOld = ""

        runText = ctk.CTkLabel(AllBat, text="Runs:", font=controller.fontB3)
        runEntry = ctk.CTkEntry(AllBat, textvariable=runs, width=50)
        runText.grid(row=2, rowspan=2, column=0, sticky=tk.E, padx=10, pady=10)
        runEntry.grid(row=2, rowspan=2, column=1, sticky=tk.W+tk.E, padx=5, pady=10)
        runUp = ctk.CTkButton(master=AllBat, image=upArrow, text="", 
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.entAdd(runs))
        runDown = ctk.CTkButton(master=AllBat, image=downArrow, text="",
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.entSub(runs))
        runUp.grid(row=2, column=2, padx=4, pady=2, sticky=tk.W)
        runDown.grid(row=3, column=2, padx=4, pady=2, sticky=tk.W)

        global strikes
        strikes = tk.StringVar()
        strikes.set(0)
        strikes.trace("w", lambda name, index, mode, strikes=strikes: self.callback(strikes, strikesOld))
        strikesOld = ""

        strikeText = ctk.CTkLabel(AllBat, text="Strikes:", font=controller.fontB3)
        strikeEntry = ctk.CTkEntry(AllBat, textvariable=strikes, width=50)
        strikeText.grid(row=2, rowspan=2, column=3, sticky=tk.E, padx=10, pady=10)
        strikeEntry.grid(row=2, rowspan=2, column=4, sticky=tk.W+tk.E, padx=5, pady=10)
        strikeUp = ctk.CTkButton(master=AllBat, image=upArrow, text="", 
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.entAdd(strikes, "strikes", foulBall))
        strikeDown = ctk.CTkButton(master=AllBat, image=downArrow, text="",
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.entSub(strikes, "strikes"))
        strikeUp.grid(row=2, column=5, padx=4, pady=2, sticky=tk.W)
        strikeDown.grid(row=3, column=5, padx=4, pady=2, sticky=tk.W)

        global foulBall
        foulBall = tk.StringVar()
        foulBall.set(0)
        foulBall.trace("w", lambda name, index, mode, foulBall=foulBall: self.callback(foulBall, foulBallOld))
        foulBallOld = ""

        foulBallText = ctk.CTkLabel(AllBat, text="Foul Balls:", font=controller.fontB3)
        foulBallEntry = ctk.CTkEntry(AllBat, textvariable=foulBall, width=50)
        foulBallText.grid(row=4, rowspan=2, column=0, sticky=tk.E, padx=10, pady=30)
        foulBallEntry.grid(row=4, rowspan=2, column=1, sticky=tk.W+tk.E, padx=5, pady=10)
        foulBallUp = ctk.CTkButton(master=AllBat, image=upArrow, text="", 
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.entAdd(foulBall, "foulBall", strikes))
        foulBallDown = ctk.CTkButton(master=AllBat, image=downArrow, text="",
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.entSub(foulBall, "foulBall"))
        foulBallUp.grid(row=4, column=2, padx=4, pady=3, sticky=tk.W+tk.S)
        foulBallDown.grid(row=5, column=2, padx=4, pady=3, sticky=tk.W+tk.N)

        global battersOut
        battersOut = 0
        global batOutText
        batOutText = ctk.CTkLabel(AllBat, text=f"Batters Out: {battersOut}", font=controller.fontB3)
        batOutText.grid(row=4, rowspan=2, column=3, sticky=tk.E, padx=10, pady=10)
        

        # All Tab Fielding Frame
        global fieldEntry

        fieldName = ctk.CTkLabel(AllFld, text="Pitcher:", font=controller.fontB3)
        fieldEntry = ctk.CTkComboBox(AllFld)
        fieldName.grid(row=1, column=0, columnspan=3, sticky=tk.W+tk.E, padx=20, pady=30)
        fieldEntry.grid(row=1, column=3, columnspan=3, sticky=tk.W+tk.E, padx=20, pady=30)
        blankLbl = ctk.CTkLabel(AllFld, text="", width=145)
        blankLbl.grid(row=1, column=6, columnspan=3, sticky=tk.W+tk.E, padx=20, pady=30)

        global balls
        balls = tk.StringVar()
        balls.set(0)
        balls.trace("w", lambda name, index, mode, balls=balls: self.callback(balls, ballsOld))
        ballsOld = ""

        ballText = ctk.CTkLabel(AllFld, text="Balls:", font=controller.fontB3)
        ballEntry = ctk.CTkEntry(AllFld, textvariable=balls, width=50)
        ballText.grid(row=2, rowspan=2, column=0, sticky=tk.E, padx=10, pady=10)
        ballEntry.grid(row=2, rowspan=2, column=1, sticky=tk.W+tk.E, padx=5, pady=10)
        ballUp = ctk.CTkButton(master=AllFld, image=upArrow, text="", 
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.entAdd(balls))
        ballDown = ctk.CTkButton(master=AllFld, image=downArrow, text="",
                                width=10, height=10, fg_color="#ababab",
                                command=lambda: self.entSub(balls))
        ballUp.grid(row=2, column=2, padx=4, pady=2, sticky=tk.W)
        ballDown.grid(row=3, column=2, padx=4, pady=2, sticky=tk.W)


        AllBat.pack(padx=(10, 5), side=tk.LEFT, fill=tk.BOTH, expand=True)
        AllFld.pack(padx=(5, 10), side=tk.RIGHT, fill=tk.BOTH, expand=True)

        addStatsBtn = ctk.CTkButton(allTab, text="Add Scores to Player", command=lambda: self.addStats())
        addStatsBtn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        #overview Tab
        global overviewFrame
        overviewFrame = ctk.CTkFrame(overviewTab)
        overviewFrame.pack(fill="both", expand=True)

        global overviewTableValues
        overviewTableValues = []
        for x in range(12):
            overviewFrame.columnconfigure(x, weight=1)
            for y in range(13):
                overviewFrame.rowconfigure(y, weight=1)
                if (y==1 and x==0) or (y==8 and x==0):
                    e=ctk.CTkEntry(overviewFrame,
                                font=controller.fontB4, corner_radius=0)
                    e.grid(row=x, column=y, sticky="nsew", columnspan=2)
                elif (y==2 and x==0) or (y==9 and x==0):
                    pass
                else:
                    e=ctk.CTkEntry(overviewFrame,
                                font=controller.fontB4, corner_radius=0)
                    e.grid(row=x, column=y, sticky="nsew")
                overviewTableValues.append(e)
                
        
    
    def innCallback(self, sv, old):
        if sv.get().isdigit() or sv.get == "":
            old = sv.get()
        else:
            sv.set(old)
    
    def callback(self, sv, old):
        if sv.get().isdigit():
            old = sv.get()
        else:
            sv.set(old)

    def entAdd(self, var, *names):
        try:
            global battersOut
            name = names[0]
            var2 = int(names[1].get())
        except:
            name = "none"
            var2 = 0
        if name == "inningNum":
            if int(var.get()) < gameLength.get():
                var.set(int(var.get())+1)
            elif int(var.get()) >= gameLength.get():
                endGame = msgbox.askyesno(title="Finishing Game", message="Do you wish to proceed?\n\nThis will end the game, or move the game into overtime.")
        elif name == "strikes":
            if int(var.get())+var2 < 2:
                var.set(int(var.get())+1)
            elif int(var.get())+var2 >= 2:
                strikeOut = msgbox.askokcancel(title="Batter out", message="The current batter will become out.\nPress cancel to undo.")
                if strikeOut:
                    var.set(int(var.get())+1)
                    battersOut += 1
                    batOutText.configure(text=f"Batters Out: {battersOut}")
                    self.changeBatter()
        elif name == "foulBall":
            if var2==2:
                foulOut = msgbox.askokcancel(title="Batter out", message="The current batter will become out.\nPress cancel to undo.")
                if foulOut:
                    var.set(int(var.get())+1)
                    battersOut += 1
                    batOutText.configure(text=f"Batters Out: {battersOut}")
                    self.changeBatter()
            elif var2==1 and int(var.get())==1:
                foulOut = msgbox.askokcancel(title="Batter out", message="The current batter will become out.\nPress cancel to undo.")
                if foulOut:
                    var.set(int(var.get())+1)
                    battersOut += 1
                    batOutText.configure(text=f"Batters Out: {battersOut}")
                    self.changeBatter()
            else:
                var.set(int(var.get())+1)
        else:
            var.set(int(var.get())+1)

    def entSub(self, var, *names):
        try:
            name = names[0]
        except:
            name = "none"
        if name == "inningNum":
            if int(var.get()) > 1:
                var.set(int(var.get())-1)
        else:
            if int(var.get()) > 0:
                var.set(int(var.get())-1)

    def changeBatter(self):
    
        index = batterEntry.cget("values").index(batterEntry.get())
        playerCell="A1"
        if BattingTeam.get()==f"Away Team ({awayTeamName})":
            for row in range(0, 8):
                if index==row:
                    sheet[f"J{row+3}"] = runs.get()
                    sheet[f"K{row+3}"] = strikes.get()
                    sheet[f"L{row+3}"] = foulBall.get()
                if fieldEntry.cget("values").index(fieldEntry.get())==row:
                    sheet[f"F{row+3}"] = balls.get()
        else:
            for row in range(0, 8):
                if index==row:
                    sheet[f"C{row+3}"] = runs.get()
                    sheet[f"D{row+3}"] = strikes.get()
                    sheet[f"E{row+3}"] = foulBall.get()
                if fieldEntry.cget("values").index(fieldEntry.get())==row:
                    sheet[f"M{row+3}"] = balls.get()
        runs.set(0)
        strikes.set(0)
        foulBall.set(0)
        balls.set(0)

        
        global battersOut
        if battersOut >= 3:
            msgbox.showinfo(title="Swapping Sides", message="Teams will now swap sides.")
            battersOut = 0
            batOutText.configure(text=f"Batters Out: {battersOut}")
            self.swapSides()

        try:
            batterEntry.set(batterEntry.cget("values")[index+1])
        except IndexError:
            batterEntry.set(batterEntry.cget("values")[0])
    
    def swapSides(self):

        BattingTeam.configure(state="normal")
        if BattingTeam.get()==f"Away Team ({awayTeamName})":
            BattingTeam.set(f"Home Team ({homeTeamName})")
        else:
            BattingTeam.set(f"Away Team ({awayTeamName})")
        BattingTeam.configure(state="disabled")
        global teamSwapNum
        teamSwapNum += 1
        if teamSwapNum%2==0:
            self.entAdd(inningNum, "inningNum")
        self.updateTeams(batterEntry, fieldEntry)

    def updateDevMode(self, devOptions, BattingTeam):
        if devOptions.get() == 1:
            BattingTeam.configure(state="normal")
        else:
            BattingTeam.configure(state="disabled")
    
    def updateTabs(self):
        #overviewTab updates
        overviewList = []
        overviewTable = list(sheet.values)
        for row in overviewTable:
            for term in row:
                overviewList.append(term)

        for cell in overviewTableValues:
            index = overviewTableValues.index(cell)
            cell.configure(state="normal")
            cell.delete(0, tk.END)
            cell.insert(1, str(overviewList[index]))
            cell.configure(state="disabled")

    def updateTeams(self, batterName, fieldName):
        batOld=batText.cget("text")
        text=BattingTeam.get()
        if batOld != text:
            batText.configure(text=text)
            fldText.configure(text=batOld)
            if text == f"Home Team ({homeTeamName})":
                batterName.configure(values=HomeMembers)
                batterName.set(HomeMembers[0])
                fieldName.configure(values=AwayMembers)
                fieldName.set(AwayMembers[0])
            else:
                batterName.configure(values=AwayMembers)
                batterName.set(AwayMembers[0])
                fieldName.configure(values=HomeMembers)
                fieldName.set(HomeMembers[0])
    
    def addStats(self):
        self.changeBatter()


app = Win()
app.mainloop()