import sys

from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication, QVBoxLayout

from pages import FrontPage, ListeningPage , WhisperSettings , ListeningSettings


class MyApp(QWidget):
    """Main application that manages page switching."""

    def __init__(self):
        super().__init__()

        # Stacked widget for managing pages
        self.stacked_widget = QStackedWidget()

        # Create pages
        self.main_page = FrontPage(self.stacked_widget)
        self.whisper_settings_page = WhisperSettings(self.stacked_widget)
        self.listening_page = ListeningPage(self.stacked_widget)
        self.listening_settings_page = ListeningSettings(self.stacked_widget)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.whisper_settings_page)
        self.stacked_widget.addWidget(self.listening_page)
        self.stacked_widget.addWidget(self.listening_settings_page)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle("Whisper Text")
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: #111; color: white;")

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    sys.exit(app.exec())