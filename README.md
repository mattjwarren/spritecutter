# SpriteCutter - Image Grid Slicer

A Python GUI application for slicing images into grids with precise control and flexible naming options. Perfect for creating sprite sheets, cutting up tiled images, or extracting individual tiles from larger images.

Simple, intuitive, and does exactly what it says on the tin - hopefully it does one job well.

## 🚀 Quick Start

### Installation
1. **Python 3.7+ Required** (3.8+ recommended)
2. **Clone or Download** this repository
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
```bash
python spritecutter.py
```

## 📖 Usage Guide

### **1. Load Your Image**
- Click **"Load Image"** and select your source image
- Supports: PNG, JPG, JPEG, GIF, BMP, TIFF
- The filename automatically becomes your default prefix

### **2. Configure Your Grid**
- **Rows & Columns**: Use spinboxes to set grid dimensions
- **Cell Dimensions**: Specify exact pixel sizes for precision work
- **Aspect Ratio**: Enable to maintain proportional cells during resize

### **3. Position the Grid**
- **Move**: Drag inside the red grid area
- **Resize**: Drag corner handles for proportional resize
- **Resize Edges**: Drag edge handles for single-direction resize
- **Fine-tune**: Use dimension controls for pixel-perfect positioning

### **4. Customize Output**
- **Filename Prefix**: Edit the text field to customize your output names
- **Naming Scheme**: Choose between:
  - **Row & Column**: `sprite_r00_c00.png` (position-based)
  - **Sequential**: `sprite_001.png` (index-based)

### **5. Save Your Sprites**
- Click **"Save Sliced Images"**
- Choose your output directory (starts from home folder)
- Files are saved directly to your chosen location

## 💾 Output Options

### **Naming Schemes**
```
Row & Column Format:
├── sprite_r00_c00.png  (top-left)
├── sprite_r00_c01.png  (top-center)
├── sprite_r00_c02.png  (top-right)
├── sprite_r01_c00.png  (middle-left)
└── ...

Sequential Format:
├── sprite_001.png
├── sprite_002.png
├── sprite_003.png
└── ...
```

### **File Details**
- **Format**: PNG (lossless compression)

### **Dependencies**
```bash
# Core dependencies
Pillow>=10.0.0          # Image processing
tkinter-dnd2>=0.3.0     # Enhanced drag & drop (optional)

# tkinter is included with most Python installations
```

### **Installation Methods**
```bash
# Method 1: pip install
pip install -r requirements.txt

# Method 2: Individual packages
pip install Pillow tkinter-dnd2

# Method 3: Using virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🤝 Contributing

This project aims to be simple and focused. Contributions are welcome for:

- **Bug fixes** and stability improvements
- **UI/UX enhancements** for better usability  
- **Performance optimizations** for large images
- **Additional file format support**
- **Documentation improvements**

Please keep the core philosophy: *"Do one thing well."*

## 📄 License

This project is open source and available under the MIT License. Feel free to modify, distribute, and use in your projects.

## 🙏 Acknowledgments

Built with:
- **Python & tkinter**
- **Pillow (PIL)**
- **Love for simple, effective tools** 🛠️

---

**SpriteCutter** - Because sometimes you just need to slice an image into a grid, and it should be simple.
