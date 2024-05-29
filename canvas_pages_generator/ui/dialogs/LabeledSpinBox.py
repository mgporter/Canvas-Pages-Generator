from typing import Any, Generic, Literal, TypeVar, override
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from canvas_pages_generator.ui.dialogs.AbstractLabeledItem import AbstractLabeledItem

class LabeledSpinBox(AbstractLabeledItem[qtw.QSpinBox]):

  field: qtw.QSpinBox

  def __init__(
    self, 
    label: str, 
    statusTip: str = "", 
    addSelectionTip: bool = False,
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    parent = None
  ) -> None:
    self.field = qtw.QSpinBox()
    super().__init__(label, statusTip, self.field, addSelectionTip, orientation, parent)

  @override
  def getValue(self) -> int:
    return self.field.value()
  
  @override
  def setValue(self, value: int) -> None:
    self.field.setValue(value)