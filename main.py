import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt


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
        
        # Check if UI file exists
        if not ui_file.exists():
            print(f"Error: UI file not found at {ui_file}")
            sys.exit(1)
        
        # Set window properties from UI file metadata
        self.setWindowTitle("MainWindow")
        self.setGeometry(0, 0, 800, 600)
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create a layout for the central widget
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create menu bar
        self.menubar = self.menuBar()
        
        # Create status bar
        self.statusbar = self.statusBar()


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
