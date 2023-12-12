import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw
import adafruit_ssd1306

# Set up the OLED Bonnet
reset_pin = DigitalInOut(board.D4)
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin)

# Create blank image for drawing.
# Make sure to create an image with mode '1' for 1-bit color.
width = oled.width
height = oled.height
image = Image.new("1", (width, height))

# Get drawing object to draw on the image.
draw = ImageDraw.Draw(image)

# Initialize buttons
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP

# Calibrate joystick values based on your specific joystick
min_x, max_x = 0, 65535  # Adjust these values as needed
min_y, max_y = 0, 65535

while True:
    # Clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Read button states
    button_A_state = not button_A.value
    button_B_state = not button_B.value
    button_C_state = not button_C.value

    # Read joystick values
    joystick_x_value = board.JOYSTICK_X
    joystick_y_value = board.JOYSTICK_Y

    # Determine text based on button states
    if button_A_state and button_B_state:
        text = "Both buttons pressed"
    elif button_A_state:
        text = "Button A pressed"
    elif button_B_state:
        text = "Button B pressed"
    else:
        text = "No buttons pressed"

    # Draw text on the image
    draw.text((10 + (joystick_x_value - min_x) // 100, 10 + (joystick_y_value - min_y) // 100), text, font=font, fill=1)

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()
