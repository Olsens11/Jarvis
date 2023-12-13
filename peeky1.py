import os
import board
import digitalio
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
button_A = digitalio.DigitalInOut(board.D5)
button_A.switch_to_input(pull=digitalio.Pull.UP)

button_B = digitalio.DigitalInOut(board.D6)
button_B.switch_to_input(pull=digitalio.Pull.UP)

button_L = digitalio.DigitalInOut(board.D27)
button_L.switch_to_input(pull=digitalio.Pull.UP)

button_R = digitalio.DigitalInOut(board.D23)
button_R.switch_to_input(pull=digitalio.Pull.UP)

button_U = digitalio.DigitalInOut(board.D17)
button_U.switch_to_input(pull=digitalio.Pull.UP)

button_D = digitalio.DigitalInOut(board.D22)
button_D.switch_to_input(pull=digitalio.Pull.UP)

button_C = digitalio.DigitalInOut(board.D4)
button_C.switch_to_input(pull=digitalio.Pull.UP)

# Rectangles configuration
rect_width = 40
rect_height = 12
rect_margin_x = 1
rect_margin_y = 1

# Filename rectangles configuration
filename_rect_width = 122
filename_rect_height = 12
filename_margin_y = 1

# Initial selected rectangle index
selected_index = 0

# Previous selected index
prev_selected_index = 0

# Current directory path
current_path = "/"

# Words and their estimated widths
words = ["Back", "Faves", "Setup"]
word_widths = [24, 30, 30]

def get_displayed_files(directory):
    return os.listdir(directory)

# Main loop
while True:
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Read button states
    button_A_state = not button_A.value
    button_B_state = not button_B.value
    button_L_state = not button_L.value
    button_R_state = not button_R.value
    button_U_state = not button_U.value
    button_D_state = not button_D.value
    button_C_state = not button_C.value

    # Update selected index based on directional buttons
    if button_U_state:
        selected_index = (selected_index - 1) % (3 + len(os.listdir(current_path)))
        while not button_U.value:  # Wait until button is released
            pass
    elif button_D_state:
        selected_index = (selected_index + 1) % (3 + len(os.listdir(current_path)))
        while not button_D.value:  # Wait until button is released
            pass
    elif button_L_state:
        selected_index = (selected_index + 1) % (3 + len(os.listdir(current_path)))  # Adjusted for left
        while not button_L.value:  # Wait until button is released
            pass
    elif button_R_state:
        selected_index = (selected_index - 1) % (3 + len(os.listdir(current_path)))  # Adjusted for right
        while not button_R.value:  # Wait until button is released
            pass

    # Handle center button press
    if button_C_state:
        if selected_index == 0 or selected_index == 1:  # Back or Faves rectangle selected
            current_path = os.path.dirname(current_path)
            prev_selected_index = selected_index
            selected_index = 3  # Select the uppermost filename
            while not button_C.value:  # Wait until button is released
                pass
        elif selected_index > 2:  # Filename rectangle selected
            selected_file = os.listdir(current_path)[len(os.listdir(current_path)) - selected_index + 2]
            selected_path = os.path.join(current_path, selected_file)
            if os.path.isdir(selected_path):
                current_path = selected_path
                prev_selected_index = selected_index
                selected_index = 3  # Select the uppermost filename
                while not button_C.value:  # Wait until button is released
                    pass

    # Handle B button press (acts as Back button)
    if button_B_state:
        current_path = os.path.dirname(current_path)
        selected_index = prev_selected_index
        while not button_B.value:  # Wait until button is released
            pass

    # Draw rectangles and text at the top
    for i in range(3):
        x = i * (rect_width + rect_margin_x)
        y = rect_margin_y

        # Check if the rectangle is selected
        is_selected = i == selected_index

        # Calculate the starting position to center the word within the rectangle
        text_x = x + (rect_width - word_widths[i]) // 2
        text_y = y + rect_margin_y - 1

        # Draw the rectangle
        draw.rectangle(
            (x, y, x + rect_width, y + rect_height),
            outline=1 if not is_selected else 0,
            fill=1 if is_selected else 0,
        )

        # Draw the text
        draw.text((text_x, text_y), words[i], font=font, fill=0 if is_selected else 1)

    # Display file names in the current directory below the rectangles
    displayed_files = get_displayed_files(current_path)
    for i, file_name in enumerate(reversed(displayed_files)):
        file_y = rect_margin_y + (i + 1) * (filename_rect_height + rect_margin_y)

        # Check if the file rectangle is selected
        is_file_selected = selected_index == 3 + len(displayed_files) - 1 - i

        # Draw the file rectangle
        draw.rectangle(
            (0, file_y, filename_rect_width, file_y + filename_rect_height),
            outline=1 if not is_file_selected else 0,
            fill=1 if is_file_selected else 0,
        )

        # Draw the file text
        draw.text(
            (rect_margin_x, file_y + filename_margin_y - 1),
            file_name,
            font=font,
            fill=0 if is_file_selected else 1,
        )

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()
