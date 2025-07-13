# SpriteCutter - Image Grid Slicer

A simple, straight forward python GUI application for slicing images into grids. Perfect for creating sprite sheets, cutting up tiled images, or extracting individual tiles from larger images.

Not very fancy, but does exactly what it say's on the tin.  Hopefully it does one simple job well.

## Features

- **Interactive Grid Overlay**: Drag and resize a visual grid over your image
- **Flexible Grid Control**: 
  - Adjust number of rows and columns
  - Set custom cell dimensions (width/height)
  - Maintain aspect ratio for proportional cells
  - Real-time visual feedback
- **Intuitive Controls**:
  - Drag the grid to reposition
  - Drag corners and edges to resize
  - Visual resize handles for precise control
- **Batch Image Export**: Save all grid cells as individual PNG files
- **Smart Naming**: Automatically names files with row/column coordinates

## Installation

1. Make sure you have Python 3.7+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python spritecutter.py
   ```

2. **Load an Image**: Click "Load Image" and select your source image

3. **Position the Grid**: 
   - Drag the red grid overlay to position it over the area you want to slice
   - The grid will show a visual preview of how your image will be cut

4. **Adjust Grid Settings**:
   - **Rows/Columns**: Change the number of grid divisions
   - **Cell Dimensions**: Set exact pixel dimensions for each cell
   - **Aspect Ratio**: Enable to maintain proportional cells when resizing

5. **Resize the Grid**:
   - Drag the corner handles to resize the entire grid
   - Drag edge handles to resize in one direction
   - Hold the grid interior to move without resizing

6. **Save Sliced Images**:
   - Click "Save Sliced Images" 
   - Choose an output directory
   - Images are saved as PNG files with descriptive names (e.g., `image_r00_c00.png`)

## Controls

| Action | Method |
|--------|--------|
| Move Grid | Drag inside the grid area |
| Resize Grid | Drag the corner/edge handles |
| Change Grid Size | Adjust rows/columns spinboxes |
| Set Cell Size | Adjust width/height spinboxes |
| Maintain Proportions | Check "Maintain Aspect Ratio" |

## Output Format

- Images are saved as PNG files for best quality
- Naming convention: `{original_name}_r{row}_c{column}.png`
- Files are organized in a subfolder named `{original_name}_sliced`

## Example Use Cases

- **Sprite Sheets**: Cut game sprites from a larger sheet
- **Tile Maps**: Extract individual tiles from tiled backgrounds
- **Icon Sets**: Separate icons from a grid layout
- **Image Processing**: Batch process sections of large images

## Requirements

- Python 3.7+
- Pillow (PIL) for image processing
- tkinter (usually included with Python)
- tkinter-dnd2 for enhanced drag & drop support

## License

This project is open source. Feel free to modify and distribute as needed.
