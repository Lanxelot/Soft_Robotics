import tkinter
import tkinter.messagebox
import customtkinter
import numpy as np
from customtkinter import CTkLabel
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import gpiozero
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
channel = 12
GPIO.setup(channel,GPIO.OUT)
GPIO.output(channel, GPIO.LOW)  
pwm= GPIO.PWM(12,1)      # set RPI_PIN LOW to at the start


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Control Board")
        self.geometry(f"{800}x{480}")


        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.var = customtkinter.IntVar()
        self.check_var = customtkinter.StringVar()

        # create left sidebar frame with widgets
        self.sidebar_frame_left = customtkinter.CTkTabview(self, width=200, corner_radius=0)
        self.sidebar_frame_left.grid_propagate(False)
        self.sidebar_frame_left.add("1")
        self.sidebar_frame_left.add("2")
        self.sidebar_frame_left.add("3")
        self.sidebar_frame_left.grid(row=0, column=0, rowspan=4,pady = (0,10), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self.sidebar_frame_left.tab("1"),fg_color="#36454F", border_width=2,text_color=("gray10", "#DCE4EE"), text="Start") #Start pump
        self.main_button_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_button_2 = customtkinter.CTkButton(master=self.sidebar_frame_left.tab("1"),fg_color="#36454F", border_width=2,text_color=("gray10", "#DCE4EE"), text="Stop") #Stop pump
        self.main_button_2.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.slider_2 = customtkinter.CTkSlider(self.sidebar_frame_left.tab("1"), orientation="vertical",from_=0, to=13, number_of_steps=13)
        self.slider_2.grid(row=4, column=0)
        self.set_button = customtkinter.CTkButton(master=self.sidebar_frame_left.tab("1"), fg_color="#36454F", border_width=2,text_color=("gray10", "#DCE4EE"), text="Set",command=self.set_pressure)  # Stop pump
        self.set_button.grid(row=5, column=0, padx=20, pady=20 )# , sticky="nsew")
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame_left.tab("1"),height=20,width=50)
        self.textbox.place(y = 150,x = 130)      #.place(y=200, x=130)
        self.slider_2.bind(" <B1-Motion>", self.update_textbox)


        # create Right sidebar frame with widgets
        self.man_cont_frame = customtkinter.CTkTabview(self, width=250)
        self.man_cont_frame.grid_propagate(False)
        self.man_cont_frame.grid(row=0, column=2,rowspan = 4,pady = (0,10), sticky="nsew")
        self.man_cont_frame.add("Manual Control")
        self.man_cont_frame.tab("Manual Control").grid_columnconfigure(0, weight=1)
        self.man_cont_frame.add("Automatic control")
        self.man_cont_frame.tab("Automatic control").grid_columnconfigure(0, weight=1)
        
       
        self.switch1 = customtkinter.CTkSwitch(master=self.man_cont_frame.tab("Manual Control"), text=f"Valve {1}",command = self.turn_on_1,variable = self.var)
        self.switch1.grid(row=2, column=0, padx=10, pady=(20, 20))
        self.switch2 = customtkinter.CTkSwitch(master=self.man_cont_frame.tab("Manual Control"), text=f"Valve {2}")
        self.switch2.grid(row=3, column=0, padx=10, pady=(0, 20))
        self.switch3 = customtkinter.CTkSwitch(master=self.man_cont_frame.tab("Manual Control"), text=f"Valve {3}")
        self.switch3.grid(row=4, column=0, padx=10, pady=(0, 20))
        self.switch4 = customtkinter.CTkSwitch(master=self.man_cont_frame.tab("Manual Control"), text=f"Valve {4}")
        self.switch4.grid(row=5, column=0, padx=10, pady=(0, 20))

        self.slider_3 = customtkinter.CTkSlider(self.man_cont_frame.tab("Automatic control"), orientation="vertical", from_=0,to=20, number_of_steps=20)
        self.slider_3.place(y=30, x=30)
        self.slider_4 = customtkinter.CTkSlider(self.man_cont_frame.tab("Automatic control"),orientation="vertical", from_=0, to=100, number_of_steps=100)
        self.slider_4.place(y=30, x=150)
        self.textbox1 = customtkinter.CTkTextbox(self.man_cont_frame.tab("Automatic control"), height=20, width=50)
        self.textbox1.place(y=90, x=60)
        self.textbox2 = customtkinter.CTkTextbox(self.man_cont_frame.tab("Automatic control"), height=20, width=50)
        self.textbox2.place(y=90, x=180)
        #self.checkbox = customtkinter.CTkCheckBox(self.man_cont_frame.tab("Automatic control"), text="CTkCheckBox", command= self.checkbox_event,
        #variable= self.check_var, onvalue="on", offvalue="off")
        #self.checkbox.place(x=30, y=250)
        self.Ti_me = customtkinter.CTkEntry(master=self.man_cont_frame.tab("Automatic control"),placeholder_text="Time",width=100,height=25,border_width=2,corner_radius=10)
        self.Ti_me.place(y=290, x=10)
        self.delay = customtkinter.CTkEntry(master=self.man_cont_frame.tab("Automatic control"),placeholder_text="delay",width=100,height=25,border_width=2,corner_radius=10)
        self.delay.place(y=290, x=120)
        self.start = customtkinter.CTkButton(master=self.man_cont_frame.tab("Automatic control"),width=110,height=25,border_width=0,corner_radius=8,text="Start",command = self.setpwm)
        self.start.place(y=340, x=5)
        self.resume = customtkinter.CTkButton(master=self.man_cont_frame.tab("Automatic control"), width=110, height=25,border_width=0, corner_radius=8, text="Resume")
        self.resume.place(y=340, x=125)
        self.stop = customtkinter.CTkButton(master=self.man_cont_frame.tab("Automatic control"), width=110, height=25,border_width=0, corner_radius=8, text="Stop",command = self.destroy_pwm)
        self.stop.place(y=380, x=5)
        self.pause = customtkinter.CTkButton(master=self.man_cont_frame.tab("Automatic control"), width=110, height=25,border_width=0, corner_radius=8, text="Pause")
        self.pause.place(y=380, x=125)

        self.slider_3.bind(" <B1-Motion>", self.update_textbox1)
        self.slider_4.bind(" <B1-Motion>", self.update_textbox2)
        #Hello






        # create Graph and oscilloscope
        self.graph = customtkinter.CTkTabview(self, width=250)
        self.graph.add("Oscilloscope")
        self.graph.add("Graph")
        self.graph.grid(row=0, column=1, padx=(10, 10),sticky = "ns")
        # self.graph.grid_rowconfigure(0, weight=1)
        # self.graph.grid_rowconfigure(0, weight=1)

        fig_graph = plt.Figure(figsize=(5, 5), dpi=100)
        axis = fig_graph.add_subplot(111)
        # Generate a PWM signal as a list of values between 0 and 1
        pwm_signal = [0, 0, 0, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 0.5, 0, 0, 0]
        # Plot the PWM signal
        axis.plot(pwm_signal)
        canvas = FigureCanvasTkAgg(fig_graph, master=self.graph.tab(("Graph")))
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        #Oscilloscope
        self.fig_osc = Figure()
        self.axis = self.fig_osc.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig_osc, master=self.graph.tab("Oscilloscope"))
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        # initialize data
        self.x_data = np.linspace(0, 2 * np.pi, 200)
        self.y_data = np.sin(self.x_data)
        self.line, = self.axis.plot(self.x_data, self.y_data)

        # start the animation
        self.animation()


        #UI
        self.UI = customtkinter.CTkTabview(self, width=250)
        self.UI.add("System Diagnostics")
        self.UI.add("Save")
        self.UI.add("UI settings")
        self.UI.grid(row=1, column=1, padx=(10, 10), pady = (10,10), sticky="nsew")
        self.appearance_mode_label = customtkinter.CTkLabel(self.UI.tab("UI settings"), text="Appearance Mode:",anchor="e")
        self.appearance_mode_label.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.UI.tab("UI settings"), values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=10, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.UI.tab("UI settings"), text="UI Scaling:", anchor="e")
        self.scaling_label.grid(row=0, column=1, padx=10, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.UI.tab("UI settings"), values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=1, column=1, padx=10, pady=(10, 10))

        # create save button
        self.string_input_button = customtkinter.CTkButton(self.UI.tab("Save"), text="Save",command=self.open_input_dialog_event,width=100)
        self.string_input_button.pack(fill = "both",expand = True)
        


        #System diagnostics
        # Pump diag
        # CMOS diag
        # Valve diag
        # Press Reg diag








    #     # create tabview
    #     self.tabview = customtkinter.CTkTabview(self, width=250)
    #     self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
    #     self.tabview.add("CTkTabview")
    #     self.tabview.add("Tab 2")
    #     self.tabview.add("Save File")
    #     self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
    #     self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
    #     self.tabview.tab("Save File").grid_columnconfigure(0, weight=1)
    #
    #     self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,values=["Value 1", "Value 2", "Value Long Long Long"])
    #     self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
    #     self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),values=["Value 1", "Value 2", "Value Long....."])
    #     self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
    #     self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Save File"), text="Save",command=self.open_input_dialog_event)
    #     self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
    #     self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
    #     self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)
    #

    #
    #
    #
    #     # create slider and progressbar frame
    #     self.Wave_frame = customtkinter.CTkTabview(self)
    #     self.Wave_frame.grid(row=1, column=1,columnspan = 3, padx=(20, 10), pady=(10, 10), sticky="nsew")
    #     self.Wave_frame.add("Square wave")
    #     self.Wave_frame.add("Sine wave")
    #     self.Wave_frame.add("Traingle wave")
    #     self.Wave_frame.add("Pulse wave")
    #     self.Wave_frame.add("Cardiac pattern wave")
    #     self.Wave_frame.add("Gaussian pulse wave")
    #     self.Wave_frame.add("Arbitrary wave")
    #
    #
    #
    #     self.appearance_mode_optionemenu.set("Dark")
    #     self.scaling_optionemenu.set("100%")
    #     self.optionmenu_1.set("CTkOptionmenu")
    #     self.combobox_1.set("CTkComboBox")
    #     # self.slider_1.configure(command=self.progressbar_2.set)
    #     # self.slider_2.configure(command=self.progressbar_3.set)
    #     # self.progressbar_1.configure(mode="indeterminnate")
    #     # self.progressbar_1.start()
    #     # # self.textbox.insert("0.0", "CTkTextbox\n\n" + "This box will be replaced by a graph.\n\n")
    #     # self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
    #     # self.seg_button_1.set("Value 2")
    #
    # def open_input_dialog_event(self):
    #     dialog = customtkinter.CTkInputDialog(text="Save File as:", title="CTkInputDialog")
    #     print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def set_pressure(self):
        value = self.slider_2.get()
        print(value)

    def update_textbox(self, event):
        self.textbox.delete("1.0", customtkinter.END)
        self.textbox.insert(customtkinter.END, "{0}".format(self.slider_2.get()))




    def animation(self):
        # update data
        self.y_data = np.roll(self.y_data, -1)
        self.line.set_ydata(self.y_data)

        # redraw the plot
        self.fig_osc.canvas.draw()

        # repeat after 50 milliseconds
        self.graph.tab("Oscilloscope").after(50, self.animation)


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
        
        
    def turn_on_1(self):
        print(1)
        if self.var.get() == 1:
                GPIO.output(channel,True)
                print("On")
        
        if self.var.get() == 0:
                GPIO.output(channel,False)
                print("Off")
    
    def setpwm(self):
        pwm.start(0)
        
        pwm.ChangeFrequency(int(self.slider_3.get()))
        pwm.ChangeDutyCycle(int(self.slider_4.get())) 

    def destroy_pwm(self):
        pwm.stop()

    def update_textbox1(self,event):
        self.textbox1.delete("1.0", customtkinter.END)
        self.textbox1.insert(customtkinter.END, "{0}".format(self.slider_3.get()))
        pwm.ChangeFrequency(int(self.slider_3.get()))

    def update_textbox2(self,event):
        self.textbox2.delete("1.0", customtkinter.END)
        self.textbox2.insert(customtkinter.END, "{0}".format(self.slider_4.get()))
        pwm.ChangeDutyCycle(int(self.slider_4.get())) 

    def checkbox_event(self):
      pass





if __name__ == "__main__":
    app = App()
    app.mainloop()
