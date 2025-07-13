"""
SpriteCutter - A GUI application for slicing images into grids
Allows users to drag a resizable grid across an image and slice it into multiple images.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import math


class SpriteCutter:
    def __init__(self, root):
        self.root = root
        self.root.title("SpriteCutter - Image Grid Slicer")
        self.root.geometry("1200x800")
        
        # Initialize variables
        self.image = None
        self.display_image = None
        self.canvas_image = None
        self.image_scale = 1.0
        self.grid_x = 50
        self.grid_y = 50
        self.grid_width = 200
        self.grid_height = 200
        self.dragging = False
        self.resize_mode = None
        self.last_x = 0
        self.last_y = 0
        
        # Grid settings
        self.rows = tk.IntVar(value=2)
        self.cols = tk.IntVar(value=2)
        self.cell_width = tk.IntVar(value=100)
        self.cell_height = tk.IntVar(value=100)
        self.maintain_aspect = tk.BooleanVar(value=False)
        self.aspect_ratio = tk.DoubleVar(value=1.0)
        
        # File naming
        self.filename_prefix = tk.StringVar(value="sprite")
        self.naming_scheme = tk.StringVar(value="row_col")  # "row_col" or "sequential"
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control panel on the left
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Image canvas on the right
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_controls(control_frame)
        self.setup_canvas(canvas_frame)
        
    def setup_controls(self, parent):
        """Set up the control panel"""
        # File operations
        file_frame = ttk.LabelFrame(parent, text="File Operations", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="Load Image", command=self.load_image).pack(fill=tk.X, pady=2)
        
        # Filename prefix
        prefix_frame = ttk.Frame(file_frame)
        prefix_frame.pack(fill=tk.X, pady=2)
        ttk.Label(prefix_frame, text="Filename Prefix:").pack(side=tk.LEFT)
        prefix_entry = ttk.Entry(prefix_frame, textvariable=self.filename_prefix, width=15)
        prefix_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Helper text for prefix
        prefix_help = ttk.Label(file_frame, text="(Custom name for saved files)", 
                               font=('TkDefaultFont', 8), foreground='gray')
        prefix_help.pack(fill=tk.X, pady=(0, 5))
        
        # Naming scheme options
        naming_frame = ttk.LabelFrame(file_frame, text="File Naming", padding=5)
        naming_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Radiobutton(naming_frame, text="Row & Column (prefix_r00_c00.png)", 
                       variable=self.naming_scheme, value="row_col").pack(anchor=tk.W)
        ttk.Radiobutton(naming_frame, text="Sequential Number (prefix_001.png)", 
                       variable=self.naming_scheme, value="sequential").pack(anchor=tk.W)
        
        ttk.Button(file_frame, text="Save Sliced Images", command=self.save_sliced_images).pack(fill=tk.X, pady=2)
        
        # Grid settings
        grid_frame = ttk.LabelFrame(parent, text="Grid Settings", padding=10)
        grid_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rows and columns
        ttk.Label(grid_frame, text="Rows:").grid(row=0, column=0, sticky=tk.W, pady=2)
        rows_spin = ttk.Spinbox(grid_frame, from_=1, to=50, textvariable=self.rows, width=10, command=self.update_grid)
        rows_spin.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        rows_spin.bind('<KeyRelease>', lambda e: self.root.after(100, self.update_grid))
        
        ttk.Label(grid_frame, text="Columns:").grid(row=1, column=0, sticky=tk.W, pady=2)
        cols_spin = ttk.Spinbox(grid_frame, from_=1, to=50, textvariable=self.cols, width=10, command=self.update_grid)
        cols_spin.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        cols_spin.bind('<KeyRelease>', lambda e: self.root.after(100, self.update_grid))
        
        # Cell dimensions
        ttk.Separator(grid_frame, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)
        
        ttk.Label(grid_frame, text="Cell Width:").grid(row=3, column=0, sticky=tk.W, pady=2)
        width_spin = ttk.Spinbox(grid_frame, from_=1, to=1000, textvariable=self.cell_width, width=10, command=self.update_grid_size)
        width_spin.grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        width_spin.bind('<KeyRelease>', lambda e: self.root.after(100, self.update_grid_size))
        
        ttk.Label(grid_frame, text="Cell Height:").grid(row=4, column=0, sticky=tk.W, pady=2)
        height_spin = ttk.Spinbox(grid_frame, from_=1, to=1000, textvariable=self.cell_height, width=10, command=self.update_grid_size)
        height_spin.grid(row=4, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        height_spin.bind('<KeyRelease>', lambda e: self.root.after(100, self.update_grid_size))
        
        # Aspect ratio
        ttk.Separator(grid_frame, orient='horizontal').grid(row=5, column=0, columnspan=2, sticky='ew', pady=10)
        
        aspect_check = ttk.Checkbutton(grid_frame, text="Maintain Aspect Ratio", variable=self.maintain_aspect, command=self.toggle_aspect_ratio)
        aspect_check.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        ttk.Label(grid_frame, text="Aspect Ratio:").grid(row=7, column=0, sticky=tk.W, pady=2)
        aspect_spin = ttk.Spinbox(grid_frame, from_=0.1, to=10.0, increment=0.1, textvariable=self.aspect_ratio, width=10, command=self.update_aspect_ratio)
        aspect_spin.grid(row=7, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        aspect_spin.bind('<KeyRelease>', lambda e: self.root.after(100, self.update_aspect_ratio))
        
        # Grid position info
        info_frame = ttk.LabelFrame(parent, text="Grid Info", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_label = ttk.Label(info_frame, text="No image loaded", wraplength=200)
        self.info_label.pack()
        
        # Instructions
        instructions_frame = ttk.LabelFrame(parent, text="Instructions", padding=10)
        instructions_frame.pack(fill=tk.X)
        
        instructions = """
