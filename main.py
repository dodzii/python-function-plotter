from PySide2.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide2.QtGui import QDoubleValidator, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import math
import numpy as np


def parse_and_evaluate(func, x):
    func = func.replace("^", "**")
    func = func.replace("log10(", "math.log10(")
    func = func.replace("sqrt(", "math.sqrt(")

    try:
        allowed_builtins = {'math': math, '__builtins__': {}}
        return eval(func, allowed_builtins, {'x': x})
    except Exception as e:
        return "Invalid function"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Function Plotter")
        self.setGeometry(300, 300, 800, 600)
        self.icon = QIcon("assets/master_micro_icon.jpeg")
        self.setWindowIcon(self.icon)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label1 = QLabel("Enter a function to plot: ", self)
        layout.addWidget(self.label1)

        self.func = QLineEdit(self)
        layout.addWidget(self.func)

        self.label_min = QLabel("Min value of x: ", self)
        layout.addWidget(self.label_min)

        self.min = QLineEdit(self)
        layout.addWidget(self.min)

        self.label_max = QLabel("Max value of x: ", self)
        layout.addWidget(self.label_max)

        self.max = QLineEdit(self)
        layout.addWidget(self.max)

        self.button = QPushButton("Plot", self)
        layout.addWidget(self.button)

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.min.setValidator(validator)
        self.max.setValidator(validator)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.button.clicked.connect(lambda: self.plot_function(self.func.text(), self.min.text(), self.max.text()))

        self.set_stylesheet()

        self.latest_error = ""

    def plot_function(self, func, min_x, max_x):
        if not func or not min_x or not max_x:
            self.latest_error = "Please enter a function and min/max values for x"
            alert = QMessageBox()
            alert.setText(self.latest_error)
            alert.setWindowTitle("Error")
            alert.setWindowIcon(self.icon)
            alert.exec_()
            return

        if float(min_x) > float(max_x):
            self.latest_error = "Min value of x must be less than max value of x"
            alert = QMessageBox()
            alert.setText(self.latest_error)
            alert.setWindowTitle("Error")
            alert.setWindowIcon(self.icon)
            alert.exec_()
            return

        if parse_and_evaluate(func, 1) == "Invalid function":
            self.latest_error = "Invalid function"
            alert = QMessageBox()
            alert.setText(self.latest_error)
            alert.setWindowTitle("Error")
            alert.setWindowIcon(self.icon)
            alert.exec_()
            return

        self.latest_error = ""

        x = np.linspace(float(min_x), float(max_x), 1000)
        y = [parse_and_evaluate(func, i) for i in x]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)

        ax.grid(True)

        self.canvas.draw()

    def set_stylesheet(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                font-family: Courier New;
            }
            QLineEdit {
                font-size: 16px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            QPushButton {
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: white;
                color: #4CAF50;
                border: 1px solid #4CAF50;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #3c8e41;
            }
            
            FigureCanvasQTAgg {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
        """)


if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    myApp.exec_()
    sys.exit(0)
