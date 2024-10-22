# simple_steganography_demo

This collection of tools demonstrates the simplest way to embed data into images using steganography. This tools are inspired by the work of Romana Machado and her famous tool [Stego][1]!

# Basic Idea
The data is embedded into the LSB (least significant bit) of the image's pixels. This causes virtually no visible difference to the image. The first 29 bits (from the first 11 bytes of the image) are used to store a Magic Header (STEGO), the correct bit level, the data is stored in and the the length of the input data. This allows the tool to know how much data to extract when recovering the embedded information.

# Usage
## Embed

## Extract

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
