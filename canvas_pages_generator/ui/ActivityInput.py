from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from canvas_pages_generator.ui.ActivitiesArea import ActivitiesArea

from typing import List
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # type: ignore

from canvas_pages_generator.core.DataModel import DataModel
from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.ui.AddButton import AddButton
from canvas_pages_generator.ui.ActivityInputBox import ActivityInputBox


class ActivityInput(QWidget):

  dataModel: DataModel
  vBoxLayout: QVBoxLayout

  addButton: AddButton
  activitiesArea: ActivitiesArea

  def __init__(self, activitiesArea: ActivitiesArea, parent = None) -> None:
    super().__init__(parent)

    self.activitiesArea = activitiesArea
    self.dataModel = self.activitiesArea.getGradeTab().getDataModel()
    self.activitiesArea.getGradeTab().getEventService().subscribe(
      "media_removed",
      self.removeMedia
    )

    # self.setMinimumWidth(700)
    self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)

    self.vBoxLayout = QVBoxLayout()
    self.vBoxLayout.setSpacing(Constants.SUBSECTION_SPACING)
    self.vBoxLayout.setContentsMargins(
      Constants.SUBSECTION_MARGIN,
      Constants.SECTION_MARGIN,
      Constants.SECTION_MARGIN,
      Constants.SECTION_MARGIN,
    )
    self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.initializeRows(self.vBoxLayout)

    self.addButton = AddButton("activity", self.onAddRow, self)
    self.vBoxLayout.addWidget(self.addButton)

    self.setLayout(self.vBoxLayout)
  
  def initializeRows(self, layout: QVBoxLayout) -> None:
    activities = self.dataModel.getActivitiesForCurrentMonth()

    if activities.empty:
      self.addRow()
    else:
      for i, row in activities.iterrows():
        activityInputBox = self.createInputBox(row["id"], row["description"])
        layout.addWidget(activityInputBox)

  def onAddRow(self, checked: bool) -> None:
    """Add Button handler"""
    self.addRow()

  def addRow(self, text: str = "") -> None:

    newId = self.dataModel.insertActivity(text)
    count = self.vBoxLayout.count()

    self.vBoxLayout.insertWidget(
      count - 1,
      self.createInputBox(newId, text)
    )

  def createInputBox(self, id: int, text: str) -> ActivityInputBox:
    return ActivityInputBox(self, id, text)

  def onDescriptionChange(self, id: int, text: str) -> None:
    self.dataModel.updateActivity(id, text)

  def removeRow(self, row: ActivityInputBox) -> None:
    self.dataModel.removeActivity(row.id)
    self.vBoxLayout.removeWidget(row)
    row.deleteLater()
    row = None # type: ignore

  def removeMedia(self, activity_id: int, media_id: int) -> None:
    for child in self.children():
      if isinstance(child, ActivityInputBox) and child.id == activity_id:
        child.removeMedia(media_id)

  def getActivitiesArea(self) -> ActivitiesArea:
    return self.activitiesArea