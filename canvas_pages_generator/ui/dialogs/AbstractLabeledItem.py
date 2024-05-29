from typing import Any, Generic, Literal, Optional, TypeVar
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

T = TypeVar("T", bound="qtw.QWidget")

class AbstractLabeledItem(Generic[T], qtw.QWidget):

  label: qtw.QLabel
  selectionTipLabel: Optional[qtw.QLabel]
  field: T

  def __init__(
    self, 
    label: str, 
    statusTip: str, 
    field: T,
    addSelectionTip: bool,
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    parent = None
  ) -> None:
    
    super().__init__(parent)

    self.label = qtw.QLabel(label)
    self.selectionTipLabel = None

    self.field = field
    self.field.setStatusTip(statusTip)
    fieldWidget = self.field

    if addSelectionTip:
      fieldWidget = qtw.QWidget() # type: ignore
      fieldLayout = qtw.QVBoxLayout(fieldWidget)
      fieldLayout.setContentsMargins(0,0,0,0)
      fieldLayout.setSpacing(2)
      self.selectionTipLabel = qtw.QLabel()
      self.selectionTipLabel.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)
      self.selectionTipLabel.setStyleSheet("font-size: 10pt; opacity: 0.8;")
      self.selectionTipLabel.setWordWrap(True)
      fieldLayout.addWidget(self.field)
      fieldLayout.addWidget(self.selectionTipLabel)

    layout: qtw.QBoxLayout
    spacing: int

    if orientation == "horizontal":
      layout = qtw.QHBoxLayout(self)
      spacing = 40
      self.label.setAlignment(qtc.Qt.AlignmentFlag.AlignTop)
    else:
      layout = qtw.QVBoxLayout(self)
      spacing = 10

    layout.setContentsMargins(8,8,8,8)
    layout.addWidget(self.label)
    layout.addSpacing(spacing)
    layout.addWidget(fieldWidget)

    self.setSizePolicy(
      qtw.QSizePolicy.Policy.Preferred,
      qtw.QSizePolicy.Policy.Fixed,
    )

  def getLabel(self) -> qtw.QLabel:
    return self.label
  
  def getField(self) -> T:
    return self.field
  
  def getValue(self) -> Any:
    return None
  
  def setValue(self, value: Any) -> None:
    pass

  def setSelectionTipText(self, value: str) -> None:
    if self.selectionTipLabel is not None:
      self.selectionTipLabel.setText(value)