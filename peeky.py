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
button_U = digitalio.DigitalInOut(board.D17)
button_U.switch_to_input(pull=digitalio.Pull.UP)

button_D = digitalio.DigitalInOut(board.D22)
button_D.switch_to_input(pull=digitalio.Pull.UP)

button_R = digitalio.DigitalInOut(board.D23)
button_R.switch_to_input(pull=digitalio.Pull.UP)

button_L = digitalio.DigitalInOut(board.D27)
button_L.switch_to_input(pull=digitalio.Pull.UP)

# Rectangles configuration
rect_width = 40
rect_height = 12
rect_margin_x = 1
rect_margin_y = 1

# Initial selected rectangle index
selected_index = 0

# Main loop
while True:
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Read button states
    button_U_state = not button_U.value
    button_D_state = not button_D.value
    button_R_state = not button_R.value
    button_L_state = not button_L.value

    # Update selected index based on directional buttons
    if button_U_state:
        selected_index = (selected_index - 1) % 3
        while not button_U.value:  # Wait until button is released
            pass
    elif button_D_state:
        selected_index = (selected_index + 1) % 3
        while not button_D.value:  # Wait until button is released
            pass
    elif button_L_state:
        selected_index = (selected_index + 1) % 3
        while not button_L.value:  # Wait until button is released
            pass
    elif button_R_state:
        selected_index = (selected_index - 1) % 3
        while not button_R.value:  # Wait until button is released
            pass

    # Draw rectangles and text
    for i in range(3):
        x = i * (rect_width + rect_margin_x)
        y = rect_margin_y

        # Check if the rectangle is selected
        is_selected = i == selected_index

        # Draw the rectangle
        draw.rectangle(
            (x, y, x + rect_width, y + rect_height),
            outline=1 if not is_selected else 0,
            fill=1 if is_selected else 0,
        )

        # Draw the text
        text = ["Back", "Faves", "Setup"][i]
        text_width, text_height = draw.textsize(text, font)
        text_x = x + (rect_width - text_width) // 2  # Center horizontally
        text_y = y + rect_margin_y - 1
        draw.text((text_x, text_y), text, font=font, fill=0 if is_selected else 1)

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()
