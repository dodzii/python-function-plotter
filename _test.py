import pytest
from PySide2.QtWidgets import QApplication
from main import parse_and_evaluate, MainWindow
import sys
import math


@pytest.fixture(scope="module")
def app():
    app = QApplication(sys.argv)
    yield app
    app.quit()


def test_parse_and_evaluate():
    assert parse_and_evaluate("x^2", 2) == 4
    assert parse_and_evaluate("log10(x)", 10) == 1
    assert parse_and_evaluate("sqrt(x)", 4) == 2
    assert parse_and_evaluate("1/x", 2) == 0.5
    assert parse_and_evaluate("x + 1", 2) == 3
    assert parse_and_evaluate("x ** 2 + 2 * x + 1", 3) == 16
    assert parse_and_evaluate("math.sin(x)", math.pi / 2) == 1


def test_invalid_function():
    assert parse_and_evaluate("invalid_function(x)", 1) == "Invalid function"


def test_main_window_ui(app):
    main_window = MainWindow()
    assert main_window.windowTitle() == "Function Plotter"
    assert main_window.label1.text() == "Enter a function to plot: "
    assert main_window.label_min.text() == "Min value of x: "
    assert main_window.label_max.text() == "Max value of x: "
    assert main_window.button.text() == "Plot"
    assert main_window.func.text() == ""
    assert main_window.min.text() == ""
    assert main_window.max.text() == ""


def test_plot_function_valid(app):
    main_window = MainWindow()
    main_window.func.setText("x^2")
    main_window.min.setText("0")
    main_window.max.setText("10")

    main_window.plot_function(main_window.func.text(), main_window.min.text(), main_window.max.text())

    assert len(main_window.figure.axes) > 0
    ax = main_window.figure.axes[0]
    assert len(ax.lines) > 0
    line = ax.lines[0]
    assert len(line.get_xdata()) == 1000
    assert len(line.get_ydata()) == 1000
    assert main_window.latest_error == ""


def test_plot_function_invalid_min_max(app):
    main_window = MainWindow()
    main_window.func.setText("x^2")
    main_window.min.setText("10")
    main_window.max.setText("0")

    main_window.plot_function(main_window.func.text(), main_window.min.text(), main_window.max.text())
    assert main_window.latest_error == "Min value of x must be less than max value of x"


def test_plot_function_invalid_function(app):
    main_window = MainWindow()
    main_window.func.setText("invalid_function(x)")
    main_window.min.setText("0")
    main_window.max.setText("10")

    main_window.plot_function(main_window.func.text(), main_window.min.text(), main_window.max.text())
    assert main_window.latest_error == "Invalid function"
