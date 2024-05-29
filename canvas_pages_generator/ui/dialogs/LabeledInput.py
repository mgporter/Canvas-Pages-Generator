from typing import Any, Generic, Literal, TypeVar, override
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from canvas_pages_generator.ui.dialogs.AbstractLabeledItem import AbstractLabeledItem

class LabeledInput(AbstractLabeledItem[qtw.QLineEdit]):

  field: qtw.QLineEdit

  def __init__(
    self, 
    label: str, 
    statusTip: str = "", 
    addSelectionTip: bool = False,
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    parent = None
  ) -> None:
    self.field = qtw.QLineEdit()
    super().__init__(label, statusTip, self.field, addSelectionTip, orientation, parent)

  @override
  def getValue(self) -> str:
    return self.field.text()
  
  @override
  def setValue(self, value: str) -> None:
    self.field.setText(value)