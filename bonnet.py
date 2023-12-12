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
acceleration = 0.1

while True:
    # Clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Read joystick and button states
    button_U_state = not button_U.value
    button_L_state = not button_L.value
    button_R_state = not button_R.value
    button_D_state = not button_D.value
    button_C_state = not button_C.value
    button_A_state = not button_A.value
    button_B_state = not button_B.value

    # Draw text based on joystick and button states
    if button_D_state and not button_U_state:
        text = "Up"
    elif button_R_state and not button_L_state:
        text = "Left"
    elif button_L_state and not button_R_state:
        text = "Right"
    elif button_U_state and not button_D_state:
        text = "Down"
    elif not button_U_state and not button_D_state and not button_L_state and not button_R_state and button_C_state:
        text = "Center Button Pressed"
    elif button_A_state:
        text = "A Button Pressed"
    elif button_B_state:
        text = "B Button Pressed"
    else:
        text = "No Joystick or Button Pressed"

    # Wrap text to fit within the screen width
    wrapped_text = textwrap.fill(text, width=16)

    # Calculate the position to center the text within the screen
    text_x = (width - draw.textbbox((0, 0), wrapped_text, font=font)[2]) // 2
    text_y = (height - draw.textbbox((0, 0), wrapped_text, font=font)[3]) // 2

    # Draw wrapped text on the image
    draw.text((text_x, text_y), wrapped_text, font=font, fill=1)

    # Move the dot based on joystick input with variable speed
    if button_D_state:
        dot_y -= dot_speed
    elif button_U_state:
        dot_y += dot_speed
    if button_R_state:
        dot_x -= dot_speed
    elif button_L_state:
        dot_x += dot_speed

    # Wrap the dot to the opposite side when off-screen
    dot_x = dot_x % width
    dot_y = dot_y % height

    # Increase dot speed smoothly over time
    dot_speed += acceleration

    # Draw a dot on the image using paste() to achieve smooth movement
    dot_image = Image.new("1", (4, 4), 0)
    dot_draw = ImageDraw.Draw(dot_image)
    dot_draw.ellipse((0, 0, 4, 4), outline=1, fill=1)
    image.paste(dot_image, (int(dot_x) - 2, int(dot_y) - 2))

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()

    # Pause for a short duration to control the speed of the loop
    time.sleep(0.05)
