import subprocess
import time
import Adafruit_SSD1306

# Set up the display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3C)

# Initialize the display.
disp.begin()

# Clear the display.
disp.clear()
disp.display()

# Function to get the most recent terminal output
def get_recent_output():
    try:
        # Run the command to get the terminal output
        result = subprocess.check_output(['bash', '-c', 'history 1'], universal_newlines=True)
        return result.strip()
    except Exception as e:
        return str(e)

# Main loop
try:
    while True:
        # Get the most recent terminal output
        terminal_output = get_recent_output()

        # Clear the display
        disp.clear()

        # Draw the text on the display
        disp.draw_text(0, 0, terminal_output)

        # Display the text
        disp.display()

        # Wait for a few seconds before updating again
        time.sleep(5)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    pass
finally:
    # Clear the display on exit
    disp.clear()
    disp.display()
