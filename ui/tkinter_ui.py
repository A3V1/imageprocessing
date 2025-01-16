import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Text
from PIL import Image, ImageTk
from utils.file_operations import load_image, save_image
from utils.undo_redo import UndoRedoManager
from image_processing.basic_operations import rotate_image, resize_image, crop_image
from image_processing.filters import apply_blur
from image_processing.color_adjustments import brightness, contrast, saturation
from image_processing.compression import compress_image, compress_image_size
from image_processing.histogram_equalization import histogram_equalization  # Import histogram equalization
from image_processing.edge_detection import find_edges  # Import edge detection
from utils.metadata import get_image_metadata  # Import the metadata function

class TkinterUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Processing Tool")
        
        # Image variables and undo/redo manager
        self.image = None
        self.original_image = None
        self.undo_manager = UndoRedoManager()
        
        # Layout frames
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack()
        
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()
        
        # File operation buttons
        tk.Button(self.control_frame, text="Open Image", command=self.open_image).grid(row=0, column=0)
        tk.Button(self.control_frame, text="Save Image", command=self.save_image).grid(row=0, column=1)
        tk.Button(self.control_frame, text="Reset Image", command=self.reset_image).grid(row=0, column=2)
        
        # Add a button to display metadata
        tk.Button(self.control_frame, text="Show Metadata", command=self.show_metadata).grid(row=0, column=3)
        
        # Basic operation buttons
        tk.Button(self.control_frame, text="Blur", command=self.apply_blur).grid(row=2, column=0)
        tk.Button(self.control_frame, text="Rotate", command=self.rotate_image).grid(row=1, column=1)
        tk.Button(self.control_frame, text="Resize", command=self.resize_image).grid(row=1, column=2)
        tk.Button(self.control_frame, text="Crop", command=self.start_crop).grid(row=1, column=3)
        
        # Add buttons for histogram equalization and edge detection
        tk.Button(self.control_frame, text="Histogram Equalization", command=self.apply_histogram_equalization).grid(row=2, column=1)
        tk.Button(self.control_frame, text="Edge Detection", command=self.apply_edge_detection).grid(row=2, column=2)
        
        # Color adjustment buttons
        tk.Button(self.control_frame, text="Brightness +", command=lambda: self.adjust_brightness(1.2)).grid(row=3, column=0)
        tk.Button(self.control_frame, text="Brightness -", command=lambda: self.adjust_brightness(0.8)).grid(row=3, column=1)
        tk.Button(self.control_frame, text="Contrast +", command=lambda: self.adjust_contrast(1.2)).grid(row=3, column=2)
        tk.Button(self.control_frame, text="Contrast -", command=lambda: self.adjust_contrast(0.8)).grid(row=3, column=3)
        tk.Button(self.control_frame, text="Saturation +", command=lambda: self.adjust_saturation(1.2)).grid(row=4, column=0)
        tk.Button(self.control_frame, text="Saturation -", command=lambda: self.adjust_saturation(0.8)).grid(row=4, column=1)
        
        # Compression buttons and controls
        tk.Label(self.control_frame, text="Quality:").grid(row=5, column=0)
        self.quality_var = tk.Scale(self.control_frame, from_=1, to=100, orient='horizontal')
        self.quality_var.set(85)
        self.quality_var.grid(row=5, column=1, columnspan=2)
        
        tk.Label(self.control_frame, text="Size (KB):").grid(row=5, column=3)
        self.size_var = tk.Entry(self.control_frame, width=10)
        self.size_var.insert(0, "500")
        self.size_var.grid(row=5, column=4)
        
        tk.Button(self.control_frame, text="Compress Quality", command=self.compress_quality).grid(row=6, column=1)
        tk.Button(self.control_frame, text="Compress Size", command=self.compress_size).grid(row=6, column=2)
        
        # Undo/Redo buttons
        tk.Button(self.control_frame, text="Undo", command=self.undo).grid(row=4, column=3)
        tk.Button(self.control_frame, text="Redo", command=self.redo).grid(row=4, column=4)
        
        # Image display label
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()
        
        # Add these crop mode variables
        self.crop_mode = False
        self.crop_start = None
        self.crop_rect = None
        
        # Add mouse event bindings for crop
        self.image_label.bind('<Button-1>', self.start_crop)
        self.image_label.bind('<B1-Motion>', self.update_crop)
        self.image_label.bind('<ButtonRelease-1>', self.end_crop)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = load_image(file_path)
            self.original_image = self.image.copy()
            self.undo_manager.reset()
            self.undo_manager.add_state(self.image.copy())  # Add initial state
            self.display_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            save_image(self.image, file_path)

    def reset_image(self):
        if self.original_image:
            self.image = self.original_image.copy()
            self.undo_manager.reset()
            self.undo_manager.add_state(self.image.copy())
            self.display_image()

    def display_image(self):
        if self.image:
            # Calculate scaling to fit in 400x400 while maintaining aspect ratio
            display_size = (400, 400)
            image_ratio = self.image.width / self.image.height
            if image_ratio > 1:
                display_size = (400, int(400 / image_ratio))
            else:
                display_size = (int(400 * image_ratio), 400)
            
            display_image = self.image.resize(display_size, Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(display_image)
            self.image_label.configure(image=self.tk_image)
            self.image_label.image = self.tk_image
            
            # Draw the cropping rectangle if in crop mode
            if self.crop_rect:
                self.image_label.create_rectangle(
                    self.crop_rect[0], self.crop_rect[1],
                    self.crop_rect[2], self.crop_rect[3],
                    outline="red", width=2
                )

    def apply_blur(self):
        self.image = apply_blur(self.image)
        self.undo_manager.add_state(self.image.copy())
        self.display_image()

    def rotate_image(self):
        self.image = rotate_image(self.image, 90)  # Rotate 90 degrees
        self.undo_manager.add_state(self.image.copy())
        self.display_image()
        
    def resize_image(self):
        self.image = resize_image(self.image, (8000, 8000))
        self.undo_manager.add_state(self.image.copy())
        self.display_image()
    
    def start_crop(self, event):
        if self.image:
            self.crop_mode = True
            self.crop_start = (event.x, event.y)
            self.crop_rect = [event.x, event.y, event.x, event.y]  # Initialize rectangle

    def update_crop(self, event):
        if self.crop_mode and self.crop_start and self.image:
            self.crop_rect[2] = event.x  # Update right
            self.crop_rect[3] = event.y  # Update bottom
            self.display_image()  # Redraw the image with the updated rectangle

    def end_crop(self, event):
        if self.crop_mode and self.crop_start and self.image:
            # Convert display coordinates to original image coordinates
            display_width = self.image_label.winfo_width()
            display_height = self.image_label.winfo_height()
            
            scale_x = self.image.width / display_width
            scale_y = self.image.height / display_height
            
            left = min(self.crop_start[0], event.x) * scale_x
            top = min(self.crop_start[1], event.y) * scale_y
            right = max(self.crop_start[0], event.x) * scale_x
            bottom = max(self.crop_start[1], event.y) * scale_y
            
            # Apply crop
            self.image = crop_image(self.image, (int(left), int(top), int(right), int(bottom)))
            self.undo_manager.add_state(self.image.copy())
            self.display_image()
            
            # Reset crop mode
            self.crop_mode = False
            self.crop_start = None
            self.crop_rect = None

    def undo(self):
        previous_state = self.undo_manager.undo()
        if previous_state:
            self.image = previous_state
            self.display_image()

    def redo(self):
        next_state = self.undo_manager.redo()
        if next_state:
            self.image = next_state
            self.display_image()
        
    def adjust_brightness(self, factor):
        if self.image:
            self.image = brightness(self.image, factor)
            self.undo_manager.add_state(self.image.copy())
            self.display_image()

    def adjust_contrast(self, factor):
        if self.image:
            self.image = contrast(self.image, factor)
            self.undo_manager.add_state(self.image.copy())
            self.display_image()

    def adjust_saturation(self, factor):
        if self.image:
            self.image = saturation(self.image, factor)
            self.undo_manager.add_state(self.image.copy())
            self.display_image()
        
    def compress_quality(self):
        if self.image:
            quality = self.quality_var.get()
            self.image = compress_image(self.image, quality=quality)
            self.undo_manager.add_state(self.image.copy())
            self.display_image()
            messagebox.showinfo("Compression", f"Image compressed with quality {quality}")

    def compress_size(self):
        if self.image:
            try:
                target_size = int(self.size_var.get())
                self.image = compress_image_size(self.image, max_size_kb=target_size)
                self.undo_manager.add_state(self.image.copy())
                self.display_image()
                messagebox.showinfo("Compression", f"Image compressed to target size {target_size}KB")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid target size")

    def show_metadata(self):
        if self.image:
            metadata = get_image_metadata(self.image)
            metadata_window = Toplevel(self.root)
            metadata_window.title("Image Metadata")
            metadata_window.geometry("300x400")
            
            text_widget = Text(metadata_window, wrap=tk.WORD)
            text_widget.pack(expand=True, fill='both')
            
            for key, value in metadata.items():
                text_widget.insert(tk.END, f"{key}: {value}\n")
            
            text_widget.config(state='disabled')  # Make read-only

    def apply_histogram_equalization(self):
        if self.image:
            self.image = histogram_equalization(self.image)
            self.undo_manager.add_state(self.image.copy())
            self.display_image()

    def apply_edge_detection(self):
        if self.image:
            self.image = find_edges(self.image)
            self.undo_manager.add_state(self.image.copy())
            self.display_image()

    def run(self):
        self.root.mainloop()

class UndoRedoManager:
    def __init__(self):
        self.history = []  # To store the history of states
        self.current_state = -1  # To track the current state index
    
    def add_state(self, state):
        self.history = self.history[:self.current_state + 1]
        self.history.append(state)
        self.current_state += 1

    def undo(self):
        if self.current_state > 0:
            self.current_state -= 1
            return self.history[self.current_state]
        return None
    
    def redo(self):
        if self.current_state < len(self.history) - 1:
            self.current_state += 1
            return self.history[self.current_state]
        return None
    
    def reset(self):
        self.history = []
        self.current_state = -1

# Initialize and run the UI
if __name__ == "__main__":
    app = TkinterUI()
    app.run()
