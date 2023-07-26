import tkinter as tk
import pyglet, os

pyglet.font.add_file('Airstrike Academy.ttf')  # Your TTF file name here

root = tk.Tk()
MyLabel = tk.Label(root,text="test",font=('Airstrike Academy',25)) 

MyLabel.pack()
root.mainloop()