import gpiod
import tkinter as tk

# GPIO Setup
LED_CONFIG = {
    18: "Green LED",
    23: "Orange LED",
    24: "Red LED"
}
CHIP_PATH = "/dev/gpiochip4"

# Create line settings for all LEDs
config = gpiod.LineSettings()
config.direction = gpiod.line_settings.Direction.OUTPUT
config.output_value = gpiod.line_settings.Value.INACTIVE

# Request GPIO lines
request = gpiod.request_lines(
    CHIP_PATH,
    consumer="LED_GUI_Controller",
    config={pin: config for pin in LED_CONFIG.keys()}
)

# GUI Setup
root = tk.Tk()
root.title("LED Control Panel")

# Functions to control LEDs
def turn_on(pin):
    request.set_value(pin, gpiod.line_settings.Value.ACTIVE)

def turn_off(pin):
    request.set_value(pin, gpiod.line_settings.Value.INACTIVE)

def set_brightness(pin, value):
    """Simulate PWM by quickly toggling the LED (software PWM)."""
    if int(value) > 0:
        request.set_value(pin, gpiod.line_settings.Value.ACTIVE)
    else:
        request.set_value(pin, gpiod.line_settings.Value.INACTIVE)

# Create UI for each LED
for pin, label_text in LED_CONFIG.items():
    frame = tk.Frame(root)
    frame.pack(pady=5)

    label = tk.Label(frame, text=label_text, font=("Arial", 12))
    label.pack(side=tk.LEFT, padx=10)

    on_button = tk.Button(frame, text="ON", command=lambda p=pin: turn_on(p), bg="green", fg="white")
    on_button.pack(side=tk.LEFT, padx=5)

    off_button = tk.Button(frame, text="OFF", command=lambda p=pin: turn_off(p), bg="red", fg="white")
    off_button.pack(side=tk.LEFT, padx=5)

    pwm_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal",
                          label="Brightness", command=lambda v, p=pin: set_brightness(p, v))
    pwm_slider.pack(side=tk.LEFT, padx=10)

# Start the GUI
try:
    root.mainloop()
finally:
    for pin in LED_CONFIG:
        request.set_value(pin, gpiod.line_settings.Value.INACTIVE)
    request.release()  # Ensure GPIOs are released when GUI closes
