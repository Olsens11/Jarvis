import subprocess
import board
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont

# Set up the OLED Bonnet
reset_pin = DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin)

# Create blank image for drawing.
width = oled.width
height = oled.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)

# Fixed font size
font_size = 12
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)

# Terminal command to execute
terminal_command = "ls -l"

while True:
    # Clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Run terminal command and capture the output
    terminal_output = subprocess.check_output(terminal_command, shell=True)
    terminal_output = terminal_output.decode("utf-8")

    # Display the terminal output on the screen
    lines = terminal_output.splitlines()
    for i, line in enumerate(lines):
        draw.text((0, i * font_size), line, font=font, fill=1)

    # Display the image on the OLED screen
    rotated_image = image.rotate(180)
    oled.image(rotated_image)
    oled.show()
