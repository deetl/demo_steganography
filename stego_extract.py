import sys
import argparse
from PIL import Image, UnidentifiedImageError

def bits_to_int(bits):
    """Convert a list of bits to an integer."""
    n = 0
    for bit in bits:
        n = (n << 1) | bit
    return n

def int_to_bits(n, length):
    """Convert an integer to a list of bits."""
    return [(n >> i) & 1 for i in range(length-1, -1, -1)]

def extract_data_from_image(stego_image_path, output_binary_file_path):
    try:
        # Open image
        img = Image.open(stego_image_path)
    except FileNotFoundError:
        print(f"Error: The file '{stego_image_path}' was not found.")
        sys.exit(1)
    except UnidentifiedImageError:
        print(f"Error: The file '{stego_image_path}' is not a valid image or the format is not supported.")
        sys.exit(1)
    except Exception as e:
        print(f"An unknown error occurred while opening the image file: {e}")
        sys.exit(1)

    img = img.convert("RGB")  # Ensure the image is in RGB format

    # Get pixel data
    pixels = img.load()

    # Step 1: Check for the Magic Marker "STEGO" in the first 14 pixels
    marker = "STEGO"
    marker_bits = []
    for char in marker:
        marker_bits.extend(int_to_bits(ord(char), 8))  # 8 bits per character

    extracted_marker_bits = []
    bit_index = 0
    for x in range(14):
        r, g, b = pixels[x, 0]
        extracted_marker_bits.append(r & 1)
        bit_index += 1
        if bit_index >= len(marker_bits):
            break
        extracted_marker_bits.append(g & 1)
        bit_index += 1
        if bit_index >= len(marker_bits):
            break
        extracted_marker_bits.append(b & 1)
        bit_index += 1
        if bit_index >= len(marker_bits):
            break

    extracted_marker = ''.join([chr(bits_to_int(extracted_marker_bits[i:i+8])) for i in range(0, len(extracted_marker_bits), 8)])

    if extracted_marker != marker:
        print("Error: Magic Marker 'STEGO' not found. This image does not contain embedded data or is corrupted.")
        sys.exit(1)

    print("Magic Marker 'STEGO' found.")

    # Step 2: Extract the bit position from the next 4 pixels
    bit_position_bits = []
    for x in range(14, 18):
        r, g, b = pixels[x, 0]
        bit_position_bits.append(r & 1)
        bit_position_bits.append(g & 1)
        bit_position_bits.append(b & 1)

    bit_position = int(bits_to_int(bit_position_bits)/16)
    print(f"Bit position used for embedding: {bit_position}")

    # Step 3: Extract the length of the binary data from the next 11 pixels
    bit_length_bits = []
    for x in range(18, 29):
        r, g, b = pixels[x, 0]
        bit_length_bits.append(r & 1)
        bit_length_bits.append(g & 1)
        bit_length_bits.append(b & 1)

    bit_length = int(bits_to_int(bit_length_bits)/2)
    byte_length = bit_length // 8  # Convert to bytes
    print(f"Data length: {bit_length} bits ({byte_length} bytes)")

    # Step 4: Extract the binary data from the rest of the image
    bit_data = []
    bit_index = 0
    mask = 1 << bit_position  # Create a mask for the specified bit position
    for y in range(img.height):
        for x in range(img.width):
            if y == 0 and x < 40:  # Skip the first 40 pixels, as they store metadata
                continue
            r, g, b = pixels[x, y]
            if bit_index < bit_length:
                bit_data.append((r & mask) >> bit_position)
                bit_index += 1
            if bit_index < bit_length:
                bit_data.append((g & mask) >> bit_position)
                bit_index += 1
            if bit_index < bit_length:
                bit_data.append((b & mask) >> bit_position)
                bit_index += 1
            if bit_index >= bit_length:
                break
        if bit_index >= bit_length:
            break

    # Convert the extracted bit data back into bytes
    binary_data = bytearray()
    for i in range(0, len(bit_data), 8):
        byte = bits_to_int(bit_data[i:i+8])
        binary_data.append(byte)

    # Save the extracted binary data
    try:
        with open(output_binary_file_path, "wb") as binary_file:
            binary_file.write(binary_data)
        print(f"Extracted binary data saved to '{output_binary_file_path}'.")
    except Exception as e:
        print(f"An error occurred while saving the binary file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Extract binary data from a stego image.")
    parser.add_argument('-r', '--read', type=str, default='output_stego.png', help='Path to the stego image (default: output_stego.png)')
    parser.add_argument('-w', '--write', type=str, default='output.txt', help='Path to the output binary file (default: extracted_data.bin)')

    # Parse arguments
    args = parser.parse_args()

    stego_image_path = args.read
    output_binary_file_path = args.write

    # Extract data from image
    extract_data_from_image(stego_image_path, output_binary_file_path)
