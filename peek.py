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
button_A.direction = digitalio.Direction.INPUT
button_A.pull = digitalio.Pull.UP

button_B = digitalio.DigitalInOut(board.D6)
button_B.direction = digitalio.Direction.INPUT
button_B.pull = digitalio.Pull.UP

button_L = digitalio.DigitalInOut(board.D27)
button_L.direction = digitalio.Direction.INPUT
button_L.pull = digitalio.Pull.UP

button_R = digitalio.DigitalInOut(board.D23)
button_R.direction = digitalio.Direction.INPUT
button_R.pull = digitalio.Pull.UP

button_U = digitalio.DigitalInOut(board.D17)
button_U.direction = digitalio.Direction.INPUT
button_U.pull = digitalio.Pull.UP

button_D = digitalio.DigitalInOut(board.D22)
button_D.direction = digitalio.Direction.INPUT
button_D.pull = digitalio.Pull.UP

button_C = digitalio.DigitalInOut(board.D4)
button_C.direction = digitalio.Direction.INPUT
button_C.pull = digitalio.Pull.UP

# Rectangles and square configuration
rect_width = 38
rect_height = 12
rect_margin_x = 1
rect_margin_y = 1

filename_rect_width = 124
filename_rect_height = 12
max_filename_length = 15  # Maximum characters to display in filename rectangle

square_width = 12
square_height = 12

vert_rect_width = 12
vert_rect_height = 50

# Initialize selected_index and current_directory
selected_index = 0
current_directory = "/"

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

    # Example: Set selected_index based on button presses
    if button_A_state:
        selected_index = 0
    elif button_B_state:
        selected_index = 1
    elif button_U_state:
        # Example: Move up to the previous file if the Up button is pressed
        selected_index -= 1
    elif button_D_state:
        # Example: Move down to the next file if the Down button is pressed
        selected_index += 1

    # Draw the square to the left of the rectangles
    square_outline_color = 1 if selected_index == 0 else 0
    square_fill_color = 0 if selected_index == 0 else 1

    # Draw the outline of the square
    draw.rectangle(
        (0, rect_margin_y, square_width, rect_margin_y + square_height),
        outline=square_outline_color,
        fill=square_fill_color,
    )

    # Draw three horizontal lines inside the square
    for line_y in range(rect_margin_y + 2, rect_margin_y + square_height - 2, 4):
        draw.line(
            [(2, line_y), (square_width - 2, line_y)],
            fill=1 if selected_index == 0 else 0,
        )

    # Draw the vertical rectangle to the left of the filenames
    vert_rect_x = square_width
    vert_rect_y = rect_margin_y
    draw.rectangle(
        (vert_rect_x, vert_rect_y, vert_rect_x + vert_rect_width, vert_rect_y + vert_rect_height),
        outline=1 if selected_index == 0 else 0,
        fill=1 if selected_index == 0 else 0,
    )

    # Draw rectangles and text at the top
    words = ["Back", "Faves", "Setup"]
    word_widths = [5, 5, 5]  # Estimated widths, replace with actual values

    for i in range(3):
        x = square_width + i * (rect_width + rect_margin_x)
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
    displayed_files = os.listdir(current_directory)
    for i, file_name in enumerate(reversed(displayed_files)):
        file_y = rect_margin_y + (i + 1) * (filename_rect_height + rect_margin_y)

        # Check if the filename rectangle is selected
        is_selected = i + 3 == selected_index

        # Draw the filename rectangle
        draw.rectangle(
            (square_width, file_y, square_width + filename_rect_width, file_y + filename_rect_height),
            outline=1 if not is_selected else 0,
            fill=1 if is_selected else 0,
        )

        # Draw the filename text
        draw.text(
            (square_width + 1, file_y + 1),
            file_name if len(file_name) <= max_filename_length else file_name[:max_filename_length - 3] + "...",
            font=font,
            fill=0 if is_selected else 1,
        )

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()
