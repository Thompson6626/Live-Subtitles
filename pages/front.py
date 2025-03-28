from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QStackedWidget, QLabel, QComboBox, QHBoxLayout,
    QPushButton, QVBoxLayout, QLineEdit, QSizePolicy
)

from .listening import ListeningPage

# Whisper Models
WHISPER_MODELS = [
    "tiny", "tiny.en", "base", "base.en", "small", "small.en",
    "medium", "medium.en", "large-v1", "large-v2", "large-v3",
    "distil-small.en", "distil-medium.en", "distil-large-v2", "distil-large-v3"
]

class FrontPage(QWidget):
    """Main page with model selection and start button."""
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.listening_window = None

        # --- Whisper Model Selection ---
        self.label = QLabel("Whisper Model:")
        self.label.setFont(QFont("Arial", 16))
        self.label.setStyleSheet("color: white; margin-left: 15px;")

        self.combo_box = QComboBox()
        self.combo_box.addItems(WHISPER_MODELS)
        self.combo_box.setCurrentIndex(6)
        self.combo_box.setFont(QFont("Arial", 14))
        self.combo_box.setMinimumWidth(180)
        self.combo_box.setStyleSheet("""
            background-color: #333; 
            color: white; 
            padding: 5px; 
            border-radius: 5px;
        """)

        # Model Selection Layout
        model_selection_layout = QHBoxLayout()
        model_selection_layout.addWidget(self.label)
        model_selection_layout.addWidget(self.combo_box)
        model_selection_layout.addStretch()

        # --- Language Selection ---
        self.language_selection_label = QLabel("Language code:")
        self.language_selection_label.setFont(QFont("Arial", 13))
        self.language_selection_label.setStyleSheet("color: white; margin-left: 15px;")

        self.language_selection = QLineEdit()
        self.language_selection.setPlaceholderText("en")
        self.language_selection.setFont(QFont("Arial", 13))
        self.language_selection.setStyleSheet("""
            QLineEdit {
                border: none;
                background-color: #444;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 1px solid white;
            }
        """)

        # Language Input Layout
        language_input_layout = QHBoxLayout()
        language_input_layout.addWidget(self.language_selection_label)
        language_input_layout.addWidget(self.language_selection)
        language_input_layout.addStretch()

        # --- Buttons ---
        self.listen_button = QPushButton("Start Listening")
        self.listen_button.setFont(QFont("Arial", 16))
        self.listen_button.setMinimumWidth(220)
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7; 
                color: #F5F5F5; 
                padding: 12px; 
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        self.listen_button.clicked.connect(self.open_listening_page)

        self.advanced_options_button = QPushButton("Whisper Settings")
        self.advanced_options_button.setFont(QFont("Arial", 14))
        self.advanced_options_button.setMinimumWidth(180)
        self.advanced_options_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: #F5F5F5;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.advanced_options_button.clicked.connect(self.switch_to_whisper_options)

        self.listening_style_button = QPushButton("Listening Page Style")
        self.listening_style_button.setFont(QFont("Arial", 12))
        self.listening_style_button.setMinimumWidth(180)
        self.listening_style_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: #F5F5F5;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.listening_style_button.clicked.connect(self.switch_to_listening_style)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.advanced_options_button)
        buttons_layout.addWidget(self.listening_style_button)
        buttons_layout.addStretch()

        # --- Main Layout ---
        layout = QVBoxLayout()
        layout.addLayout(model_selection_layout)
        layout.addLayout(language_input_layout)
        layout.addWidget(self.listen_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(buttons_layout)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")

        # Allow resizing
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    # --- Page Switching Functions ---
    def open_listening_page(self):
        """Start audio transcription and switch to listening page."""
        if self.listening_window is None:
            whisper_settings_page = self.stacked_widget.widget(1)
            listening_settings_page = self.stacked_widget.widget(2)
            selected_model = self.combo_box.currentText()
            input_language = self.language_selection.text() or None

            self.listening_window = ListeningPage(
                selected_model,
                listening_settings_page.get_settings(),
                language=input_language,
                **whisper_settings_page.get_settings()
            )

            self.listening_window.stopped.connect(self.reset_listening_window)

            self.listening_window.show()
            self.showMinimized()

    def reset_listening_window(self):
        """Reset the listening window reference when it stops."""
        self.listening_window = None

    def switch_to_whisper_options(self):
        """Switch to Advanced Options Page."""
        self.stacked_widget.setCurrentIndex(1)

    def switch_to_listening_style(self):
        """Switch to Listening Style settings page."""
        self.stacked_widget.setCurrentIndex(2)
