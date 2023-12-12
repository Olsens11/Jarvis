import board
import digitalio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Set up the OLED Bonnet
reset_pin = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin)

# Clear the display
oled.fill(0)
oled.show()

# Create an image with a black background
image = Image.new("1", (oled.width, oled.height), 0)
draw = ImageDraw.Draw(image)

# Load a font
font = ImageFont.load_default()

while True:
    # Clear the display
    oled.fill(0)

    # Check button states
    button_a_state = not digitalio.DigitalInOut(board.D5).value
    button_b_state = not digitalio.DigitalInOut(board.D6).value

    # Draw button states on the image
    draw.text((10, 10), f"Button A: {'Pressed' if button_a_state else 'Released'}", font=font, fill=1)
    draw.text((10, 30), f"Button B: {'Pressed' if button_b_state else 'Released'}", font=font, fill=1)

    # Display the image on the OLED
    oled.image(image)
    oled.show()
