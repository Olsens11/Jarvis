import os
import board
import digitalio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import threading

# ... (Previous imports and initialization)

# Lock for synchronization
lock = threading.Lock()

# Flag to indicate background loading completion
loading_complete = True

def load_directory_contents(directory):
    global displayed_files
    global loading_complete

    with lock:
        displayed_files = get_displayed_files(directory)
        loading_complete = True

# ... (Previous code)

# Main loop
while True:
    # ... (Previous code)

    # Handle center button press
    if button_C_state:
        if selected_index == 0 or selected_index == 1:  # Back or Faves rectangle selected
            current_path = os.path.dirname(current_path)
            prev_selected_index = selected_index
            selected_index = 3  # Select the uppermost filename
            while not button_C.value:  # Wait until button is released
                pass
        elif selected_index > 2:  # Filename rectangle selected
            selected_file = os.listdir(current_path)[len(os.listdir(current_path)) - selected_index + 2]
            selected_path = os.path.join(current_path, selected_file)
            if os.path.isdir(selected_path):
                current_path = selected_path
                prev_selected_index = selected_index
                selected_index = 3  # Select the uppermost filename

                # Start background loading
                loading_complete = False
                threading.Thread(target=load_directory_contents, args=(current_path,), daemon=True).start()

                while not button_C.value or not loading_complete:  # Wait until button is released and loading is complete
                    pass

    # ... (Previous code)

    # Display file names in the current directory below the rectangles
    with lock:
        for i, file_name in enumerate(reversed(displayed_files)):
            # ... (Previous code)

    # ... (Previous code)
