import time
import board
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw
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

# Initialize button for joystick
button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP

# Initial dot position
dot_x = width // 2
dot_y = height // 2

# Initial speed and acceleration
dot_speed = 0.5
acceleration = 0.02

# Time tracking for speed increase
start_time = None

while True:
    # Clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Read joystick button state
    button_U_state = not button_U.value

    # Move the dot based on joystick input with accelerating speed
    if button_U_state:
        dot_y -= min(1, dot_speed)

        # Check if the button is pressed, and record the start time
        if start_time is None:
            start_time = time.monotonic()
    else:
        start_time = None

    # Increase dot speed smoothly over time
    current_time = time.monotonic()
    if start_time is not None and current_time - start_time >= 2:
        dot_speed += acceleration  # Increase acceleration
        start_time = None

    # Wrap the dot to the opposite side when off-screen
    dot_y = dot_y % height

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
