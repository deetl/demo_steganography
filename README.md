# Demo tools for simple image steganography

This collection of tools demonstrates the simplest way to embed data into images using steganography. This tools are inspired by the work of Romana Machado and her famous tool [Stego][1]!

# Basic Idea
The data is embedded into the LSB (least significant bit) of the image's pixels. This causes virtually no visible difference to the image. The first 29 bits (from the first 11 bytes of the image) are used to store a Magic Header (STEGO), the correct bit level, the data is stored in and the the length of the input data. This allows the tool to know how much data to extract when recovering the embedded information.

# Tools
## Embed

## Extract

## `stego_info.py` check for steganogrphic metadata 

### Functionality

This Python program checks if an image contains embedded data using a steganographic technique. The program looks for a special marker (`STEGO`) in the first few pixels of the image to verify if any hidden data is present. If the `STEGO` marker is found, it extracts and displays the bit position in which the data was embedded and the length of the embedded data in both bits and bytes. If the marker is not found, the program outputs that no embedded data was detected.

1. **Check for the Magic Marker (`STEGO`)**: The program inspects the first 14 pixels of the image to verify if the `STEGO` marker is present.
2. **Extract Bit Position**: If the `STEGO` marker is found, the program reads the next 4 pixels to extract the bit position in which the data was embedded.
3. **Extract Data Length**: The program reads the following 11 pixels to determine the length of the embedded data in bits.
4. **Output**: If the data is found, the program prints the bit position and the size of the embedded data in both bits and bytes. If no data is found, it prints a message saying no embedded data was detected.

### Parameters

The program accepts the following command-line arguments:
### Parameters:
`-r`, `--read` (optional): Specifies the path to the image file that should be checked for embedded data. Default is `output_stego.png`.

### Examples

#### Image with embedded data

```
#> python check_stego_image.py
Magic Marker 'STEGO' found. Extracting embedded data details...
Bit position: 3
Data length: 2048 bits (256 bytes)
```

#### Image without embedded data

```
python check_stego_image.py -r my_image_without_data.png
No embedded data found: The Magic Marker 'STEGO' was not found.
```

## `stego_layer.py` Visualize Bitplane

### Functionality:
The program extracts a specific bit plane from the color channels (Red, Green, and Blue) of an image. The bit plane can be selected by the user (between 0 and 7), with the default being bit plane 0 (LSB). The program also offers the option to scale the extracted bit plane to the full 8-bit range (0 or 255) to make the bits in the image more visible. The extracted image can be displayed and saved.

### Parameters:
`-r`, `--read` (optional): Path to the input file (image). Default is `image.png`.

`-w`, `--write` (optional): Path to the output file (image). Default is `output_layer.png`.

`-B`, `--bit` (optional): Specifies the bit plane to be extracted. Range of values: 0 to 7. Default is 0 (LSB).

`-s`, `--show` (optional): Displays the extracted image after processing.

`-n`, `--noscale` (optional): Prevents scaling of the extracted bit plane to the full 8-bit range (0 or 255). With this option, the bits remain in their original brightness scale.

#### Scaling
With scaling: The extracted bit plane is scaled to black (0) or white (255), making the bits more visible in the display.

Without scaling (`-n`): The bits in the plane remain in their original form, which means they may appear darker, especially in lower bit planes.

### Examples
#### Default execution

```python extract_bit_plane.py```

Extracts the LSB bit plane (bit 0) from the image `image.png`, scales the bits to 0 or 255, and saves the result as `bit_plane_0.png`.

#### With custom bit plane and no scaling:

```python extract_bit_plane.py -r my_image.png -B 5 -n```

Extracts bit plane 5 from `my_image.png`, suppresses bit scaling, and saves the result as `bit_plane_5.png`.

#### With image display

```python extract_bit_plane.py -r my_image.png -B 2 -S```

Extracts bit plane 2 from `my_image.png`, saves the image as `bit_plane_2.png`, and displays it afterward.

# Use in lectures

**Caution**:
These tools are intended strictly for educational and demonstration purposes.
- There is only a little bit of error checking.
- If you attempt to embed too much data, undefined behavior may occur.
- The tool is deliberately simple, meaning the embedded data can be easily detected.

**Serious Warning**:
These tools are purely for demonstration! You should assume that you may not recover your data, or it might be incomplete, and act accordingly.

[1]: https://ftp.funet.fi/pub/crypt/old/ghost/Stego1a2.Readme