• Load an image to start
• Drag the grid to reposition
• Drag corners/edges to resize
• Adjust rows/columns as needed
• Set cell dimensions manually
• Use aspect ratio for proportional cells
• Customize filename prefix for output
• Save to slice the image
        """
        ttk.Label(instructions_frame, text=instructions.strip(), justify=tk.LEFT, wraplength=200).pack()
        
    def setup_canvas(self, parent):
        """Set up the image canvas"""
        # Create canvas with scrollbars
        canvas_container = ttk.Frame(parent)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_container, bg='white', cursor='cross')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)
        self.canvas.bind('<Motion>', self.on_canvas_motion)
        
    def load_image(self):
        """Load an image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.image = Image.open(file_path)
                # Only update filename prefix if it's empty or still has the default value
                current_prefix = self.filename_prefix.get().strip()
                if not current_prefix or current_prefix == "sprite":
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    self.filename_prefix.set(base_name)
                self.display_image_on_canvas()
                self.update_info()
                messagebox.showinfo("Success", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                
    def display_image_on_canvas(self):
        """Display the image on the canvas"""
        if not self.image:
            return
            
        # Calculate scale to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not ready, try again later
            self.root.after(100, self.display_image_on_canvas)
            return
            
        img_width, img_height = self.image.size
        
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        self.image_scale = min(scale_x, scale_y, 1.0)  # Don't scale up
        
        # Resize image for display
        display_width = int(img_width * self.image_scale)
        display_height = int(img_height * self.image_scale)
        
        self.display_image = self.image.resize((display_width, display_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.display_image)
        
        # Clear canvas and add image
        self.canvas.delete("all")
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # Update canvas scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Initialize grid position and size
        self.grid_x = 50
        self.grid_y = 50
        self.grid_width = min(200, display_width - 100)
        self.grid_height = min(200, display_height - 100)
        
        # Update cell dimensions based on current grid
        self.update_cell_dimensions_from_grid()
        self.draw_grid()
        
    def update_cell_dimensions_from_grid(self):
        """Update cell dimension variables based on current grid size"""
        if self.rows.get() > 0 and self.cols.get() > 0:
            self.cell_width.set(int(self.grid_width / self.cols.get()))
            self.cell_height.set(int(self.grid_height / self.rows.get()))
            
            # Update aspect ratio
            if self.cell_width.get() > 0:
                self.aspect_ratio.set(round(self.cell_height.get() / self.cell_width.get(), 2))
                
    def update_grid(self):
        """Update grid based on rows/columns change"""
        if self.maintain_aspect.get():
            # Maintain aspect ratio when changing grid
            self.update_grid_size_with_aspect()
        else:
            self.update_cell_dimensions_from_grid()
        self.draw_grid()
        self.update_info()
        
    def update_grid_size(self):
        """Update grid size based on cell dimensions"""
        self.grid_width = self.cell_width.get() * self.cols.get()
        self.grid_height = self.cell_height.get() * self.rows.get()
        
        if self.maintain_aspect.get() and self.cell_width.get() > 0:
            self.aspect_ratio.set(round(self.cell_height.get() / self.cell_width.get(), 2))
            
        self.draw_grid()
        self.update_info()
        
    def toggle_aspect_ratio(self):
        """Toggle aspect ratio maintenance"""
        if self.maintain_aspect.get() and self.cell_width.get() > 0:
            self.aspect_ratio.set(round(self.cell_height.get() / self.cell_width.get(), 2))
            
    def update_aspect_ratio(self):
        """Update grid based on aspect ratio change"""
        if self.maintain_aspect.get():
            self.update_grid_size_with_aspect()
            
    def update_grid_size_with_aspect(self):
        """Update grid size maintaining aspect ratio"""
        if self.maintain_aspect.get():
            new_height = int(self.cell_width.get() * self.aspect_ratio.get())
            self.cell_height.set(new_height)
            self.grid_width = self.cell_width.get() * self.cols.get()
            self.grid_height = self.cell_height.get() * self.rows.get()
            self.draw_grid()
            self.update_info()
        
    def draw_grid(self):
        """Draw the grid overlay on the canvas"""
        if not self.display_image:
            return
            
        # Remove existing grid
        self.canvas.delete("grid")
        
        # Draw grid rectangle
        x1, y1 = self.grid_x, self.grid_y
        x2, y2 = self.grid_x + self.grid_width, self.grid_y + self.grid_height
        
        # Main grid outline
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=2, tags="grid")
        
        # Grid lines
        rows = self.rows.get()
        cols = self.cols.get()
        
        # Vertical lines
        for i in range(1, cols):
            x = x1 + (i * self.grid_width / cols)
            self.canvas.create_line(x, y1, x, y2, fill='red', width=1, tags="grid")
            
        # Horizontal lines
        for i in range(1, rows):
            y = y1 + (i * self.grid_height / rows)
            self.canvas.create_line(x1, y, x2, y, fill='red', width=1, tags="grid")
            
        # Resize handles
        handle_size = 8
        handles = [
            (x1 - handle_size//2, y1 - handle_size//2, "nw"),  # Top-left
            (x2 - handle_size//2, y1 - handle_size//2, "ne"),  # Top-right
            (x1 - handle_size//2, y2 - handle_size//2, "sw"),  # Bottom-left
            (x2 - handle_size//2, y2 - handle_size//2, "se"),  # Bottom-right
            ((x1 + x2)//2 - handle_size//2, y1 - handle_size//2, "n"),   # Top
            ((x1 + x2)//2 - handle_size//2, y2 - handle_size//2, "s"),   # Bottom
            (x1 - handle_size//2, (y1 + y2)//2 - handle_size//2, "w"),   # Left
            (x2 - handle_size//2, (y1 + y2)//2 - handle_size//2, "e"),   # Right
        ]
        
        for hx, hy, cursor in handles:
            self.canvas.create_rectangle(
                hx, hy, hx + handle_size, hy + handle_size,
                fill='red', outline='darkred', width=1,
                tags=("grid", f"handle_{cursor}")
            )
            
    def on_canvas_click(self, event):
        """Handle canvas click events"""
        if not self.display_image:
            return
            
        self.last_x = event.x
        self.last_y = event.y
        
        # Check if clicking on a resize handle
        clicked_items = self.canvas.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
        
        self.resize_mode = None
        for item in clicked_items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag.startswith("handle_"):
                    self.resize_mode = tag.replace("handle_", "")
                    self.dragging = True
                    return
                    
        # Check if clicking inside grid for moving
        if (self.grid_x <= event.x <= self.grid_x + self.grid_width and
            self.grid_y <= event.y <= self.grid_y + self.grid_height):
            self.dragging = True
            self.resize_mode = "move"
            
    def on_canvas_drag(self, event):
        """Handle canvas drag events"""
        if not self.dragging or not self.display_image:
            return
            
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        
        if self.resize_mode == "move":
            # Move the grid
            self.grid_x += dx
            self.grid_y += dy
            
            # Keep grid within image bounds
            img_width = self.display_image.width
            img_height = self.display_image.height
            
            self.grid_x = max(0, min(self.grid_x, img_width - self.grid_width))
            self.grid_y = max(0, min(self.grid_y, img_height - self.grid_height))
            
        elif self.resize_mode:
            # Resize the grid
            old_x, old_y = self.grid_x, self.grid_y
            old_w, old_h = self.grid_width, self.grid_height
            
            if 'n' in self.resize_mode:  # North
                self.grid_y += dy
                self.grid_height -= dy
            if 's' in self.resize_mode:  # South
                self.grid_height += dy
            if 'w' in self.resize_mode:  # West
                self.grid_x += dx
                self.grid_width -= dx
            if 'e' in self.resize_mode:  # East
                self.grid_width += dx
                
            # Maintain minimum size
            min_size = 50
            if self.grid_width < min_size:
                self.grid_x = old_x
                self.grid_width = old_w
            if self.grid_height < min_size:
                self.grid_y = old_y
                self.grid_height = old_h
                
            # Maintain aspect ratio if enabled
            if self.maintain_aspect.get() and self.resize_mode in ['se', 'nw', 'sw', 'ne']:
                if abs(dx) > abs(dy):
                    self.grid_height = int(self.grid_width * self.aspect_ratio.get())
                else:
                    self.grid_width = int(self.grid_height / self.aspect_ratio.get())
                    
            # Update cell dimensions
            self.update_cell_dimensions_from_grid()
            
        self.last_x = event.x
        self.last_y = event.y
        
        self.draw_grid()
        self.update_info()
        
    def on_canvas_release(self, event):
        """Handle canvas button release"""
        self.dragging = False
        self.resize_mode = None
        
    def on_canvas_motion(self, event):
        """Handle canvas mouse motion for cursor changes"""
        if not self.display_image or self.dragging:
            return
            
        # Check if hovering over resize handles
        items = self.canvas.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
        
        cursor = 'cross'
        for item in items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag.startswith("handle_"):
                    direction = tag.replace("handle_", "")
                    cursor_map = {
                        'nw': 'top_left_corner', 'se': 'bottom_right_corner',
                        'ne': 'top_right_corner', 'sw': 'bottom_left_corner',
                        'n': 'top_side', 's': 'bottom_side',
                        'w': 'left_side', 'e': 'right_side'
                    }
                    cursor = cursor_map.get(direction, 'cross')
                    break
                    
        # Check if inside grid
        if (cursor == 'cross' and 
            self.grid_x <= event.x <= self.grid_x + self.grid_width and
            self.grid_y <= event.y <= self.grid_y + self.grid_height):
            cursor = 'fleur'
            
        self.canvas.configure(cursor=cursor)
        
    def update_info(self):
        """Update the info label"""
        if not self.image:
            self.info_label.config(text="No image loaded")
            return
            
        # Calculate actual pixel coordinates and sizes
        scale_factor = 1.0 / self.image_scale if self.image_scale > 0 else 1.0
        
        actual_x = int(self.grid_x * scale_factor)
        actual_y = int(self.grid_y * scale_factor)
        actual_w = int(self.grid_width * scale_factor)
        actual_h = int(self.grid_height * scale_factor)
        
        cell_w = actual_w // self.cols.get()
        cell_h = actual_h // self.rows.get()
        
        info_text = f"""Image: {self.image.width}×{self.image.height}
Grid: {actual_x},{actual_y} ({actual_w}×{actual_h})
Cells: {self.rows.get()}×{self.cols.get()} ({cell_w}×{cell_h} each)
Total sprites: {self.rows.get() * self.cols.get()}"""
        
        self.info_label.config(text=info_text)
        
    def save_sliced_images(self):
        """Save the sliced images to a folder"""
        if not self.image:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        # Choose output directory
        output_dir = filedialog.askdirectory(
            title="Select Directory to Save Sliced Images",
            initialdir=os.path.expanduser("~")  # Start from user's home directory
        )
        if not output_dir:
            return
            
        try:
            # Calculate actual coordinates
            scale_factor = 1.0 / self.image_scale if self.image_scale > 0 else 1.0
            
            actual_x = int(self.grid_x * scale_factor)
            actual_y = int(self.grid_y * scale_factor)
            actual_w = int(self.grid_width * scale_factor)
            actual_h = int(self.grid_height * scale_factor)
            
            cell_w = actual_w // self.cols.get()
            cell_h = actual_h // self.rows.get()
            
            # Get the filename prefix
            prefix = self.filename_prefix.get().strip()
            if not prefix:
                prefix = "sprite"  # Default fallback
            
            # Slice and save images directly to the selected directory
            saved_count = 0
            image_index = 1  # For sequential numbering
            
            for row in range(self.rows.get()):
                for col in range(self.cols.get()):
                    # Calculate crop box
                    left = actual_x + col * cell_w
                    top = actual_y + row * cell_h
                    right = left + cell_w
                    bottom = top + cell_h
                    
                    # Ensure we don't go beyond image boundaries
                    right = min(right, self.image.width)
                    bottom = min(bottom, self.image.height)
                    
                    if left < self.image.width and top < self.image.height:
                        # Crop and save
                        cropped = self.image.crop((left, top, right, bottom))
                        
                        # Generate filename based on selected naming scheme
                        if self.naming_scheme.get() == "sequential":
                            # Sequential numbering: prefix_001.png, prefix_002.png, etc.
                            total_images = self.rows.get() * self.cols.get()
                            digits = len(str(total_images))  # Calculate needed digits
                            filename = f"{prefix}_{image_index:0{digits}d}.png"
                            image_index += 1
                        else:
                            # Row and column: prefix_r00_c00.png (default)
                            filename = f"{prefix}_r{row:02d}_c{col:02d}.png"
                            
                        filepath = os.path.join(output_dir, filename)
                        cropped.save(filepath, "PNG")
                        saved_count += 1
                        
            # Show success message with appropriate example
            if self.naming_scheme.get() == "sequential":
                total_images = self.rows.get() * self.cols.get()
                digits = len(str(total_images))
                example = f"{prefix}_{'1'.zfill(digits)}.png, {prefix}_{'2'.zfill(digits)}.png, etc."
            else:
                example = f"{prefix}_r00_c00.png, {prefix}_r00_c01.png, etc."
                
            messagebox.showinfo("Success", 
                              f"Saved {saved_count} images to:\n{output_dir}\n\nFiles named: {example}")
                              
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save images: {str(e)}")


def main():
    root = tk.Tk()
    app = SpriteCutter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
