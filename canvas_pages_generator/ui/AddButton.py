from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # type: ignore

class AddButton(QPushButton):

  def __init__(self, itemType: str, onClickedAction=None, parent=None) -> None:
    super().__init__(parent)
    self.setText("+ Add")
    self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
    self.setStatusTip(f"Add a new {itemType}")
    self.clicked.connect(onClickedAction)
