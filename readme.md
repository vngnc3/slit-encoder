# Slit Animation Encoder 🎬

## Overview 📖
This project contains a Python script for creating slit animations. Slit animations are a form of animation where multiple frames are encoded into a single image. A corresponding slit pattern is used to reveal individual frames from the encoded image when it is viewed through the pattern.

## How to Use 🛠️
0. **Install dependencies**: Run `pip install -r requirements.txt`.
1. **Setup**: Place the image sequence you want to encode in a folder and specify its path as `input_directory` in the code.
2. **Run**: Execute the Python script.
3. **Results**: The encoded image, along with the slit pattern, will be saved in `output_directory`.

### Parameters 📝
- `input_directory`: The directory containing the image sequence to be encoded.
- `output_directory`: The directory where the encoded image and slit pattern will be saved.
- `n_slits`: The number of slits in the slit pattern.

## Limitations ⚠️
- **Floating Point Error**: Due to limitations with integer division, the slit pattern may sometimes include a row/column with transparent pixels.
- **Trailing Error**: The last slit in the pattern may be slightly wider than the others, causing a visible error in the rendered canvas.

## License 📄
This project is licensed under the ISC License.