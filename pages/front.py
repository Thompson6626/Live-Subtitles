from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QStackedWidget, QLabel, QComboBox, QHBoxLayout, QPushButton, QVBoxLayout, QLineEdit

# Faster-Whisper Models
# https://huggingface.co/Systran
WHISPER_MODELS = [
    "tiny", "tiny.en",
    "base", "base.en",
    "small", "small.en",
    "medium", "medium.en",
    "large-v1", "large-v2", "large-v3",
    "distil-small.en",
    "distil-medium.en",
    "distil-large-v2",
    "distil-large-v3"
]

# Add a advanced options for the whisper model
class FrontPage(QWidget):
    """Main page with model selection and start button."""

    selected_model = pyqtSignal(str)

    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Label
        self.label = QLabel("Whisper Model:")
        self.label.setFont(QFont("Arial", 16))
        self.label.setStyleSheet("color: white; margin-right: 1.5em; margin-left: 1.5em;")

        # Language selection label
        self.language_selection_label = QLabel("Language code:")
        self.language_selection_label.setFont(QFont("Arial", 13))
        self.language_selection_label.setStyleSheet("color: white; margin-right: 1.5em; margin-left: 1.5em;")

        # Language Selection
        self.language_selection = QLineEdit()
        self.language_selection.setPlaceholderText("en")
        self.language_selection.setFont(QFont("Arial", 13))
        self.language_selection.setStyleSheet("""
        QLineEdit {
            border: none;
        }
        QLineEdit:focus{
            border: 1px solid white;
        }
        """)
        language_input_layout = QHBoxLayout()
        language_input_layout.addWidget(self.language_selection_label)
        language_input_layout.addWidget(self.language_selection)
        language_input_layout.addStretch()
        language_input_layout.setContentsMargins(50, 30, 0, 0)  # (left, top, right, bottom)

        # ComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItems(WHISPER_MODELS)
        self.combo_box.setCurrentIndex(6)
        self.combo_box.setFont(QFont("Arial", 14))
        self.combo_box.setFixedWidth(200)
        self.combo_box.setStyleSheet("background-color: #333; color: white; padding: 5px; border-radius: 5px;")

        # Horizontal layout for label and combo box
        model_selection_layout = QHBoxLayout()
        model_selection_layout.addWidget(self.label)
        model_selection_layout.addWidget(self.combo_box)
        model_selection_layout.addStretch()  # Pushes everything to the left neatly

        # Listen Button
        self.listen_button = QPushButton("Start Listening")
        self.listen_button.setFont(QFont("Arial", 16))
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7; 
                color: #F5F5F5; 
                padding: 12px; 
                border-radius: 8px;
                font-weight: bold;
                transition: background-color 0.7s, border-color 0.7s;
            }
            QPushButton:hover {
                background-color: #005a9e;
                color: #FFFFFF;
            }
            QPushButton:pressed {
                background-color: #004080;
                border-color: #003366;
            }
        """)
        self.listen_button.clicked.connect(self.switch_to_listening)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(model_selection_layout)
        layout.addLayout(language_input_layout)
        layout.addWidget(self.listen_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")

    def switch_to_listening(self):
        """Start audio transcription and switch to listening page."""
        listening_page = self.stacked_widget.widget(2) # Listening Page
        selected_model = self.combo_box.currentText()
        input_language = self.language_selection.text() or None

        listening_page.start_listening(
            selected_model,
            language=input_language
        )

        self.stacked_widget.setCurrentIndex(2)
