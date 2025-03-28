from typing import Dict, Union

from PyQt6.QtCore import QTimer, Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QMouseEvent, QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

from .transcription import AudioStreamer


class ListeningPage(QWidget):
    """Listening Page UI with dynamic text rendering and resizable behavior."""

    RESIZE_MARGIN = 10  # Margin for detecting resize edges
    stopped = pyqtSignal()

    def __init__(
            self,
            selected_model: str,
            listening_settings: Dict[str, Union[Dict[str, int], int, bool]],
            **whisper_settings
    ):
        super().__init__()
        self.text_fragments = []
        self.audio_thread = None
        self.selected_model = selected_model
        self.whisper_settings = whisper_settings
        self.dragging = False
        self.resizing = False
        self.drag_position = QPoint()

        # Label for transcribed text
        self.listening_label = QLabel("")
        self.listening_label.setFont(QFont("Arial", 16))
        self.listening_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.listening_label.setWordWrap(True)
        self.listening_label.setStyleSheet("color: white;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.listening_label)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")
        self.setMinimumSize(200, 100)  # Prevent excessive shrinking

        self.apply_settings(listening_settings)
        self.start_listening()

    def start_listening(self):
        """Start audio transcription thread."""
        if self.audio_thread is None or not self.audio_thread.isRunning():
            self.audio_thread = AudioStreamer(self.selected_model, **self.whisper_settings)
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
        self.stopped.emit()
        self.close()

    def apply_settings(self, settings: Dict[str, Union[Dict[str, int], int, bool]]):
        """Apply UI settings such as colors and window behavior."""
        if settings["frameless"]:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        else:
            self.setWindowFlags(Qt.WindowType.Window)  # Allow resizing when not frameless

        text_rgba = f"rgba({settings['text_color']['r']}, {settings['text_color']['g']}, {settings['text_color']['b']}, {settings['text_alpha'] / 255})"
        bg_rgba = f"rgba({settings['bg_color']['r']}, {settings['bg_color']['g']}, {settings['bg_color']['b']}, {settings['bg_alpha'] / 255})"

        self.setStyleSheet(f"background-color: {bg_rgba};")
        self.listening_label.setStyleSheet(f"color: {text_rgba};")
        self.show()

    def mousePressEvent(self, event: QMouseEvent):
        """Detect right-click to stop, left-click to move or resize."""
        if event.button() == Qt.MouseButton.RightButton:
            self.stop_listening()
        elif event.button() == Qt.MouseButton.LeftButton:
            if self.is_near_edge(event.pos()):
                self.resizing = True
                self.drag_position = event.globalPosition().toPoint()
            else:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle window dragging and resizing."""
        if self.resizing:
            delta = event.globalPosition().toPoint() - self.drag_position
            new_width = max(self.minimumWidth(), self.width() + delta.x())
            new_height = max(self.minimumHeight(), self.height() + delta.y())
            self.resize(new_width, new_height)
            self.drag_position = event.globalPosition().toPoint()
        elif self.dragging:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_position)
            self.drag_position = event.globalPosition().toPoint()
        else:
            self.update_cursor(event.pos())

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Reset dragging and resizing flags."""
        self.dragging = False
        self.resizing = False

    def is_near_edge(self, pos: QPoint) -> bool:
        """Check if mouse position is near the edge for resizing."""
        return pos.x() >= self.width() - self.RESIZE_MARGIN or pos.y() >= self.height() - self.RESIZE_MARGIN

    def update_cursor(self, pos: QPoint):
        """Update the cursor style based on position."""
        if self.is_near_edge(pos):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
