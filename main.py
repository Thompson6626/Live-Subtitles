import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets.QWidget import setToolTip

from transcription import AudioStreamer


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

class ListeningPage(QWidget):
    """Listening Page UI with dynamic text rendering."""

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.text_fragments = []
        self.audio_thread = None

        # Label for transcribed text
        self.listening_label = QLabel("Listening...")
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

    def start_listening(self, model_name: str):
        """Start audio transcription thread."""
        if self.audio_thread is None or not self.audio_thread.isRunning():
            self.audio_thread = AudioStreamer(model_name)
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
            self.audio_thread.quit()
            self.audio_thread.wait()  # Ensure it fully stops
            self.audio_thread = None

        self.text_fragments.clear()
        self.update_label()
        self.stacked_widget.setCurrentIndex(0)

class AdvancedPage(QWidget):

    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.language = QLineEdit()  # Language code (optional)
        self.language.placeholderText("en")
        self.language.setToolTip("Specify the language code for transcription (e.g., 'en' for English, 'es' for Spanish). Leave empty for auto-detection.")

        self.task = QComboBox()  # Task selection (transcribe/translate)
        self.task.addItems(["transcribe", "translate"])
        self.task.setToolTip(
            "Choose between 'transcribe' (convert speech to text) or 'translate' (convert speech to English text).")

        self.beam_size = QSpinBox()  # Beam size
        self.beam_size.setValue(5)
        self.beam_size.setToolTip(
            "The number of candidates considered in beam search. Higher values improve accuracy but increase latency.")

        self.best_of = QSpinBox()
        self.best_of.setValue(5)
        self.best_of.setToolTip(
            "Number of decoding attempts for each segment. Higher values improve quality but increase computation time.")

        self.patience = QDoubleSpinBox()
        self.patience.setValue(1.0)
        self.patience.setToolTip(
            "Adjusts decoding patience. Values >1 allow the model to wait longer before finalizing text, improving accuracy.")

        self.length_penalty = QDoubleSpinBox()
        self.length_penalty.setValue(1.0)
        self.length_penalty.setToolTip(
            "Applies a penalty to longer outputs. Higher values discourage long transcriptions.")

        self.repetition_penalty = QDoubleSpinBox()
        self.repetition_penalty.setValue(1.0)
        self.repetition_penalty.setToolTip(
            "Prevents the model from repeating phrases too often. A value >1 discourages repetition.")

        self.no_repeat_ngram_size = QSpinBox()
        self.no_repeat_ngram_size.setValue(0)
        self.no_repeat_ngram_size.setToolTip(
            "Ensures that n-grams of the given size are not repeated in the output. Set to 0 to disable.")

        self.temperature = QLineEdit()  # List of floats (stored as a string)
        self.temperature.setText("0.0, 0.2, 0.4, 0.6, 0.8, 1.0")
        self.temperature.setToolTip(
            "A comma-separated list of temperature values for sampling diversity. Lower values make output more deterministic.")

        self.suppress_blank = QCheckBox()
        self.suppress_blank.setChecked(True)
        self.suppress_blank.setToolTip(
            "If enabled, removes unnecessary silent pauses at the beginning of transcriptions.")

        self.without_timestamps = QCheckBox()
        self.without_timestamps.setChecked(True)
        self.without_timestamps.setToolTip("If checked, timestamps will not be included in the transcription output.")

        self.word_timestamps = QCheckBox()
        self.word_timestamps.setChecked(False)
        self.word_timestamps.setToolTip("Enable word-level timestamps instead of segment-level timestamps.")

        self.prepend_punctuations = QLineEdit()
        self.prepend_punctuations.setText("\"'“¿([{-")
        self.prepend_punctuations.setToolTip(
            "Punctuation marks that should be attached to the beginning of a word (e.g., '“Hello' instead of ' “Hello').")

        self.append_punctuations = QLineEdit()
        self.append_punctuations.setText("\"'.。,，!！?？:：”)]}、")
        self.append_punctuations.setToolTip(
            "Punctuation marks that should be attached to the end of a word (e.g., 'Hello.' instead of 'Hello .').")

        self.multilingual = QCheckBox()
        self.multilingual.setChecked(False)
        self.multilingual.setToolTip(
            "Enable transcription for multiple languages. Useful when working with mixed-language audio.")

        self.batch_size = QSpinBox()
        self.batch_size.setValue(8)
        self.batch_size.setToolTip(
            "Number of audio segments processed simultaneously. Lower values reduce latency but may affect accuracy.")

        self.hotwords = QLineEdit()
        self.hotwords.setToolTip("Specify key phrases or words that should be prioritized during transcription (comma-separated).")



# Add a advanced options for the whisper model
class MainPage(QWidget):
    """Main page with model selection and start button."""

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # Label
        self.label = QLabel("Whisper Model:")
        self.label.setFont(QFont("Arial", 16))
        self.label.setStyleSheet("color: white; margin-right: 1.5em; margin-left: 1.5em;")
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
        layout.addWidget(self.listen_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")

    def switch_to_listening(self):
        """Start audio transcription and switch to listening page."""
        listening_page = self.stacked_widget.widget(1)
        selected_model = self.combo_box.currentText()
        listening_page.start_listening(selected_model)
        self.stacked_widget.setCurrentIndex(1)

class MyApp(QWidget):
    """Main application that manages page switching."""

    def __init__(self):
        super().__init__()

        # Stacked widget for managing pages
        self.stacked_widget = QStackedWidget()

        # Create pages
        self.main_page = MainPage(self.stacked_widget)
        self.listening_page = ListeningPage(self.stacked_widget)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.listening_page)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle("Whisper Text")
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: #111; color: white;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())