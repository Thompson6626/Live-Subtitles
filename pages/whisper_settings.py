from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QComboBox, QSpinBox, QCheckBox,
    QVBoxLayout, QGridLayout, QLabel, QGroupBox, QStackedWidget, QPushButton
)

class WhisperSettings(QWidget):

    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout(self)

        # Create form layout
        form_layout = QGridLayout()

        self.task = QComboBox()
        self.task.addItems(["transcribe", "translate (to english)"])
        self.task.setToolTip(
            "Choose between 'transcribe' (convert speech to text) or 'translate' (convert speech to English text).")

        self.beam_size = QSpinBox()
        self.beam_size.setValue(5)
        self.beam_size.setToolTip(
            "The number of candidates considered in beam search. Higher values improve accuracy but increase latency.")

        self.temperature = QLineEdit()
        self.temperature.setText("0.0, 0.2, 0.4, 0.6, 0.8, 1.0")
        self.temperature.setToolTip(
            "A comma-separated list of temperature values for sampling diversity. Lower values make output more deterministic.")

        self.suppress_blank = QCheckBox("Suppress Blank")
        self.suppress_blank.setChecked(True)
        self.suppress_blank.setToolTip(
            "If enabled, removes unnecessary silent pauses at the beginning of transcriptions.")

        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.reset_defaults)

        self.back_button = QPushButton("Go Back")  # New Go Back Button
        self.back_button.clicked.connect(self.go_back)  # Connect to go_back method

        form_layout.addWidget(QLabel("Task:"), 1, 0)
        form_layout.addWidget(self.task, 1, 1)

        form_layout.addWidget(QLabel("Beam Size:"), 2, 0)
        form_layout.addWidget(self.beam_size, 2, 1)

        form_layout.addWidget(QLabel("Temperature:"), 3, 0)
        form_layout.addWidget(self.temperature, 3, 1)

        # Create checkbox layout
        checkbox_group = QGroupBox("Additional Options")
        checkbox_layout = QVBoxLayout()
        checkbox_layout.addWidget(self.suppress_blank)
        checkbox_group.setLayout(checkbox_layout)

        # Add layouts to main layout
        layout.addLayout(form_layout)
        layout.addWidget(checkbox_group)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def reset_defaults(self):
        self.task.setCurrentIndex(0)
        self.beam_size.setValue(5)
        self.temperature.setText("0.0, 0.2, 0.4, 0.6, 0.8, 1.0")
        self.suppress_blank.setChecked(True)

    def go_back(self):
        """Switch back to the main page."""
        self.stacked_widget.setCurrentIndex(0)  # Assuming 0 is the main page index


    def get_settings(self) -> dict:
        return {
            "task": self.task.currentText(),
            "beam_size": self.beam_size.value(),
            "temperature": self.temperature.text(),
            "suppress_blank": self.suppress_blank.isChecked(),
        }
