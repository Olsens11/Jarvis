import board
import digitalio
import evdev
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Set up the OLED Bonnet
reset_pin = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin)

# Create an image with a black background
image = Image.new("1", (oled.width, oled.height), 0)
draw = ImageDraw.Draw(image)

# Load a font
font = ImageFont.load_default()

# Initialize buttons
button_a = digitalio.DigitalInOut(board.D5)
button_a.switch_to_input(pull=digitalio.Pull.UP)

button_b = digitalio.DigitalInOut(board.D6)
button_b.switch_to_input(pull=digitalio.Pull.UP)

# Calibrate joystick values based on your specific joystick
min_x, max_x = 0, 1023
min_y, max_y = 0, 1023

while True:
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Read button states
    button_a_state = not button_a.value
    button_b_state = not button_b.value

    # Read joystick values
    joystick_x_value = analogio.read(board.JOYSTICK_X)
    joystick_y_value = analogio.read(board.JOYSTICK_Y)

    # Determine text based on button states
    if button_a_state and button_b_state:
        text = "Both buttons pressed"
    elif button_a_state:
        text = "Button A pressed"
    elif button_b_state:
        text = "Button B pressed"
    else:
    
