from os import path
from typing import Any
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw

from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.ui.CloseButton import CloseButton # type: ignore

class GoalInputBox(qtw.QWidget):

  id: int
  lineedit: qtw.QLineEdit

  def __init__(self, id: int, text: str, onInputChange: Any, onRemove: Any, parent=None) -> None:
    super().__init__(parent)

    self.id = id

    hBox = qtw.QHBoxLayout(self)
    hBox.setSpacing(8)
    hBox.setContentsMargins(0,0,0,0)

    self.lineedit = qtw.QLineEdit(text, parent)
    self.lineedit.setSizePolicy(qtw.QSizePolicy.Policy.MinimumExpanding, qtw.QSizePolicy.Policy.Fixed)

    self.lineedit.textChanged.connect(lambda newText: onInputChange(self.id, newText))

    removeButton = CloseButton(lambda: onRemove(self))

    hBox.addWidget(self.lineedit)
    hBox.addWidget(removeButton)

    self.setLayout(hBox)
    