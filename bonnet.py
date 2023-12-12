import board
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

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

# Load a font
font = ImageFont.load_default()

# Initialize buttons for joystick
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

# Initial dot position
dot_x, dot_y = width // 2, height // 2

while True:
    # Clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Read joystick button states
    button_U_state = not button_U.value
    button_L_state = not button_L.value
    button_R_state = not button_R.value
    button_D_state = not button_D.value
    button_C_state = not button_C.value

    # Update dot position based on joystick input
    if button_U_state and not button_D_state:
        dot_y -= 1
    elif not button_U_state and button_D_state:
        dot_y += 1

    if button_L_state and not button_R_state:
        dot_x -= 1
    elif not button_L_state and button_R_state:
        dot_x += 1

    # Draw the dot
    draw.point((dot_x, dot_y), fill=1)

    # Draw text displaying dot coordinates
    text = f"Dot Position: ({dot_x}, {dot_y})"
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    text_x = (width - text_width) // 2
    text_y = height - text_height - 2
    draw.text((text_x, text_y), text, font=font, fill=1)

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()
