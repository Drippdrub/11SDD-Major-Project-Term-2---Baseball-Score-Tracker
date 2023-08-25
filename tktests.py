import tkinter
import customtkinter

app = customtkinter.CTk()

def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

radio_var = tkinter.IntVar(value=0)
wonga = tkinter.IntVar(value=0)
radiobutton_1 = customtkinter.CTkRadioButton(app, text="CTkRadioButton 1",
                                             command=radiobutton_event, variable= radio_var, value=7)
radiobutton_2 = customtkinter.CTkRadioButton(app, text="CTkRadioButton 2",
                                             command=radiobutton_event, variable= radio_var, value=9)
radiobutton_1.pack()
radiobutton_2.pack()

radiobutton_3 = customtkinter.CTkRadioButton(app, text="CTkRadioButton 3",
                                             command=radiobutton_event, variable= wonga, value=7)
radiobutton_4 = customtkinter.CTkRadioButton(app, text="CTkRadioButton 4",
                                             command=radiobutton_event, variable= wonga, value=9)
radiobutton_3.pack()
radiobutton_4.pack()

app.mainloop()