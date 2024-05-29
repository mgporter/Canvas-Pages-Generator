from typing import Any, Generic, List, Literal, TypeVar, override
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from canvas_pages_generator.ui.dialogs.AbstractLabeledItem import AbstractLabeledItem

class LabeledComboBox(AbstractLabeledItem[qtw.QComboBox]):

  field: qtw.QComboBox

  def __init__(
    self, 
    label: str, 
    options: List[str],
    statusTip: str = "", 
    addSelectionTip: bool = False,
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    parent = None
  ) -> None:
    self.field = qtw.QComboBox()
    super().__init__(label, statusTip, self.field, addSelectionTip, orientation, parent)

    self.field.addItems(options)

  @override
  def getValue(self) -> int:
    return self.field.currentIndex()
  
  @override
  def setValue(self, value: int) -> None:
    self.field.setCurrentIndex(value)