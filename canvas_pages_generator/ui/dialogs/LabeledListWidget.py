from typing import Any, Callable, Generic, List, Literal, Optional, TypeVar, override, cast
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from canvas_pages_generator.ui.dialogs.AbstractLabeledItem import AbstractLabeledItem

T = TypeVar("T", bound="str")

class LabeledListWidget(Generic[T], AbstractLabeledItem[qtw.QListWidget]):

  field: qtw.QListWidget

  def __init__(
    self, 
    label: str, 
    options: List[T],
    selectedOptions: List[T],
    statusTip: str = "", 
    addSelectionTip: bool = False,
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    parent = None
  ) -> None:
    self.field = qtw.QListWidget()
    super().__init__(label, statusTip, self.field, addSelectionTip, orientation, parent)

    self.field.setSelectionMode(qtw.QAbstractItemView.SelectionMode.MultiSelection)

    for option in options:
      item = qtw.QListWidgetItem(option, self.field)
      if option in selectedOptions:
        item.setSelected(True)

  @override
  def getValue(self) -> List[T]:
    return [cast(T, x.text()) for x in self.field.selectedItems()]

  @override
  def setValue(self, values: List[T]) -> None:
    items = [self.getField().item(x) for x in range(self.getField().count())]
    for item in items:
      if item is not None:
        if item.text() in values:
          item.setSelected(True)
        else:
          item.setSelected(False)
      