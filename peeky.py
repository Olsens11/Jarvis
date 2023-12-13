import os
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from font5x8 import font_data  # Import the font data

# Constants
WHITE = 1
BLACK = 0
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
FONT_SIZE = 8  # Change this value as needed
MAX_FILE_NAME_LENGTH = 16  # Adjust based on your preference

# Initialize I2C and OLED display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Load font
font = ImageFont.load_default()  # Use the default font

# Function to display text on OLED using ImageDraw
def display_text(text, color=WHITE):
    oled.fill(0)
    draw = ImageDraw.Draw(oled.image)
    draw.text((0, 0), text, font=font, fill=color)
    oled.show()

# Function to browse and display files in a directory
def browse_directory(path):
    try:
        files = os.listdir(path)
        return [file[:MAX_FILE_NAME_LENGTH] for file in files]
    except Exception as e:
        print(f"Exception during browse_directory: {e}")
        return []

# Main program
current_path = "/"
selected_index = 0

# Initialize buttons
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

while True:
    try:
        current_items = browse_directory(current_path)

        # Read button states
        button_A_state = not button_A.value
        button_B_state = not button_B.value

        # Determine text based on button states
        if button_A_state and button_B_state:
            text = "Both buttons pressed"
        elif button_A_state:
            text = "Button A pressed"
        elif button_B_state:
            text = "Button B pressed"
        else:
            # Display file/folder names
            text = current_items[selected_index]

        # Display text on OLED
        display_text(text, WHITE)

        # Handle user input
        if not button_A.value:
            selected_index = max(0, selected_index - 1)
            time.sleep(0.2)  # Debounce
        elif not button_B.value:
            selected_index = min(len(current_items) - 1, selected_index + 1)
            time.sleep(0.2)  # Debounce
        elif button_A.value and button_B.value:
            if selected_index == 0:  # Back
                current_path = os.path.dirname(current_path)
            time.sleep(0.2)  # Debounce

    except Exception as e:
        print(f"Main loop exception: {e}")

    time.sleep(0.1)  # Adjust sleep duration as needed
