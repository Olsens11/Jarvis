import os
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageFont
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

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_L.pull = Pull.UP

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_R.pull = Pull.UP

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP

# Load font
font = ImageFont.load_default()  # Use the default font

# Function to display text on OLED
def display_text(text, color=WHITE):
    oled.fill(0)
    x = 0
    y = 0
    for char in text:
        oled.text(char, x, y, color)
        x += FONT_SIZE  # Adjust the spacing based on your preference
        if x >= DISPLAY_WIDTH:
            x = 0
            y += FONT_SIZE + 2  # Adjust the vertical spacing based on your preference
    oled.show()

# Function to display menu options
def display_menu(options, selected_index):
    oled.fill(0)
    for i, option in enumerate(options):
        y = i * (FONT_SIZE + 2)
        if i == selected_index:
            oled.rect(0, y, DISPLAY_WIDTH, y + FONT_SIZE + 2, WHITE)
            display_text(option, BLACK)
        else:
            display_text(option, WHITE)
    oled.show()

# Function to handle file/folder selection
def select_item(items, selected_index):
    return items[selected_index]

# Function to display and handle favorites screen
def display_favorites(favorites, selected_index):
    display_menu(favorites, selected_index)
    # Handle user input and add to favorites logic here

# Function to display and handle settings screen
def display_settings(selected_index):
    settings = ["Invert Black/White", "Rotate Screen", "Close Program"]
    display_menu(settings, selected_index)
    # Handle user input and settings logic here

# Function to browse and display files in a directory
def browse_directory(path):
    files = os.listdir(path)
    return [file[:MAX_FILE_NAME_LENGTH] for file in files]

# Main program
current_path = "/"
selected_index = 0
favorites = []

while True:
    current_items = browse_directory(current_path)

    # Display top menu
    menu_options = ["Back", "Favorites", "Settings"]
    display_menu(menu_options, selected_index)

    # Display file/folder names
    display_menu(current_items, selected_index)

    # Handle user input
    if not button_U.value:
        selected_index = max(0, selected_index - 1)
    elif not button_D.value:
        selected_index = min(len(current_items) - 1, selected_index + 1)
    elif not button_C.value:
        if selected_index == 0:  # Back
            current_path = os.path.dirname(current_path)
        elif selected_index == 1:  # Favorites
            display_favorites(favorites, 0)
        elif selected_index == 2:  # Settings
            display_settings(0)
    elif not button_A.value:
        # Additional logic for button A
        pass
    elif not button_B.value:
        # Additional logic for button B
        pass

    time.sleep(0.1)  # Adjust sleep duration as needed
