import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Set up the OLED Bonnet
reset_pin = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin)

# Set up the ADC for the joystick
ads = ADS.ADS1015(i2c)
x_channel = AnalogIn(ads, ADS.P0)
y_channel = AnalogIn(ads, ADS.P1)

# Set up the buttons
button_a = digitalio.DigitalInOut(board.D5)
button_a.switch_to_input(pull=digitalio.Pull.UP)

button_b = digitalio.DigitalInOut(board.D6)
button_b.switch_to_input(pull=digitalio.Pull.UP)

# Clear the display
oled.fill(0)
oled.show()

# Create an image with a white background
image = Image.new("1", (oled.width, oled.height), 1)
draw = ImageDraw.Draw(image)

# Load a font
font = ImageFont.load_default()

while True:
    # Clear the display
    oled.fill(0)

    # Check button states
    button_a_state = "Pressed" if not button_a.value else "Released"
    button_b_state = "Pressed" if not button_b.value else "Released"

    # Draw button states on the image
    draw.text((10, 10), f"Button A: {button_a_state}", font=font, fill=0)
    draw.text((10, 30), f"Button B: {button_b_state}", font=font, fill=0)

    # Read joystick values
    x_value = x_channel.value
    y_value = y_channel.value

    # Draw joystick values on the image
    draw.text((10, 50), f"Joystick X: {x_value}", font=font, fill=0)
    draw.text((10, 70), f"Joystick Y: {y_value}", font=font, fill=0)

    # Display the image on the OLED
    oled.image(image)
    oled.show()
