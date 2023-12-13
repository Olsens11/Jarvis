import os

# ... (previous code)

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
        selected_index = (selected_index + 1) % 3  # Adjusted for left
        while not button_L.value:  # Wait until button is released
            pass
    elif button_R_state:
        selected_index = (selected_index - 1) % 3  # Adjusted for right
        while not button_R.value:  # Wait until button is released
            pass

    # Draw rectangles and text
    for i in range(3):
        x = i * (rect_width + rect_margin_x)
        y = rect_margin_y

        # Check if the rectangle is selected
        is_selected = i == selected_index

        # Calculate the starting position to center the word within the rectangle
        text_x = x + (rect_width - word_widths[i]) // 2
        text_y = y + rect_margin_y - 1

        # Draw the rectangle
        draw.rectangle(
            (x, y, x + rect_width, y + rect_height),
            outline=1 if not is_selected else 0,
            fill=1 if is_selected else 0,
        )

        # Draw the text
        draw.text((text_x, text_y), words[i], font=font, fill=0 if is_selected else 1)

    # Display file names in the root folder below the rectangles
    root_files = os.listdir("/")
    for i, file_name in enumerate(root_files):
        file_y = rect_margin_y + (i + 1) * (rect_height + rect_margin_y)
        draw.text((rect_margin_x, file_y), file_name, font=font, fill=1)

    # Rotate the image 180 degrees before displaying
    rotated_image = image.rotate(180)

    # Display the rotated image on the OLED
    oled.image(rotated_image)
    oled.show()
