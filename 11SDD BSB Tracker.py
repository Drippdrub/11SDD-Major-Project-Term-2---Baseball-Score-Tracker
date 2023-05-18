import tkinter as tk
from tkinter import messagebox as msgbox
import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

bgClr = "#121212"

# initialise window
app = ctk.CTk(fg_color=bgClr)
app.geometry("1280x720")
app.resizable(width=False, height=False)
app.iconbitmap("ball_icon.ico")

# set fonts
fontH1 = ctk.CTkFont(family="Airstrike Academy", size=72)
fontH2 = ctk.CTkFont(family="Venus Plant", size=32)
fontB1 = ctk.CTkFont(family="Franklin Gothic", size=18)
fontB2 = ctk.CTkFont(family="Cambria", size=18)

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





# main menu frame
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
tLT1 = ctk.CTkFrame(teamLineups, fg_color="#b00b13")
tLT2 = ctk.CTkFrame(teamLineups, fg_color="#4cab42")

tLT1.columnconfigure(0, weight=1)
tLT1.columnconfigure(1, weight=1)
tLT1.columnconfigure(2, weight=1)

T1Text = ctk.CTkLabel(tLT1, text="Team 1", font=fontH2)
T1Text.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E)

T1NameLabel = ctk.CTkLabel(tLT1, text="Team Name:", font=fontB2)
T1NameLabel.grid(row=1, column=0, sticky=tk.W+tk.E, padx=10)

T1Name = ctk.CTkEntry(tLT1, placeholder_text="TEAM 1", font=fontB1, height=50)
T1Name.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E, padx=10)

T2Text = ctk.CTkLabel(tLT2, text="Team 2", font=fontH2)
T2Text.pack()

T2Name = ctk.CTkEntry(tLT2, placeholder_text="TEAM 2", font=fontB1, width=350, height=50)
T2Name.pack()

tLT1.pack(padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
tLT2.pack(padx=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)

changeScreen(mainMenu)
app.mainloop()