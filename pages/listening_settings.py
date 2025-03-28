from typing import Dict, Union

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QStackedWidget, QPushButton, QSlider, QLabel,
    QColorDialog, QVBoxLayout, QCheckBox, QGroupBox
)


class ListeningSettings(QWidget):
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # Preview Label
        self.preview_label = QLabel("Preview Text")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.preview_label.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 8px;")
        main_layout.addWidget(self.preview_label)

        # Text Settings Group
        text_group = QGroupBox("Text Settings")
        text_layout = QVBoxLayout()

        self.text_color_btn = QPushButton("Select Text Color")
        self.text_color_btn.clicked.connect(self.select_text_color)
        self.text_color_btn.setStyleSheet("border: 2px solid white; padding: 5px;")

        self.text_alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.text_alpha_slider.setMinimum(0)
        self.text_alpha_slider.setMaximum(255)
        self.text_alpha_slider.setValue(255)
        self.text_alpha_slider.valueChanged.connect(self.update_text_transparency)

        self.font_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_size_slider.setMinimum(5)
        self.font_size_slider.setMaximum(90)
        self.font_size_slider.setValue(18)
        self.font_size_slider.valueChanged.connect(self.update_font_size)

        text_layout.addWidget(self.text_color_btn)
        text_layout.addWidget(QLabel("Text Transparency"))
        text_layout.addWidget(self.text_alpha_slider)
        text_layout.addWidget(QLabel("Font Size"))
        text_layout.addWidget(self.font_size_slider)
        text_group.setLayout(text_layout)
        main_layout.addWidget(text_group)

        # Background Settings Group
        bg_group = QGroupBox("Background Settings")
        bg_layout = QVBoxLayout()

        self.bg_color_btn = QPushButton("Select Background Color")
        self.bg_color_btn.clicked.connect(self.select_bg_color)
        self.bg_color_btn.setStyleSheet("border: 2px solid white; padding: 5px;")

        self.bg_alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.bg_alpha_slider.setMinimum(0)
        self.bg_alpha_slider.setMaximum(255)
        self.bg_alpha_slider.setValue(255)
        self.bg_alpha_slider.valueChanged.connect(self.update_bg_transparency)

        bg_layout.addWidget(self.bg_color_btn)
        bg_layout.addWidget(QLabel("Background Transparency"))
        bg_layout.addWidget(self.bg_alpha_slider)
        bg_group.setLayout(bg_layout)
        main_layout.addWidget(bg_group)

        # Frameless Checkbox
        self.frameless_checkbox = QCheckBox("Enable Frameless Window")
        self.frameless_checkbox.setChecked(True)
        main_layout.addWidget(self.frameless_checkbox)

        # Go Back Button
        self.go_back_btn = QPushButton("Go Back")
        self.go_back_btn.clicked.connect(self.go_back)
        main_layout.addWidget(self.go_back_btn)

        self.setLayout(main_layout)

        # Default Settings
        self.text_color = QColor(255, 255, 255, 255)  # White
        self.bg_color = QColor(0, 0, 0, 255)  # Black
        self.font_size = 18
        self.update_preview()

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)

    def select_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_color.setRgb(color.red(), color.green(), color.blue(), self.text_alpha_slider.value())
            self.update_preview()

    def update_text_transparency(self, value):
        self.text_color.setAlpha(value)
        self.update_preview()

    def select_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color.setRgb(color.red(), color.green(), color.blue(), self.bg_alpha_slider.value())
            self.update_preview()

    def update_bg_transparency(self, value):
        self.bg_color.setAlpha(value)
        self.update_preview()

    def update_font_size(self, value):
        self.font_size = value
        self.update_preview()

    def update_preview(self):
        text_rgba = f"rgba({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()}, {self.text_color.alpha() / 255})"
        bg_rgba = f"rgba({self.bg_color.red()}, {self.bg_color.green()}, {self.bg_color.blue()}, {self.bg_color.alpha() / 255})"

        self.preview_label.setFont(QFont("Arial", self.font_size, QFont.Weight.Bold))
        self.preview_label.setStyleSheet(f"""
            background-color: {bg_rgba}; 
            color: {text_rgba}; 
            padding: 10px; 
            border-radius: 8px;
            font-size: {self.font_size}px;
        """)

    def get_settings(self) -> Dict[str, Union[Dict[str, int], int, bool]]:
        return {
            "text_color": {
                "r": self.text_color.red(),
                "g": self.text_color.green(),
                "b": self.text_color.blue(),
                "a": self.text_color.alpha()
            },
            "bg_color": {
                "r": self.bg_color.red(),
                "g": self.bg_color.green(),
                "b": self.bg_color.blue(),
                "a": self.bg_color.alpha()
            },
            "text_alpha": self.text_alpha_slider.value(),
            "bg_alpha": self.bg_alpha_slider.value(),
            "font_size": self.font_size,
            "frameless": self.frameless_checkbox.isChecked()
        }
