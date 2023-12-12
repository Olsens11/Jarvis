import board
import digitalio
import analogio
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
button_a = digitalio.DigitalInOut(board.D5)
button_a.switch_to_input(pull=digitalio.Pull.UP)

button_b = digitalio.DigitalInOut(board.D6)
button_b.switch_to_input(pull=digitalio.Pull.UP)

# Initialize joystick
joystick_x = analogio.AnalogIn(board.A2)
joystick_y = analogio.AnalogIn(board.A3)

while True:
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Read button states
    button_a_state = not button_a.value
    button_b_state = not button_b.value

    # Read joystick values
    joystick_x_value = joystick_x.value
    joystick_y_value = joystick_y.value

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
    draw.text((10 + joystick_x_value // 100, 10 + joystick_y_value // 100), text, font=font, fill=1)

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()
