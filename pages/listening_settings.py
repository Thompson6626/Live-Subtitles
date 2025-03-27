from PyQt6.QtWidgets import QWidget, QStackedWidget


class ListeningSettings(QWidget):


    def __init__(self,stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget


