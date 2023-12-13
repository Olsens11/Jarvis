binary_file_path = "font5x8.bin"
python_list_path = "font5x8.py"

with open(binary_file_path, "rb") as binary_file, open(python_list_path, "w") as python_list:
    data = binary_file.read()
    hex_data = ', '.join([f'0x{byte:02X}' for byte in data])
    python_list.write(f"font_data = [{hex_data}]")
