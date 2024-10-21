import sys
import argparse
from PIL import Image

def extract_bit_plane(image, bit_position, scale):
    """Extract a specific bit plane from an image and optionally scale the bit to 0 or 255."""
    img = image.convert("RGB")  # Ensure the image is in RGB format
    width, height = img.size
    pixels = img.load()

    # Create a new image to hold the bit plane
    bit_plane_img = Image.new("RGB", (width, height))
    bit_plane_pixels = bit_plane_img.load()

    mask = 1 << bit_position  # Mask for the specified bit position

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if scale:
                # Extract the bit for each color channel
                r_bit = (r & mask) >> bit_position
                g_bit = (g & mask) >> bit_position
                b_bit = (b & mask) >> bit_position
                #  scale the bit to 0 or 255
                r_bit *= 255
                g_bit *= 255
                b_bit *= 255
            else:
                r_bit = (r & mask)
                g_bit = (g & mask)
                b_bit = (b & mask)



            # Set the new pixel value in the bit plane image
            bit_plane_pixels[x, y] = (r_bit, g_bit, b_bit)

    return bit_plane_img

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Extract a specific bit plane from an image and display or save it.")
    parser.add_argument('-r', '--read', type=str, default='image.png', help='Path to the input image (default: image.png)')
    parser.add_argument('-B', '--bit', type=int, default=0, help='Bit position to extract (default: 0)')
    parser.add_argument('-n', '--noscale', action='store_true', help='Do not scale the extracted bit to 0 or 255.')
    parser.add_argument('-s', '--show', action='store_true', help='Display the extracted bit plane image.')
    parser.add_argument('-w', '--write', type=str, default='output_layer.png', help='Path to the output image (default: output_stego.png)')
    # Parse arguments
    args = parser.parse_args()

    image_path = args.read
    bit_position = args.bit
    scale = not args.noscale
    show_image = args.show

    # Validate the bit position
    if bit_position < 0 or bit_position > 7:
        print("Error: The bit position must be between 0 and 7.")
        sys.exit(1)

    # Load the image
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while opening the image: {e}")
        sys.exit(1)

    # Extract the specified bit plane
    bit_plane_img = extract_bit_plane(img, bit_position, scale)

    # Save the result image with the bit plane embedded
    output_image_path = args.write
    bit_plane_img.save(output_image_path)
    print(f"The bit plane image has been saved as '{output_image_path}'.")

    # Optionally show the image
    if show_image:
        bit_plane_img.show()
