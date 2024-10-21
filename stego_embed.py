import sys
import argparse
from PIL import Image, UnidentifiedImageError

def int_to_bits(n, length):
    """Convert an integer to a list of bits."""
    return [(n >> i) & 1 for i in range(length-1, -1, -1)]

def embed_data_in_image(image_path, binary_file_path, output_image_path, bit_position):
    try:
        # Open image
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        sys.exit(1)
    except UnidentifiedImageError:
        print(f"Error: The file '{image_path}' is not a valid image or the format is not supported.")
        sys.exit(1)
    except Exception as e:
        print(f"An unknown error occurred while opening the image file: {e}")
        sys.exit(1)

    # Check if the image is lossy (e.g. JPEG, WEBP)
    if img.format.lower() in ['jpeg', 'jpg', 'webp']:
        print("Error: The image was saved in a lossy format (JPEG/WEBP). Steganography cannot be used.")
        sys.exit(1)

    img = img.convert("RGB")  # Ensure the image is in RGB format

    # Load binary file
    try:
        with open(binary_file_path, "rb") as binary_file:
            binary_data = binary_file.read()
    except FileNotFoundError:
        print(f"Error: The binary file '{binary_file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the binary file: {e}")
        sys.exit(1)

    # Convert the binary file to a list of bits
    bit_data = []
    for byte in binary_data:
        bit_data.extend(int_to_bits(byte, 8))  # 8 bits per byte

    # Store the length of the binary data (in bits)
    bit_length = len(bit_data)
    if bit_length + 32 > img.width * img.height * 3:
        print("Error: The binary file is too large to be embedded in the image.")
        sys.exit(1)

    # Get pixel data
    pixels = img.load()

    # Image width and height
    width, height = img.size

    # Step 1: Clear LSBs of all pixels up to pixel 39
    for x in range(29):
        for channel in range(3):
            r, g, b = pixels[x, 0]
            r = r & ~1
            g = g & ~1
            b = b & ~1
            pixels[x, 0] = (r, g, b)

    # Step 2: Embed "STEGO" in the LSBs of the first 14 pixels
    marker = "STEGO"
    marker_bits = []
    for char in marker:
        marker_bits.extend(int_to_bits(ord(char), 8))  # 8 bits per character

    bit_index = 0
    for x in range(14):
        for channel in range(3):
            if bit_index < len(marker_bits):
                r, g, b = pixels[x, 0]
                if channel == 0:
                    r = (r & ~1) | marker_bits[bit_index]
                elif channel == 1:
                    g = (g & ~1) | marker_bits[bit_index]
                elif channel == 2:
                    b = (b & ~1) | marker_bits[bit_index]
                pixels[x, 0] = (r, g, b)
                bit_index += 1

    # Step 3: Store the bit position in the next 4 pixels
    bit_position_bits = int_to_bits(bit_position, 8)
    bit_index = 0
    for x in range(14, 18):
        for channel in range(3):
            if bit_index < len(bit_position_bits):
                r, g, b = pixels[x, 0]
                if channel == 0:
                    r = (r & ~1) | bit_position_bits[bit_index]
                elif channel == 1:
                    g = (g & ~1) | bit_position_bits[bit_index]
                elif channel == 2:
                    b = (b & ~1) | bit_position_bits[bit_index]
                pixels[x, 0] = (r, g, b)
                bit_index += 1

    # Step 4: Store the length of the binary data in the next 11 pixels
    bit_length_bits = int_to_bits(bit_length, 32)  # 32 bits for length
    bit_index = 0
    for x in range(18, 29):
        for channel in range(3):
            if bit_index < len(bit_length_bits):
                r, g, b = pixels[x, 0]
                if channel == 0:
                    r = (r & ~1) | bit_length_bits[bit_index]
                elif channel == 1:
                    g = (g & ~1) | bit_length_bits[bit_index]
                elif channel == 2:
                    b = (b & ~1) | bit_length_bits[bit_index]
                pixels[x, 0] = (r, g, b)
                bit_index += 1

    # Step 5: Now embed the binary data into the rest of the image
    bit_index = 0
    mask = 1 << bit_position  # Create a mask for the specified bit position
    for y in range(height):
        for x in range(width):
            if y == 0 and x < 40:  # Skip the first 40 pixels, as they store metadata
                continue
            r, g, b = pixels[x, y]
            if bit_index < bit_length:
                r = (r & ~mask) | ((bit_data[bit_index] << bit_position) & mask)
                bit_index += 1
            if bit_index < bit_length:
                g = (g & ~mask) | ((bit_data[bit_index] << bit_position) & mask)
                bit_index += 1
            if bit_index < bit_length:
                b = (b & ~mask) | ((bit_data[bit_index] << bit_position) & mask)
                bit_index += 1
            pixels[x, y] = (r, g, b)
            if bit_index >= bit_length:
                break
        if bit_index >= bit_length:
            break

    # Check and ensure the output path ends with .png
    if not output_image_path.lower().endswith('.png'):
        print(f"Warning: The output path '{output_image_path}' did not have a .png extension. The file will be saved as PNG.")
        output_image_path = output_image_path.rsplit('.', 1)[0] + '.png'

    # Save image as PNG
    try:
        img.save(output_image_path, "PNG")
        print(f"The stego image has been saved as '{output_image_path}'.")
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Embed binary data into an image.")
    parser.add_argument('-r', '--read', type=str, default='image.png', help='Path to the image (default: image.png)')
    parser.add_argument('-b', '--binary', type=str, default='input.txt', help='Path to the binary file (default: data.bin)')
    parser.add_argument('-w', '--write', type=str, default='output_stego.png', help='Path to the output image (default: output_stego.png)')
    parser.add_argument('-B', '--bit', type=int, default=0, help='Bit position to embed data (default: 0)')

    # Parse arguments
    args = parser.parse_args()

    image_path = args.read
    binary_file_path = args.binary
    output_image_path = args.write
    bit_position = args.bit

    if bit_position < 0 or bit_position > 7:
        print("Error: The bit position must be between 0 and 7.")
        sys.exit(1)

    # Embed data into image
    embed_data_in_image(image_path, binary_file_path, output_image_path, bit_position)
