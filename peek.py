import board
import digitalio
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
button_A = digitalio.DigitalInOut(board.D5)
button_A.switch_to_input(pull=digitalio.Pull.UP)

button_B = digitalio.DigitalInOut(board.D6)
button_B.switch_to_input(pull=digitalio.Pull.UP)

# Main loop
while True:
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Read button states
    button_A_state = not button_A.value
    button_B_state = not button_B.value

    # Draw rectangles and text
    rect_width = 42
    rect_height = 10
    rect_margin = 2

    # Back rectangle
    draw.rectangle(
        (rect_margin, rect_margin, rect_width, rect_height),
        outline=1 if button_A_state else 0,
        fill=1 if button_A_state else 0,
    )
    draw.text((rect_margin + 5, rect_margin + 2), "Back", font=font, fill=0)

    # Favorites rectangle
    draw.rectangle(
        (rect_width + 2 * rect_margin, rect_margin, 2 * rect_width + rect_margin, rect_height),
        outline=1 if button_B_state else 0,
        fill=1 if button_B_state else 0,
    )
    draw.text((2 * rect_margin + rect_width + 5, rect_margin + 2), "Favorites", font=font, fill=0)

    # Settings rectangle
    draw.rectangle(
        (2 * rect_width + 3 * rect_margin, rect_margin, 3 * rect_width + 2 * rect_margin, rect_height),
        outline=1 if not (button_A_state or button_B_state) else 0,
        fill=1 if not (button_A_state or button_B_state) else 0,
    )
    draw.text(
        (3 * rect_margin + 2 * rect_width + 5, rect_margin + 2),
        "Settings",
        font=font,
        fill=0,
    )

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()
