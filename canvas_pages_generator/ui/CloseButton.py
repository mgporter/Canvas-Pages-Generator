from os import path
from typing import Any, Callable
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw

from canvas_pages_generator.core.Constants import Constants

class CloseButton(qtw.QPushButton):

  def __init__(self, callback: Callable[[], None], parent=None):
    super().__init__(parent)

    icon = qtg.QIcon(path.join(Constants.RESOURCES_DIRECTORY, "X_icon.svg"))
    self.setIcon(icon)
    self.setIconSize(qtc.QSize(16, 16))
    self.setFixedSize(qtc.QSize(32, 32))
    self.clicked.connect(callback)