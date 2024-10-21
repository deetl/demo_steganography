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
    return [(n >> i) & 1 for i in range(length - 1, -1, -1)]


def check_embedded_data(stego_image_path):
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

    extracted_marker = ''.join(
        [chr(bits_to_int(extracted_marker_bits[i:i + 8])) for i in range(0, len(extracted_marker_bits), 8)])

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

    bit_position = int(bits_to_int(bit_position_bits) / 16)
    print(f"Bit position used for embedding: {bit_position}")

    # Step 3: Extract the length of the binary data from the next 11 pixels
    bit_length_bits = []
    for x in range(18, 29):
        r, g, b = pixels[x, 0]
        bit_length_bits.append(r & 1)
        bit_length_bits.append(g & 1)
        bit_length_bits.append(b & 1)

    bit_length = int(bits_to_int(bit_length_bits) / 2)
    byte_length = bit_length // 8  # Convert to bytes
    print(f"Data length: {bit_length} bits ({byte_length} bytes)")

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Check if an image contains embedded data.")
    parser.add_argument('-r', '--read', type=str, default='output_stego.png', help='Path to the image (default: image.png)')

    # Parse arguments
    args = parser.parse_args()

    image_path = args.read

    # Check for embedded data in the image
    check_embedded_data(image_path)
