from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QStackedWidget, QLabel, QPushButton, QVBoxLayout

from .transcription import AudioStreamer


class ListeningPage(QWidget):
    """Listening Page UI with dynamic text rendering."""

    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.text_fragments = []
        self.audio_thread = None

        # Label for transcribed text
        self.listening_label = QLabel("")
        self.listening_label.setFont(QFont("Arial", 16))
        self.listening_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.listening_label.setWordWrap(True)
        self.listening_label.setStyleSheet("color: white;")

        # Stop button
        self.stop_button = QPushButton("Stop Listening")
        self.stop_button.setFont(QFont("Arial", 14))
        self.stop_button.setStyleSheet("background-color: red; color: white; padding: 10px; border-radius: 8px;")
        self.stop_button.clicked.connect(self.stop_listening)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.listening_label)
        layout.addWidget(self.stop_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")

    def start_listening(self, selected_model: str, **settings):
        """Start audio transcription thread."""
        if self.audio_thread is None or not self.audio_thread.isRunning():
            self.audio_thread = AudioStreamer(selected_model, **settings)
            self.audio_thread.new_text_signal.connect(self.add_text)
            self.audio_thread.start()

    def add_text(self, text):
        """Dynamically add text and remove old parts after a delay."""
        self.text_fragments.append(text)
        self.update_label()

        # Remove this part after 8 seconds
        QTimer.singleShot(8000, lambda: self.remove_text(text))

    def remove_text(self, text):
        """Remove a specific text fragment after timeout."""
        if text in self.text_fragments:
            self.text_fragments.remove(text)
        self.update_label()

    def update_label(self):
        """Update label text."""
        self.listening_label.setText(" ".join(self.text_fragments))

    def stop_listening(self):
        """Stop transcription and clean up."""
        if self.audio_thread:
            self.audio_thread.stop()
            self.audio_thread = None

        self.text_fragments.clear()
        self.update_label()
        self.stacked_widget.setCurrentIndex(0)
