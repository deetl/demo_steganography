# Demo tools for simple image steganography

This collection of tools demonstrates the simplest way to embed data into images using steganography. This tools are inspired by the work of Romana Machado and her famous tool [Stego][1]!

# Basic Idea
The data is embedded into the LSB (least significant bit) of the image's pixels. This causes virtually no visible difference to the image. The first 29 bits (from the first 11 bytes of the image) are used to store a Magic Header (STEGO), the correct bit level, the data is stored in and the the length of the input data. This allows the tool to know how much data to extract when recovering the embedded information.

# Tools
## `stego_embed.py` embeds binary data into an image using steganography

## Functionality

This program embeds binary data (e.g., from a file) into an image using steganography. It does this by modifying specific bits of the image's pixel values while leaving the visual appearance of the image almost unchanged. The program allows the user to specify which bit position to embed the data in and also stores metadata (such as a magic marker, bit position, and data length) at the start of the image.

The steps performed by the program are:
1. **Clear the least significant bits (LSBs)** of all pixels up to pixel 29 to prepare for metadata.
2. **Embed a magic marker (`STEGO`)** in the LSBs of the first 14 pixels to identify the image as a stego image.
3. **Store the bit position** (where the data will be embedded) in the LSBs of the next 4 pixels.
4. **Store the length of the binary data** (in bits) in the LSBs of the next 11 pixels.
5. **Embed the actual binary data** in the specified bit position of the remaining pixels.

## Parameters

`-r`, `--read`: The path to the input image file. The default is `image.png`.

`-b`, `--binary`: The path to the  file to be embedded into the image. The default is `input.txt`.

`-w`, `--write`: The path to the output image file. The default is `output_stego.png`. The file will always be saved in PNG format.

`-B`, `--bit`: Specifies the bit position (0-7) in each pixel's color channels where the binary data will be embedded. The default is bit position 0 (the least significant bit or LSB).

### Example Execution

#### Default Execution:
```
#> python stego_embed.py
```
This command will read the default image (`image.png`), embed the default binary file (`input.txt`) into the least significant bit (LSB) of the pixels, and output the stego image as `output_stego.png`.

### Custom Execution with Options:
```
#> python stego_embed.py -r input_image.png -b my_binary_data.bin -w stego_image_output.png -B 3
```
This command does the following:
- Reads `input_image.png`.
- Embeds the file `my_binary_data.bin` into the 3rd bit (bit position 3) of each pixel's RGB channels.
- Outputs the stego image as `stego_image_output.png` (the file will be saved as PNG, even if the input file has a different format). 

## `stego_extract.py` extract data from steganographic image

### Program Description

This Python program extracts binary data embedded in a steganographic image. It specifically checks for a **magic marker** (`STEGO`) in the least significant bits (LSBs) of the first few pixels to confirm the presence of hidden data. Once the marker is detected, the program reads the bit position where the data was embedded, extracts the length of the hidden binary data (in bits), and finally recovers the binary data using the stored bit position. The extracted data is saved in the specified binary file.

### Parameters

`-r`, `--read` (optional): Path to the stego image file from which the data should be extracted. Default is `output_stego.png`.

`-w`, `--write` (optional):  Path to save the extracted  data. Default is `output.txt`.


### Steps in the Program

1. **Magic Marker Verification**:  
   The program first checks the LSBs of the first 14 pixels for the magic marker `STEGO`. If the marker is not found, the program aborts with an error.
   
2. **Bit Position Extraction**:  
   The program extracts the bit position from the next 4 pixels after the magic marker. This bit position indicates which bit plane (0 to 7) was used to embed the data in the image.

3. **Data Length Extraction**:  
   The length of the hidden binary data (in bits) is read from the next 11 pixels (32 bits in total). The program then calculates and displays the length in both bits and bytes.

4. **Data Extraction**:  
   The program uses the extracted bit position to read the hidden data from the image, ensuring that only the stored number of bits is recovered.

5. **Saving the Data**:  
   The extracted binary data is saved to the specified output file.

### Example Execution

#### Default Execution:
```
#> python stego_extract.py
Magic Marker 'STEGO' found.
Bit position: 2
Data length: 2048 bits (256 bytes)
```

The extracted binary data has been saved to 'output.txt'.

#### Custom Input and Output:
```
#> python stego_extract.py -r my_stego_image.png -w my_extracted_data.bin
Magic Marker 'STEGO' found.
Bit position: 2
Data length: 2048 bits (256 bytes)
```
The extracted binary data has been saved to 'my_extracted_data.bin'.

#### Image without magic marker:
```
#> python stego_extract.py -r image.png 
Error: The Magic Marker 'STEGO' was not found. Aborting.
```

## `stego_info.py` check for steganogrphic metadata 

### Functionality

This Python program checks if an image contains embedded data using a steganographic technique. The program looks for a special marker (`STEGO`) in the first few pixels of the image to verify if any hidden data is present. If the `STEGO` marker is found, it extracts and displays the bit position in which the data was embedded and the length of the embedded data in both bits and bytes. If the marker is not found, the program outputs that no embedded data was detected.

1. **Check for the Magic Marker (`STEGO`)**: The program inspects the first 14 pixels of the image to verify if the `STEGO` marker is present.
2. **Extract Bit Position**: If the `STEGO` marker is found, the program reads the next 4 pixels to extract the bit position in which the data was embedded.
3. **Extract Data Length**: The program reads the following 11 pixels to determine the length of the embedded data in bits.
4. **Output**: If the data is found, the program prints the bit position and the size of the embedded data in both bits and bytes. If no data is found, it prints a message saying no embedded data was detected.

### Parameters

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
#> python check_stego_image.py -r my_image_without_data.png
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
