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

# Create an image with a white background
image = Image.new("1", (oled.width, oled.height), 1)
draw = ImageDraw.Draw(image)

# Load a font
font = ImageFont.load_default()

# Draw text on the image
draw.text((10, 10), "OLED Bonnet Test", font=font, fill=0)
draw.text((10, 30), "Hello, world!", font=font, fill=0)

# Display the image on the OLED
oled.image(image)
oled.show()
