import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from utils.file_operations import load_image, save_image
from utils.undo_redo import UndoRedoManager
from image_processing.basic_operations import rotate_image, resize_image, crop_image
from image_processing.filters import apply_blur
from image_processing.color_adjustments import brightness, contrast, saturation
# Add imports for other operations as needed

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
        
        # Buttons
        tk.Button(self.control_frame, text="Open Image", command=self.open_image).grid(row=0, column=0)
        tk.Button(self.control_frame, text="Save Image", command=self.save_image).grid(row=0, column=1)
        tk.Button(self.control_frame, text="Reset Image", command=self.reset_image).grid(row=0, column=2)
        tk.Button(self.control_frame, text="Undo", command=self.undo).grid(row=3, column=3)
        tk.Button(self.control_frame, text="Redo", command=self.redo).grid(row=3, column=4)
        tk.Button(self.control_frame, text="Blur", command=self.apply_blur).grid(row=2, column=0)
        tk.Button(self.control_frame, text="Rotate", command=self.rotate_image).grid(row=1, column=1)
        tk.Button(self.control_frame, text="Resize", command=self.resize_image).grid(row=1, column=2)
        tk.Button(self.control_frame, text="Crop", command=self.crop_image).grid(row=1, column=3)
        
        # Add new color adjustment buttons
        tk.Button(self.control_frame, text="Brightness +", command=lambda: self.adjust_brightness(1.2)).grid(row=2, column=1)
        tk.Button(self.control_frame, text="Brightness -", command=lambda: self.adjust_brightness(0.8)).grid(row=2, column=2)
        tk.Button(self.control_frame, text="Contrast +", command=lambda: self.adjust_contrast(1.2)).grid(row=2, column=3)
        tk.Button(self.control_frame, text="Contrast -", command=lambda: self.adjust_contrast(0.8)).grid(row=2, column=4)
        tk.Button(self.control_frame, text="Saturation +", command=lambda: self.adjust_saturation(1.2)).grid(row=3, column=0)
        tk.Button(self.control_frame, text="Saturation -", command=lambda: self.adjust_saturation(0.8)).grid(row=3, column=1)
        
        # Image display label
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()
        
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
        display_image = self.image.resize((400, 400), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(display_image)
        self.image_label.configure(image=self.tk_image)
        self.image_label.image = self.tk_image

    def apply_blur(self):
        self.image = apply_blur(self.image)
        self.undo_manager.add_state(self.image.copy())
        self.display_image()

    def rotate_image(self):
        self.image = rotate_image(self.image, 90)  # Rotate 90 degrees
        self.undo_manager.add_state(self.image.copy())
        self.display_image()
        
    def resize_image(self):
        self.image=resize_image(self.image,(8000,8000))
        self.undo_manager.add_state(self.image.copy())
        self.display_image()
    
    def crop_image(self):
        self.image=crop_image(self.image,(15,20,300,350))
        self.undo_manager.add_state(self.image.copy())
        self.display_image()
        
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
