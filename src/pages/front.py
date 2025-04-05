from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QStackedWidget, QLabel, QComboBox, QHBoxLayout,
    QPushButton, QVBoxLayout, QLineEdit, QSizePolicy, QFrame
)

from .listening import ListeningPage

# Whisper Models
WHISPER_MODELS = [
    "tiny", "tiny.en", "base", "base.en", "small", "small.en",
    "medium", "medium.en", "large-v1", "large-v2", "large-v3",
    "distil-small.en", "distil-medium.en", "distil-large-v2", "distil-large-v3"
]

DEVICES = [
    "cpu",
    "cuda",
    "auto"
]

class FrontPage(QWidget):
    """Main page with model selection and start button."""
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.listening_window = None

        # --- Whisper Model Selection ---
        self.label = QLabel("Whisper Model:")
        self.label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white; margin-left: 15px;")

        self.combo_box = QComboBox()
        self.combo_box.addItems(WHISPER_MODELS)
        self.combo_box.setCurrentIndex(6)
        self.combo_box.setFont(QFont("Arial", 14))
        self.combo_box.setMinimumWidth(200)
        self.combo_box.setStyleSheet("""
            background-color: #333; 
            color: white; 
            padding: 8px; 
            border-radius: 6px;
        """)

        model_selection_layout = QHBoxLayout()
        model_selection_layout.addWidget(self.label)
        model_selection_layout.addWidget(self.combo_box)
        model_selection_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # --- Device Selection ---
        self.device_label = QLabel("Device:")
        self.device_label.setFont(QFont("Arial", 16, QFont.Weight.Medium))
        self.device_label.setStyleSheet("color: white; margin-left: 13px;")

        self.device_combo_box = QComboBox()
        self.device_combo_box.addItems(DEVICES)
        self.device_combo_box.setCurrentIndex(0)
        self.device_combo_box.setFont(QFont("Arial", 13))
        self.device_combo_box.setMinimumWidth(200)
        self.device_combo_box.setStyleSheet("""
                    background-color: #333; 
                    color: white; 
                    padding: 8px; 
                    border-radius: 6px;
                """)

        device_selection_layout = QHBoxLayout()
        device_selection_layout.addWidget(self.device_label)
        device_selection_layout.addWidget(self.device_combo_box)
        device_selection_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # --- Language Selection ---
        self.language_selection_label = QLabel("Language Code:")
        self.language_selection_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        self.language_selection_label.setStyleSheet("color: white; margin-left: 15px;")

        self.language_selection = QLineEdit()
        self.language_selection.setPlaceholderText("en")
        self.language_selection.setFont(QFont("Arial", 13))
        self.language_selection.setMinimumWidth(70)
        self.language_selection.setStyleSheet("""
            QLineEdit {
                background-color: #444;
                color: white;
                padding: 8px;
                margin-left: 15px;
                border-radius: 6px;
                border: 1px solid #555;
            }
            QLineEdit:focus {
                border: 1px solid white;
            }
        """)

        language_input_layout = QHBoxLayout()
        language_input_layout.addWidget(self.language_selection_label)
        language_input_layout.addWidget(self.language_selection)
        language_input_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # --- Divider ---
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #555; margin: 10px 0;")

        # --- Buttons ---
        self.listen_button = QPushButton("🎤 Start Listening")
        self.listen_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.listen_button.setMinimumWidth(240)
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7; 
                color: white; 
                padding: 12px; 
                border-radius: 10px;
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

        self.advanced_options_button = QPushButton("⚙️ Whisper Settings")
        self.advanced_options_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.advanced_options_button.setMinimumWidth(200)
        self.advanced_options_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.advanced_options_button.clicked.connect(self.switch_to_whisper_options)

        self.listening_style_button = QPushButton("🎨 Listening Page Style")
        self.listening_style_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.listening_style_button.setMinimumWidth(200)
        self.listening_style_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.listening_style_button.clicked.connect(self.switch_to_listening_style)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.advanced_options_button)
        buttons_layout.addWidget(self.listening_style_button)
        buttons_layout.addStretch()

        # --- Main Layout ---
        layout = QVBoxLayout()
        layout.addLayout(model_selection_layout)
        layout.addLayout(device_selection_layout)
        layout.addLayout(language_input_layout)
        layout.addWidget(divider)
        layout.addWidget(self.listen_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(buttons_layout)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

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
            input_language = self.language_selection.text() or None # No empty
            device = self.device_combo_box.currentText()

            self.listening_window = ListeningPage(
                selected_model,
                listening_settings_page.get_settings(),

                language=input_language,
                device=device,
                **whisper_settings_page.get_settings()
            )

            self.listening_window.stopped.connect(self.reset_listening_window)

            self.listening_window.show()
            self.showMinimized()

    def reset_listening_window(self):
        """Reset the listening window reference when it stops."""
        self.listening_window = None

    def switch_to_whisper_options(self):
        """Switch to Whisper Options Page."""
        self.stacked_widget.setCurrentIndex(1)

    def switch_to_listening_style(self):
        """Switch to Listening Style settings page."""
        self.stacked_widget.setCurrentIndex(2)
