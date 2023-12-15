# main_script.py

import os
import board
import digitalio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from config import *
from digitalio import DigitalInOut, Direction, Pull

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

selected_index = 0  # Set the initial selected index to 0
max_index = 2  # Set the maximum index based on the number of top words

# Button Handling Section
while True:
    # Read button states
    button_A_state = not button_A.value
    button_B_state = not button_B.value
    button_L_state = not button_L.value
    button_R_state = not button_R.value
    button_U_state = not button_U.value
    button_D_state = not button_D.value
    button_C_state = not button_C.value

    # Determine button actions and update selected_index accordingly
    if button_U_state:
        selected_index -= 1
    elif button_D_state:
        selected_index += 1
    elif button_L_state:
        selected_index -= 1
    elif button_R_state:
        selected_index += 1

    # Ensure selected_index stays within the valid range
    selected_index = max(0, min(selected_index, max_index))
    
    # Clear the image and draw the UI based on the updated selected_index
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

# Configurations Section
# Draw the square to the left of the rectangles
square_outline_color = square_outline_color_selected if selected_index == 0 else square_outline_color_unselected
square_fill_color = square_fill_color_selected if selected_index == 0 else square_fill_color_unselected

# Draw the outline of the square
draw.rectangle(
    (0, rect_margin_y, square_width, rect_margin_y + square_height),
    outline=square_outline_color,
    fill=square_fill_color,
)

# Draw three horizontal lines inside the square
for line_y in range(rect_margin_y + 2, rect_margin_y + square_height - 2, square_line_spacing):
    draw.line(
        [(2, line_y), (square_width - 2, line_y)],
        fill=square_line_color_selected if selected_index == 0 else square_line_color_unselected,
    )

# Draw the vertical rectangle to the left of the filenames
vert_rect_x = square_width
vert_rect_y = rect_margin_y
draw.rectangle(
    (vert_rect_x, vert_rect_y, vert_rect_x + vert_rect_width, vert_rect_y + vert_rect_height),
    outline=vert_rect_outline_color_selected if selected_index == 0 else vert_rect_outline_color_unselected,
    fill=vert_rect_fill_color_selected if selected_index == 0 else vert_rect_fill_color_unselected,
)

# Draw rectangles and text at the top
for i, word in enumerate(top_words):
    x = square_width + i * (rect_width + rect_margin_x)
    y = rect_margin_y

    # Check if the rectangle is selected
    is_selected = i == selected_index

    # Calculate the starting position to center the word within the rectangle
    text_x = x + (rect_width - top_word_widths[i]) // 2
    text_y = y + rect_margin_y - 1

    # Draw the rectangle
    draw.rectangle(
        (x, y, x + rect_width, y + rect_height),
        outline=rect_outline_color_selected if not is_selected else rect_outline_color_unselected,
        fill=rect_fill_color_selected if is_selected else rect_fill_color_unselected,
    )

    # Draw the text
    draw.text((text_x, text_y), word, font=font, fill=text_color_selected if is_selected else text_color_unselected)


# Display file names in the current directory below the rectangles
displayed_files = os.listdir(current_directory)
for i, file_name in enumerate(reversed(displayed_files)):
    file_y = rect_margin_y + (i + 1) * (filename_rect_height + rect_margin_y)

    # Check if the filename rectangle is selected
    is_selected = i + 3 == selected_index

    # Draw the filename rectangle
    draw.rectangle(
        (square_width, file_y, square_width + filename_rect_width, file_y + filename_rect_height),
        outline=rect_outline_color_selected if not is_selected else rect_outline_color_unselected,
        fill=rect_fill_color_selected if is_selected else rect_fill_color_unselected,
    )

    # Determine text position based on alignment
    if text_alignment == "left":
        text_x = square_width + text_x_offset
    elif text_alignment == "center":
        text_x = square_width + (filename_rect_width - font.getsize(file_name)[0]) // 2
    elif text_alignment == "right":
        text_x = square_width + filename_rect_width - font.getsize(file_name)[0] - text_x_offset
    else:
        raise ValueError("Invalid text alignment value in config.py")

    # Draw the filename text
    draw.text(
        (text_x, file_y + text_y_offset),
        file_name if len(file_name) <= max_filename_length else file_name[:max_filename_length - 3] + "...",
        font=font,
        fill=text_color_selected if is_selected else text_color_unselected,
    )

# Display the image on the OLED
oled.image(image)
oled.show()
