import board
import digitalio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Set up the OLED Bonnet
reset_pin = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin, transform='flipy')

# Create an image with a black background
image = Image.new("1", (oled.width, oled.height), 0)
draw = ImageDraw.Draw(image)

# Load a font
font = ImageFont.load_default()

# Initialize buttons
button_a = digitalio.DigitalInOut(board.D5)
button_a.switch_to_input(pull=digitalio.Pull.UP)

button_b = digitalio.DigitalInOut(board.D6)
button_b.switch_to_input(pull=digitalio.Pull.UP)

while True:
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Read button states
    button_a_state = not button_a.value
    button_b_state = not button_b.value

    # Determine text based on button states
    if button_a_state and button_b_state:
        text = "Both buttons pressed"
    elif button_a_state:
        text = "Button A pressed"
    elif button_b_state:
        text = "Button B pressed"
    else:
        text = "No buttons pressed"

    # Draw text on the image
    draw.text((10, 10), text, font=font, fill=1)

    # Display the image on the OLED
    oled.image(image)
    oled.show()
