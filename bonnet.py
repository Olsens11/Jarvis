import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import subprocess
import adafruit_ssd1306

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

# Menu options and corresponding commands
menu_options = {
    "Option 1": "ls",
    "Option 2": "df -h",
    "Option 3": "uname -a",
}

# Button pin mappings
button_pins = {
    "U": board.D17,
    "L": board.D27,
    "R": board.D23,
    "D": board.D22,
    "C": board.D4,
}

# Set up buttons
buttons = {button: DigitalInOut(pin) for button, pin in button_pins.items()}
for button in buttons.values():
    button.direction = Direction.INPUT
    button.pull = Pull.UP

# Function to display the menu
def display_menu():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), "Menu Options:", font=font, fill=1)
    for i, (option, _) in enumerate(menu_options.items(), start=1):
        draw.text((0, i * font_size), f"{i}. {option}", font=font, fill=1)
    oled.image(image.rotate(180))
    oled.show()

while True:
    # Display the menu
    display_menu()

    # Wait for a button press to select an option
    selected_option = None
    while selected_option is None:
        for button, button_pin in buttons.items():
            if not button_pin.value:
                # Button is pressed
                if button == "U":
                    # Move up in the menu
                    display_menu()
                elif button == "D":
                    # Move down in the menu
                    display_menu()
                elif button == "C":
                    # Select the current option
                    selected_option = list(menu_options.keys())[current_option - 1]
                    draw.rectangle((0, 0, width, height), outline=0, fill=0)
                    draw.text((0, 0), f"Selected: {selected_option}", font=font, fill=1)
                    oled.image(image.rotate(180))
                    oled.show()

    # Execute the selected command
    command = menu_options[selected_option]
    output = subprocess.check_output(command, shell=True).decode("utf-8")

    # Display the output on the OLED screen
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), f"Selected: {selected_option}", font=font, fill=1)
    draw.text((0, font_size), output, font=font, fill=1)
    oled.image(image.rotate(180))
    oled.show()
