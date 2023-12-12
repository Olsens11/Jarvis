import board
import digitalio
import evdev
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

# Find and print the names of available devices
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    print(f"Found device: {device.name} ({device.phys})")

# Identify the correct joystick device based on the printed names
joystick_name = "your_joystick_name_here"  # Replace with the correct name
joystick = None
for device in devices:
    if joystick_name.lower() in device.name.lower():
        joystick = device
        break

if joystick is None:
    raise RuntimeError("Joystick not found")

# Calibrate joystick values based on your specific joystick
min_x, max_x = 0, 1023
min_y, max_y = 0, 1023

while True:
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Read button states
    button_a_state = not button_a.value
    button_b_state = not button_b.value

    # Read joystick values
    for event in joystick.read():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_X:
                joystick_x_value = event.value
            elif event.code == evdev.ecodes.ABS_Y:
                joystick_y_value = event.value

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
    draw.text((10 + (joystick_x_value - min_x) // 100, 10 + (joystick_y_value - min_y) // 100), text, font=font, fill=1)

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()
