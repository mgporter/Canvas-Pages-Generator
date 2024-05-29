from typing import Any
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # type: ignore

class GoalInputBox(QWidget):

  id: int
  lineedit: QLineEdit

  def __init__(self, id: int, text: str, onInputChange: Any, onRemove: Any, parent=None) -> None:
    super().__init__(parent)

    print(id, text, parent)

    self.id = id

    hBox = QHBoxLayout(self)
    hBox.setSpacing(8)
    hBox.setContentsMargins(0,0,0,0)

    self.lineedit = QLineEdit(text, parent)
    self.lineedit.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

    self.lineedit.textChanged.connect(lambda newText: onInputChange(self.id, newText))

    removeButton = QPushButton("×")
    removeButton.setFixedSize(QSize(26, 26))
    removeButton.clicked.connect(lambda: onRemove(self))

    hBox.addWidget(self.lineedit)
    hBox.addWidget(removeButton)

    self.setLayout(hBox)
    