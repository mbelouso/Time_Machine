import gpiod
import time

# Define the GPIO pin and chip
LED_PIN = 18
CHIP_PATH = "/dev/gpiochip4"

# Create a line settings object
config = gpiod.LineSettings()

# Instead of using a string, we use the available attributes
config.direction = gpiod.line_settings.Direction.OUTPUT  # Correct way
config.output_value = gpiod.line_settings.Value.INACTIVE  # Set initial value to 0

# Request the GPIO line
request = gpiod.request_lines(
    CHIP_PATH,
    consumer="myLed",
    config={LED_PIN: config}
)

try:
    while True:
        request.set_value(LED_PIN, gpiod.line_settings.Value.ACTIVE)  # Turn LED on
        time.sleep(1)
        request.set_value(LED_PIN, gpiod.line_settings.Value.INACTIVE)  # Turn LED off
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    request.release()  # Properly release the request