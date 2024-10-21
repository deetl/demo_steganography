# simple_steganography_demo

This collection of tools demonstrates the simplest way to embed data into images using steganography.

1) Basic Idea
The data is embedded into the LSB (least significant bit) of the image's pixels. This causes virtually no visible difference to the image. The first 32 bits (from the first 11 bytes of the image) are used to store the length of the input data. This allows the tool to know how much data to extract when recovering the embedded information.

2) Usage
2.1) Embed
2.2) Extract
2.3) Visualize_LSB

**Caution**:
These tools are intended strictly for educational and demonstration purposes.
- There is no error checking**.
- If you attempt to embed too much data, undefined behavior may occur.
- The output format is the same as the input format. Therefore, if a lossy format is chosen, the embedded data will not survive after saving.
- The tool is deliberately simple, meaning the embedded data can be easily detected.

**Serious Warning**:
These tools are purely for demonstration! You should assume that you may not recover your data, or it might be incomplete, and act accordingly.
