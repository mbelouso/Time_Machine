import gpiod
import time
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# GPIO and sensor setup
CHIP_PATH = "/dev/gpiochip4"  # using the GPIOchip4
PELTIER_PIN = 18  # BCM GPIO 18, verify with gpioinfo
DS18B20_PATH = "/sys/bus/w1/devices/28-9e4fc80664ff/w1_slave" # Replace with your sensor ID

# Initialize GPIO with error handling
try:
    chip = gpiod.Chip(CHIP_PATH)
    config = gpiod.line_settings.LineSettings()
    config.direction = gpiod.line_settings.Direction.OUTPUT
    config.output_value = gpiod.line_settings.Value.INACTIVE  # Ensure OFF initially

    request = chip.request_lines(
        consumer="PeltierControl",
        config={PELTIER_PIN: config},
    )
except Exception as e:
    print(f"GPIO Initialization Error: {e}")
    exit()

# Function to read temperature
def read_temperature():
    try:
        with open(DS18B20_PATH, "r") as file:
            lines = file.readlines()
            if "YES" in lines[0]:
                temp_str = lines[1].split("t=")[-1].strip()
                temp_c = int(temp_str) / 1000.0
                return round(temp_c, 2)
    except Exception as e:
        print(f"Temperature Read Error: {e}")
    return None

# Function to control Peltier based on set temperature
def control_peltier():
    temp = read_temperature()
    if temp is not None:
        current_temp_label.config(text=f"Current Temperature: {temp:.2f}°C")

        if temp > set_temp.get():
            request.set_values({PELTIER_PIN: gpiod.line_settings.Value.ACTIVE})  # Turn ON
            peltier_status_label.config(text="Peltier: ON", fg="red")
        else:
            request.set_values({PELTIER_PIN: gpiod.line_settings.Value.INACTIVE})  # Turn OFF
            peltier_status_label.config(text="Peltier: OFF", fg="green")

        # Update plot data
        temp_data.append(temp)
        time_data.append(len(temp_data) * 0.5)
        update_plot()
    else:
        current_temp_label.config(text="Current Temperature: Sensor Error!")

    # Schedule the next call
    root.after(500, control_peltier)

# Function to update the temperature graph
def update_plot():
    ax.clear()
    ax.plot(time_data, temp_data, marker="o", linestyle="-", color="blue")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature vs Time")
    canvas.draw()

# Tkinter GUI setup
root = tk.Tk()
root.title("Peltier Temperature Control")

set_temp = tk.DoubleVar(value=4.0)

frame = ttk.Frame(root)
frame.pack(pady=10)

ttk.Label(frame, text="Set Temperature (°C):").grid(row=0, column=0)
ttk.Entry(frame, textvariable=set_temp, width=5).grid(row=0, column=1)

current_temp_label = tk.Label(frame, text="Current Temperature: -- °C")
current_temp_label.grid(row=1, columnspan=2)

peltier_status_label = tk.Label(frame, text="Peltier: OFF", fg="green")
peltier_status_label.grid(row=2, columnspan=2)

# Matplotlib Figure
fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

temp_data = []
time_data = []

# Start the control loop
root.after(500, control_peltier)

# Cleanup on exit
def on_close():
    request.set_values({PELTIER_PIN: gpiod.line_settings.Value.INACTIVE})  # Ensure Peltier is OFF
    chip.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()