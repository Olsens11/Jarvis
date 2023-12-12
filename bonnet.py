import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import subprocess
import threading

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

# Function to display the terminal output
def display_terminal_output():
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Read the content of the file containing terminal output
        with open("terminal_output.txt", "r") as file:
            terminal_output = file.read()

        # Display the terminal output on the OLED screen
        draw.text((0, 0), terminal_output, font=font, fill=1)
        oled.image(image.rotate(180))
        oled.show()

# Start the thread to display terminal output
thread = threading.Thread(target=display_terminal_output)
thread.start()

while True:
    # Check button presses
    for button, button_pin in buttons.items():
        if not button_pin.value:
            # Button is pressed
            if button == "U":
                # Simulate user typing a command
                command = input("Enter command: ")
                # Write the command to the file
                with open("terminal_output.txt", "a") as file:
                    file.write(f"$ {command}\n")
                # Execute the command and append the output to the file
                subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                with open("terminal_output.txt", "a") as file:
                    file.write("Command executed.\n")
            elif button == "C":
                # Clear the terminal output file
                with open("terminal_output.txt", "w") as file:
                    file.write("")

# Wait for the display thread to finish
thread.join()
