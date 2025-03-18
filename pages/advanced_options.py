from PyQt6.QtWidgets import QWidget, QStackedWidget, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox


class AdvancedOptionsPage(QWidget):

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

