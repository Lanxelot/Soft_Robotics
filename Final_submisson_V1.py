import tkinter as tk
import tkinter.messagebox
import customtkinter
import numpy as np
from customtkinter import CTkLabel
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ADCDACPi import ADCDACPi
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
channel = 12     
GPIO.setup(channel,GPIO.OUT)
GPIO.output(channel, GPIO.LOW)        # set RPI_PIN LOW to at the start
pwm = GPIO.PWM(12,1)
GPIO.setup(8,GPIO.OUT)
GPIO.output(8, GPIO.LOW) 
GPIO.setup(10,GPIO.OUT)
GPIO.output(10, GPIO.LOW) 
GPIO.setup(11,GPIO.OUT)
GPIO.output(11, GPIO.LOW) 


in1 = 18
in2 = 16
en = 22
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,500)
adcdac = ADCDACPi(2)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, False)


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
adcdac = ADCDACPi(2)
adcdac.set_adc_refvoltage(3.3)


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
        self.tF = 0
        self.var = customtkinter.IntVar()
        self.var1 = customtkinter.IntVar()
        self.var2 = customtkinter.IntVar()
        self.var3 = customtkinter.IntVar()
        self.pat_flag=0

        # create left sidebar frame with widgets
        self.sidebar_frame_left = customtkinter.CTkTabview(self, width=200, corner_radius=0)
        self.sidebar_frame_left.grid_propagate(False)
        self.sidebar_frame_left.add("Motor Cont")
        self.sidebar_frame_left.add("Pres Cont")
        self.sidebar_frame_left.grid(row=0, column=0, rowspan=4,pady = (0,10), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self.sidebar_frame_left.tab("Motor Cont"),fg_color="#36454F", border_width=2,text_color=("gray10", "#DCE4EE"), text="Start",command = self.start_motor) #Start pump
        self.main_button_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_button_2 = customtkinter.CTkButton(master=self.sidebar_frame_left.tab("Motor Cont"),fg_color="#36454F", border_width=2,text_color=("gray10", "#DCE4EE"), text="Stop",command = self.stop_motor) #Stop pump
        self.main_button_2.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.slider_2 = customtkinter.CTkSlider(self.sidebar_frame_left.tab("Motor Cont"), orientation="vertical",from_=0, to=100, number_of_steps=10)
        self.slider_2.grid(row=3, column=0)
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame_left.tab("Motor Cont"),height=20,width=50)
        self.textbox.place(y = 150,x = 130)      #.place(y=200, x=130)
        self.Pressure_val = customtkinter.CTkSlider(self.sidebar_frame_left.tab("Pres Cont"), orientation="vertical",from_=0, to=13, number_of_steps=13)
        self.Pressure_val.place(y = 100,x = 100)  
        self.Pressure_val.set(0)
        self.Press_textbox = customtkinter.CTkTextbox(self.sidebar_frame_left.tab("Pres Cont"),height=20,width=50)
        self.Press_textbox.place(y = 100,x = 130)      #.place(y=200, x=130)
        self.Pressure_val.bind(" <B1-Motion>", self.update_textbox5)
        self.slider_2.bind(" <B1-Motion>", self.update_textbox)
        self.slider_2.set(30)


        # create Right sidebar frame with widgets
        self.man_cont_frame = customtkinter.CTkTabview(self, width=250)
        self.man_cont_frame.grid_propagate(False)
        self.man_cont_frame.grid(row=0, column=2,rowspan = 4,pady = (0,10), sticky="nsew")
        self.man_cont_frame.add("Manual Control")
        self.man_cont_frame.tab("Manual Control").grid_columnconfigure(0, weight=1)
        self.man_cont_frame.add("Automatic control")
        self.man_cont_frame.tab("Automatic control").grid_columnconfigure(0, weight=1)
        self.man_cont_frame.add("Time and Delay")
        self.man_cont_frame.tab("Time and Delay").grid_columnconfigure(0, weight=1)

        self.switch1 = customtkinter.CTkSwitch(master=self.man_cont_frame.tab("Manual Control"), text=f"Valve {1}",command = self.turn_on_1,variable = self.var)
        self.switch1.grid(row=2, column=0, padx=10, pady=(20, 20))
        self.switch2 = customtkinter.CTkSwitch(master=self.man_cont_frame.tab("Manual Control"), text=f"Valve {2}",command = self.turn_on_2,variable = self.var1)
        self.switch2.grid(row=3, column=0, padx=10, pady=(0, 20))
        self.switch3 = customtkinter.CTkSwitch(master=self.man_cont_frame.tab("Manual Control"), text=f"Valve {3}",command = self.turn_on_3,variable = self.var2)
        self.switch3.grid(row=4, column=0, padx=10, pady=(0, 20))
        self.switch4 = customtkinter.CTkSwitch(master=self.man_cont_frame.tab("Manual Control"), text=f"Valve {4}",command = self.turn_on_4,variable = self.var3)
        self.switch4.grid(row=5, column=0, padx=10, pady=(0, 20))
        self.pattern1 = customtkinter.CTkButton(master=self.man_cont_frame.tab("Manual Control"),width=110,height=25,border_width=0,corner_radius=8,text="pattern1",command=self.Pat_123)
        self.pattern1.place(y=240, x=5)
        self.pattern2 = customtkinter.CTkButton(master=self.man_cont_frame.tab("Manual Control"), width=110, height=25,border_width=0, corner_radius=8, text="pattern2",command=self.Pat12_34)
        self.pattern2.place(y=240, x=125)
        self.pattern3 = customtkinter.CTkButton(master=self.man_cont_frame.tab("Manual Control"), width=110, height=25,border_width=0, corner_radius=8, text="pattern3",command=self.Pat14_23)
        self.pattern3.place(y=280, x=5)
        self.pattern4 = customtkinter.CTkButton(master=self.man_cont_frame.tab("Manual Control"), width=110, height=25,border_width=0, corner_radius=8, text="pattern4",command = self.Pat13_24)
        self.pattern4 .place(y=280, x=125)
        self.stop_pattern = customtkinter.CTkButton(master=self.man_cont_frame.tab("Manual Control"), width=110, height=25,border_width=0, corner_radius=8, text="stop",command = self.stop_pattern)
        self.stop_pattern .place(y=320, x=55)
        

        self.slider_3 = customtkinter.CTkSlider(self.man_cont_frame.tab("Automatic control"), orientation="vertical", from_=0,to=20, number_of_steps=20)
        self.slider_3.place(y=30, x=30)
        self.slider_4 = customtkinter.CTkSlider(self.man_cont_frame.tab("Automatic control"),orientation="vertical", from_=0, to=100, number_of_steps=100)
        self.slider_4.place(y=30, x=150)
        self.textbox1 = customtkinter.CTkTextbox(self.man_cont_frame.tab("Automatic control"), height=20, width=50)
        self.textbox1.place(y=90, x=60)
        self.textbox2 = customtkinter.CTkTextbox(self.man_cont_frame.tab("Automatic control"), height=20, width=50)
        self.textbox2.place(y=90, x=180)
        self.start = customtkinter.CTkButton(master=self.man_cont_frame.tab("Automatic control"),width=110,height=25,border_width=0,corner_radius=8,text="Start",command=self.check_val)
        self.start.place(y=340, x=5)
        self.resume = customtkinter.CTkButton(master=self.man_cont_frame.tab("Automatic control"), width=110, height=25,border_width=0, corner_radius=8, text="Resume")
        self.resume.place(y=340, x=125)
        self.stop = customtkinter.CTkButton(master=self.man_cont_frame.tab("Automatic control"), width=110, height=25,border_width=0, corner_radius=8, text="Stop",command = self.stop_pwm)
        self.stop.place(y=380, x=5)
        self.pause = customtkinter.CTkButton(master=self.man_cont_frame.tab("Automatic control"), width=110, height=25,border_width=0, corner_radius=8, text="Pause")
        self.pause.place(y=380, x=125)
        self.Time = customtkinter.CTkSlider(self.man_cont_frame.tab("Time and Delay"), orientation="vertical",from_=0, to=100, number_of_steps=100)
        self.Time.place(y=30, x=30)
        self.Delay = customtkinter.CTkSlider(self.man_cont_frame.tab("Time and Delay"), orientation="vertical",from_=0, to=100, number_of_steps=100)
        self.Delay.place(y=30, x=150)
        self.Time_box = customtkinter.CTkTextbox(self.man_cont_frame.tab("Time and Delay"), height=20, width=50)
        self.Time_box.place(y=90, x=60)
        self.Delay_box = customtkinter.CTkTextbox(self.man_cont_frame.tab("Time and Delay"), height=20, width=50)
        self.Delay_box.place(y=90, x=180)
        self.slider_3.bind(" <B1-Motion>", self.update_textbox1)
        self.slider_4.bind(" <B1-Motion>", self.update_textbox2)
        self.Time.bind(" <B1-Motion>", self.update_textbox3)
        self.Delay.bind(" <B1-Motion>", self.update_textbox4)
        self.slider_3.set(0)
        self.slider_4.set(0)
        self.Time.set(0)
        self.Delay.set(0)



        # create Graph and oscilloscope
        self.graph = customtkinter.CTkTabview(self, width=250)
        self.graph.add("Oscilloscope")
        self.graph.grid(row=0, column=1, padx=(10, 10),sticky = "ns")
        # self.graph.grid_rowconfigure(0, weight=1)
        # self.graph.grid_rowconfigure(0, weight=1)


        #Oscilloscope
        self.fig = plt.figure(figsize=(5, 4), dpi=100)

        # Add a subplot to the figure
        self.ax = self.fig.add_subplot(111)

        # Create an empty plot
        self.line, = self.ax.plot([], [])

        # Add labels and titles
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("ADC Value")
        self.ax.set_title("ADC Data Plot")

        # Set the x and y limits of the plot
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 3.3)

        # Create a Tkinter canvas to display the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph.tab("Oscilloscope"))
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

        # start the animation
        self.update_plot()
        #self.animation()


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
        


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def set_pressure(self):
        if self.Pressure_val.get() == 0:
            set_dac_raw(2,0)
        if self.Pressure_val.get() == 1:
            set_dac_raw(2,315)
        if self.Pressure_val.get() == 2:
            set_dac_raw(2,630)
        if self.Pressure_val.get() == 3:
            set_dac_raw(2,948)
        if self.Pressure_val.get() == 4:
            set_dac_raw(2,1260)
        if self.Pressure_val.get() == 5:
            set_dac_raw(2,1575)
        if self.Pressure_val.get() == 6:
            set_dac_raw(2,1890)
        if self.Pressure_val.get() == 7:
            set_dac_raw(2,2205)
        if self.Pressure_val.get() == 8:
            set_dac_raw(2,2520)
        if self.Pressure_val.get() == 9:
            set_dac_raw(2,2835)
        if self.Pressure_val.get() == 10:
            set_dac_raw(2,3150)
        if self.Pressure_val.get() == 11:
            set_dac_raw(2,3465)
        if self.Pressure_val.get() == 12:
            set_dac_raw(2,3780)
        if self.Pressure_val.get() == 13:
            set_dac_raw(2,4096)

    def update_textbox(self, event):
        self.textbox.delete("1.0", customtkinter.END)
        self.textbox.insert(customtkinter.END, "{0}".format(self.slider_2.get()))
        p.ChangeDutyCycle(int(self.slider_2.get()))


    def update_textbox1(self,event):
        self.textbox1.delete("1.0", customtkinter.END)
        self.textbox1.insert(customtkinter.END, "{0}".format(self.slider_3.get()))
        pwm.ChangeFrequency(int(self.slider_3.get()))

    def update_textbox2(self,event):
        self.textbox2.delete("1.0", customtkinter.END)
        self.textbox2.insert(customtkinter.END, "{0}".format(self.slider_4.get()))
        pwm.ChangeDutyCycle(int(self.slider_4.get()))

    def update_textbox3(self, event):
        self.Time_box.delete("1.0", customtkinter.END)
        self.Time_box.insert(customtkinter.END, "{0}".format(self.Time.get()))

    def update_textbox4(self, event):
        self.Delay_box.delete("1.0", customtkinter.END)
        self.Delay_box.insert(customtkinter.END, "{0}".format(self.Delay.get()))

    def update_textbox5(self, event):
        self.Press_textbox.delete("1.0", customtkinter.END)
        self.Press_textbox.insert(customtkinter.END, "{0}".format(self.Pressure_val.get()))

    def update_plot(self):
            # Read the ADC value
            adc_value = adcdac.read_adc_voltage(1,0)
            # Append the new data point to the plot data
            x_data = self.line.get_xdata()
            y_data = self.line.get_ydata()
            x_data = np.append(x_data, time.time())
            y_data = np.append(y_data, adc_value)
            self.line.set_data(x_data, y_data)
            # Update the x and y limits of the plot
            self.ax.set_xlim(max(0, x_data[-1] - 10), x_data[-1] + 1)
            self.ax.set_ylim(0, 3.3)
            # Redraw the canvas
            self.canvas.draw()
            # Schedule the function to be called again in 100 ms
            self.after(100, self.update_plot)


      
       


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
        
        
    def turn_on_1(self):
        if self.var.get() == 1:
                GPIO.output(channel,True)
        if self.var.get() == 0:
               GPIO.output(channel,False)
    
    def turn_on_2(self):
        if self.var1.get() == 1:
                GPIO.output(8,True)
        if self.var1.get() == 0:
               GPIO.output(8,False)
        
    def turn_on_3(self):
        if self.var2.get() == 1:
                GPIO.output(10,True)
        if self.var2.get() == 0:
               GPIO.output(10,False)
               
    def turn_on_4(self):
        if self.var3.get() == 1:
                GPIO.output(11,True)
        if self.var3.get() == 0:
               GPIO.output(11,False)
    
    
    def check_val(self):
        self.t = self.Time.get()
        self.d = self.Delay.get()
        self.c(self.t,self.d)

    def c(self,var1,var2):
        if int(var1) > 0 and int(var2) > 0:
            print("Time and Daly")
            self.tF = 1
            self.after(int(var2) * 1000, self.start_pwm)
        if int(var1) == 0 and int(var2) == 0:
            print("Time no Daly")
            self.start_pwm()
        if int(var1) == 0 and int(var2) > 0:
            print(" Daly")
            self.after(int(var2)*1000,self.start_pwm)
        if int(var1) > 0 and int(var2) == 0:
            print("Time")
            self.tF = 1
            self.start_pwm()


    def start_pwm(self):
        if self.tF ==1 :
            self.tF = 0
            pwm.start(0)
            self.after(int(self.t)*1000,self.stop_pwm)
        else:
            pwm.start(0)

    def stop_pwm(self):
        pwm.stop()
        
    def start_motor(self):
            p.start(30)
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            
    def stop_motor(self):
            p.stop()
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)        
    
    def Pat_123(self):
            if self.pat_flag == 0:
                    GPIO.output(11, GPIO.LOW)
                    GPIO.output(12, GPIO.HIGH)
                    self.after(100,self.pat1)
            else:
                    self.set_flag_pat()
                    
    def pat1(self):
            GPIO.output(8, GPIO.HIGH)
            GPIO.output(12, GPIO.LOW)
            self.after(100,self.pat2)
            
    def pat2(self):
            GPIO.output(10, GPIO.HIGH)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(8, GPIO.LOW)
            self.after(100,self.pat3)
            
    def pat3(self):
             GPIO.output(11, GPIO.HIGH)
             GPIO.output(8, GPIO.LOW)
             GPIO.output(10, GPIO.LOW)
             GPIO.output(12, GPIO.LOW)
             self.after(100,self.Pat_123)
             
    def Pat12_34(self):
            if self.pat_flag == 0:
                    GPIO.output(10, GPIO.LOW)
                    GPIO.output(11, GPIO.LOW)
                    GPIO.output(12, GPIO.HIGH)
                    GPIO.output(8, GPIO.HIGH)
                    self.after(100,self.pat34)
            else:
                    self.set_flag_pat()
                    
    def pat34(self):
            GPIO.output(10, GPIO.HIGH)
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(8, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            self.after(100,self.Pat12_34)
            
    def Pat14_23(self):
            if self.pat_flag == 0:
                    GPIO.output(10, GPIO.LOW)
                    GPIO.output(8, GPIO.LOW)
                    GPIO.output(12, GPIO.HIGH)
                    GPIO.output(11, GPIO.HIGH)
                    self.after(100,self.pat23)
            else:
                    self.set_flag_pat()
                    
    def pat23(self):
            GPIO.output(10, GPIO.HIGH)
            GPIO.output(8, GPIO.HIGH)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            self.after(100,self.Pat14_23)
            
    def Pat13_24(self):
            if self.pat_flag == 0:
                    GPIO.output(11, GPIO.LOW)
                    GPIO.output(8, GPIO.LOW)
                    GPIO.output(12, GPIO.HIGH)
                    GPIO.output(10, GPIO.HIGH)
                    self.after(100,self.pat23)
            else:
                    self.set_flag_pat()
                    
    def pat23(self):
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(8, GPIO.HIGH)
            GPIO.output(10, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            self.after(100,self.Pat13_24)
                            

     
     
     
                    
    def stop_pattern(self):
            self.pat_flag = 1
           

    def set_flag_pat(self):
            self.pat_flag = 0
            GPIO.output(12, GPIO.LOW)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(10, GPIO.LOW)
            GPIO.output(8, GPIO.LOW)
                       
            
           





if __name__ == "__main__":
    app = App()
    app.mainloop()
