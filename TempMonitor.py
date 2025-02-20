import gpiod
import time
import glob
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# GPIO chip and line for DS18B20 (GPIO4)
CHIP = "/dev/gpiochip4"
LINE_OFFSET = 4  # GPIO4

# Locate the sensor file
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    with open(device_file, 'r') as f:
        return f.readlines()

def read_temperature():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    
    temp_str = lines[1].split("t=")[-1]
    temp_c = float(temp_str) / 1000.0  # Convert to Celsius
    return temp_c

def update_temperature():
    global times, temps
    temp_c = read_temperature()
    times.append(times[-1] + 0.5 if times else 0)
    temps.append(temp_c)
    
    temperature_label.config(text=f"Current Temperature: {temp_c:.2f}°C")
    
    ax.clear()
    ax.plot(times, temps, marker='o', linestyle='-')
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature vs Time")
    canvas.draw()
    
    root.after(500, update_temperature)  # Update every 0.5 seconds

# Initialize Tkinter GUI
root = tk.Tk()
root.title("DS18B20 Temperature Monitor")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

temperature_label = tk.Label(frame, text="Reading temperature...", font=("Arial", 16))
temperature_label.pack(pady=10)

fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()

times, temps = [], []

update_temperature()  # Start updating temperature
root.mainloop()
