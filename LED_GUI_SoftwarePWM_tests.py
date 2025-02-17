import lgpio
import tkinter as tk

# GPIO Setup
LED_CONFIG = {
    18: "Green LED",
    23: "Orange LED",
    24: "Red LED"
}
CHIP = 0  # Usually 0 for Raspberry Pi 5
PWM_FREQUENCY = 1000  # 1kHz frequency

# Initialize GPIO and PWM
h = lgpio.gpiochip_open(CHIP)
for pin in LED_CONFIG.keys():
    lgpio.gpio_claim_output(h, pin)  # Set as output
    lgpio.tx_pwm(h, pin, PWM_FREQUENCY, 0)  # Start with 0% duty cycle

# GUI Setup
root = tk.Tk()
root.title("LED PWM Control")

# Function to adjust brightness
def set_brightness(pin, value):
    """Set PWM brightness based on slider value (0-100%)."""
    duty_cycle = int(value)  # Convert to integer
    lgpio.tx_pwm(h, pin, PWM_FREQUENCY, duty_cycle)

# Create UI for each LED
for pin, label_text in LED_CONFIG.items():
    frame = tk.Frame(root)
    frame.pack(pady=5)

    label = tk.Label(frame, text=label_text, font=("Arial", 12))
    label.pack(side=tk.LEFT, padx=10)

    pwm_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal",
                          label="Brightness", command=lambda v, p=pin: set_brightness(p, v))
    pwm_slider.pack(side=tk.LEFT, padx=10)

# Start the GUI
try:
    root.mainloop()

finally:
    # Turn off all LEDs by setting PWM duty cycle to 0%
    for pin in LED_CONFIG.keys():
        lgpio.tx_pwm(h, pin, PWM_FREQUENCY, 0)  # Set duty cycle to 0
        lgpio.gpio_write(h, pin, 0)  # Ensure pin is LOW

    lgpio.gpiochip_close(h)  # Close GPIO chip
