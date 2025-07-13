#!/usr/bin/env python3
"""
Example script to create a sample sprite sheet for testing SpriteCutter
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_sample_sprite_sheet():
    """Create a sample sprite sheet with numbered tiles"""
    # Create a 400x300 image with a grid of colored squares
    width, height = 400, 300
    rows, cols = 3, 4
    
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Colors for the grid
    colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
        '#FFEAA7', '#DDA0DD', '#98D8E8', '#F7DC6F',
        '#BB8FCE', '#85C1E9', '#82E0AA', '#F8C471'
    ]
    
    cell_width = width // cols
    cell_height = height // rows
    
    tile_num = 0
    for row in range(rows):
        for col in range(cols):
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            
            # Fill rectangle with color
            color = colors[tile_num % len(colors)]
            draw.rectangle([x1, y1, x2, y2], fill=color, outline='black', width=2)
            
            # Add number to tile
            text = str(tile_num + 1)
            # Try to use a font, fall back to default if not available
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            except:
                font = ImageFont.load_default()
                
            # Calculate text position (center of tile)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = x1 + (cell_width - text_width) // 2
            text_y = y1 + (cell_height - text_height) // 2
            
            draw.text((text_x, text_y), text, fill='white', font=font, stroke_width=1, stroke_fill='black')
            
            tile_num += 1
    
    # Save the sample image
    output_path = "sample_sprite_sheet.png"
    image.save(output_path)
    print(f"Sample sprite sheet saved as: {output_path}")
    print(f"Image size: {width}x{height}")
    print(f"Grid: {rows} rows x {cols} columns")
    print(f"Cell size: {cell_width}x{cell_height}")
    print("\nYou can now load this image in SpriteCutter to test the slicing functionality!")
    
    return output_path


if __name__ == "__main__":
    create_sample_sprite_sheet()
