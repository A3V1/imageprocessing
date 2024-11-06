# imageprocessing

setup - install python 

setup - opencv and venv-  https://youtu.be/fclTFQQvQFQ?si=rOlyAJ7PpG9D1Ifu

image_processing_tool/
│
├── main.py                   # Main entry point, handles the program flow
├── image_processing/         # Image processing operations
│   ├── __init__.py
│   ├── basic_operations.py   # Basic image operations like resize, crop, rotate
│   ├── filters.py            # Filters and effects like blur, sharpen
│   ├── color_adjustments.py  # Color adjustments like brightness, contrast
│   ├── edge_detection.py     # Edge detection (Sobel, Canny)
│   ├── histogram_equalization.py # Histogram equalization
│   └── compression.py        # Compression algorithms (DCT, JPEG, etc.)
│
├── ui/                       # User Interface
│   ├── __init__.py
│   ├── tkinter_ui.py         # Tkinter-based UI
│   └── pyqt_ui.py            # (Optional) PyQt5-based UI
│
└── utils/                    # Utility functions
    ├── __init__.py
    ├── file_operations.py    # Load, save, and handle files
    ├── metadata.py           # Extract metadata (EXIF, etc.)
    └── undo_redo.py          # Undo/Redo functionality
