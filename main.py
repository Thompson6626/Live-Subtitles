from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication, QVBoxLayout, QSizePolicy
import sys
from pages import FrontPage, WhisperSettings, ListeningSettings


class MyApp(QWidget):
    """Main application that manages page switching."""

    def __init__(self):
        super().__init__()

        # Stacked widget for managing pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.currentChanged.connect(self.update_size)  # Listen for page changes

        # Create pages
        self.main_page = FrontPage(self.stacked_widget)
        self.main_page.setFixedSize(500, 300)

        self.whisper_settings_page = WhisperSettings(self.stacked_widget)
        self.whisper_settings_page.setMinimumSize(500,300)

        self.listening_settings_page = ListeningSettings(self.stacked_widget)

        # Ensure different pages have proper minimum sizes
        self.listening_settings_page.setMinimumSize(979, 556)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.whisper_settings_page)
        self.stacked_widget.addWidget(self.listening_settings_page)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle("Whisper Text")
        self.setStyleSheet("background-color: #111; color: white;")

        # Show first page and adjust size accordingly
        self.update_size(0)

    def update_size(self, index: int):
        """Resize window to fit the current page."""
        current_widget = self.stacked_widget.widget(index)
        if current_widget.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Fixed and \
                current_widget.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Fixed:
            self.setFixedSize(current_widget.size().width(), current_widget.size().height())
            self.adjustSize()
            return
        self.setFixedSize(0,0)

        if current_widget.maximumSize() != QSize(0,0):
            self.setMaximumSize(current_widget.maximumSize().width(), current_widget.maximumSize().height())
        if current_widget.minimumSize() != QSize(0,0):
            self.setMinimumSize(current_widget.minimumSize().width(), current_widget.minimumSize().height())
        self.adjustSize()

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    sys.exit(app.exec())
