import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtUiTools import QUiLoader
from PyQt6.QtCore import QFile, QIODevice


def load_ui(ui_file_path):
    """Load a UI file and return the main window widget."""
    loader = QUiLoader()
    ui_file = QFile(ui_file_path)
    
    if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
        raise FileNotFoundError(f"Cannot find UI file: {ui_file_path}")
    
    window = loader.load(ui_file)
    ui_file.close()
    
    return window


class MainWindow(QMainWindow):
    """Main application window for Atlas Logger."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface from the UI file."""
        # Get the path to the UI file
        ui_dir = Path(__file__).parent / "ui"
        ui_file = ui_dir / "main.ui"
        
        # Load the UI file
        ui_window = load_ui(str(ui_file))
        
        # Copy properties from loaded UI to this window
        self.setWindowTitle(ui_window.windowTitle())
        self.setGeometry(ui_window.geometry())
        
        # Set the central widget from the loaded UI
        if ui_window.centralWidget():
            self.setCentralWidget(ui_window.centralWidget())
        
        # Transfer menu bar if it exists
        if ui_window.menuBar():
            self.setMenuBar(ui_window.menuBar())
        
        # Transfer status bar if it exists
        if ui_window.statusBar():
            self.setStatusBar(ui_window.statusBar())


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
