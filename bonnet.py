import time
import board
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import textwrap

# Set up the OLED Bonnet
reset_pin = DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin)

# Create blank image for drawing.
# Make sure to create an image with mode '1' for 1-bit color.
width = oled.width
height = oled.height
image = Image.new("1", (width, height))

# Get drawing object to draw on the image.
draw = ImageDraw.Draw(image)

# Fixed font size
font_size = 12
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)

# Initialize buttons for joystick, A, and B
button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_L.pull = Pull.UP

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_R.pull = Pull.UP

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP

button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

# Initial dot position
dot_x = width // 2
dot_y = height // 2

# Initial speed and acceleration
dot_speed = 0.5
acceleration = 0.02

# Time tracking for speed increase
start_time = None

# QWERTY keyboard characters
qwerty_chars = [
    "1234567890",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
]

# Selected text
selected_text = ""

while True:
    # Clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw QWERTY keyboard on the top half of the screen
    for i, row in enumerate(qwerty_chars):
        row_y = i * (height // len(qwerty_chars))
        char_width = width // len(row)
        for j, char in enumerate(row):
            char_x = j * char_width
            draw.text((char_x, row_y), char, font=font, fill=1)

    # Draw selected text on the bottom half of the screen
    draw.text((0, height // 2), selected_text, font=font, fill=1)

    # Read joystick and button states
    button_U_state = not button_U.value
    button_L_state = not button_L.value
    button_R_state = not button_R.value
    button_D_state = not button_D.value
    button_C_state = not button_C.value
    button_A_state = not button_A.value
    button_B_state = not button_B.value

    # Move the dot based on joystick input with accelerating speed
    if button_D_state:
        dot_y -= min(1, dot_speed)
    elif button_U_state:
        dot_y += min(1, dot_speed)
    if button_R_state:
        dot_x -= min(1, dot_speed)
    elif button_L_state:
        dot_x += min(1, dot_speed)

    # Wrap the dot to the opposite side when off-screen
    dot_x = dot_x % width
    dot_y = dot_y % height

    # Check if the button is pressed, and record the start time
    if button_D_state or button_U_state or button_R_state or button_L_state:
        if start_time is None:
            start_time = time.monotonic()
    else:
        start_time = None

    # Increase dot speed smoothly over time
    current_time = time.monotonic()
    if start_time is not None and current_time - start_time >= 2:
        dot_speed += acceleration  # Increase acceleration
        start_time = None

    # Draw a dot on the image using paste() to achieve smooth movement
    dot_image = Image.new("1", (4, 4), 0)
    dot_draw = ImageDraw.Draw(dot_image)
    dot_draw.ellipse((0, 0, 4, 4), outline=1, fill=1)
    image.paste(dot_image, (int(dot_x) - 2, int(dot_y) - 2))

    # Check if the center button is pressed to select a character
    if button_C_state:
        selected_row = min(int(dot_y / (height / len(qwerty_chars))), len(qwerty_chars) - 1)
        selected_col = min(int(dot_x / (width / len(qwerty_chars[selected_row]))), len(qwerty_chars[selected_row]) - 1)
        selected_char = qwerty_chars[selected_row][selected_col]
        selected_text += selected_char

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()

    # Pause for a short duration to control the speed of the loop
    time.sleep(0.05)
