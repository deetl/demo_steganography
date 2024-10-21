# simple_steganography_demo

This collection of tools demonstrates the simplest way to embed data into images using steganography. This tools are inspired by the work of Romana Machado and her famous tool [Stego][1]!

1) Basic Idea
The data is embedded into the LSB (least significant bit) of the image's pixels. This causes virtually no visible difference to the image. The first 32 bits (from the first 11 bytes of the image) are used to store the length of the input data. This allows the tool to know how much data to extract when recovering the embedded information.

2) Usage
    1) Embed

    2) Extract

    3) Visualize LSB
       
3) Use in lectures

**Caution**:
These tools are intended strictly for educational and demonstration purposes.
- There is only a little bit of error checking.
- If you attempt to embed too much data, undefined behavior may occur.
- The tool is deliberately simple, meaning the embedded data can be easily detected.

**Serious Warning**:
These tools are purely for demonstration! You should assume that you may not recover your data, or it might be incomplete, and act accordingly.

[1]: https://ftp.funet.fi/pub/crypt/old/ghost/Stego1a2.Readme
