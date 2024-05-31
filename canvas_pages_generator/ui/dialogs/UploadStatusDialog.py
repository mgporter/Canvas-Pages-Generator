from typing import Any, List, Literal, Mapping, Self, Tuple

from canvas_pages_generator.core.DataModel import DataModel

from pathlib import Path
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw

StatusText = Literal["done", "processing", "pending"]

class UploadStatusDialog(qtw.QDialog):

  statusRows: List[Any]

  def __init__(self, models: List[DataModel], parent=None) -> None:
    super().__init__(parent)

    self.statusRows: List[UploadStatusDialog.StatusRow] = []

    self.vBox = qtw.QVBoxLayout(self)
    self.vBox.setContentsMargins(36,36,36,36)

    for i, model in enumerate(models):
      statusRow = UploadStatusDialog.StatusRow(
        i, 
        model.getPagename(), 
        self.statusToText("pending")
      )
      self.statusRows.append(statusRow)
      self.vBox.addWidget(statusRow)

    self.vBox.setSpacing(10)

    self.vBox.addStretch(2)

  
  def statusToText(self, status: StatusText) -> str:
    if status == "done":
      return "Uploading successful!"
    elif status == "pending":
      return "Waiting to upload"
    elif status == "processing":
      return "Uploading now..."
    else:
      return ""
    
  def updateStatus(self, index: int, status: StatusText) -> None:
    statusRow = self.statusRows[index]
    statusRow.updateStatus(self.statusToText(status))


  class StatusRow(qtw.QLabel):
    
    id: int
    name: str
    template: str = "Page {n}:       {s}"

    def __init__(self, id: int, name: str, status: str, parent=None) -> None:
      super().__init__(parent)

      self.id = id
      self.name = name

      self.setText(self.template.format(n=self.name, s=status))

    def updateStatus(self, status: str) -> None:
      self.setText(self.template.format(n=self.name, s=status))









