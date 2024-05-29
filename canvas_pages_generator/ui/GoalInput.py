from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from canvas_pages_generator.ui.GoalsArea import GoalsArea

from typing import List
from PyQt6.QtGui import *
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # type: ignore

from canvas_pages_generator.core.DataModel import DataModel
from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.ui.AddButton import AddButton
from canvas_pages_generator.ui.GoalInputBox import GoalInputBox

import pandas as pd



class GoalInput(QWidget):

  dataModel: DataModel
  goalsArea: GoalsArea
  vBoxLayout: QVBoxLayout
  addButton: AddButton

  def __init__(self, goalsArea: GoalsArea, parent=None) -> None:
    super().__init__(parent)

    self.goalsArea = goalsArea
    self.dataModel = goalsArea.getGradeTab().getDataModel()

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

    self.goalsArea.getGradeTab().getEventService().subscribe(
      "goals_added_from_selector",
      self.addItemsFromSelector
    )

    self.initializeRows(self.vBoxLayout)

    self.addButton = AddButton("goal", self.onAddRow, self)
    self.vBoxLayout.addWidget(self.addButton)

    self.setLayout(self.vBoxLayout)

  def initializeRows(self, layout: QVBoxLayout) -> None:
    goals = self.dataModel.getGoalsForCurrentMonth()

    if goals.empty:
      self.addRow()
    else:
      for i, row in goals.iterrows():
        goalInputBox = self.createInputBox(row["id"], row["description"])
        layout.addWidget(goalInputBox)

  def onAddRow(self, checked: bool) -> None:
    """Add Button handler"""
    self.addRow()

  def addRow(self, text: str = "") -> None:

    newId = self.dataModel.insertGoal(text)
    count = self.vBoxLayout.count()

    self.vBoxLayout.insertWidget(
      count - 1,
      self.createInputBox(newId, text)
    )

  def createInputBox(self, id: int, text: str) -> GoalInputBox:
    return GoalInputBox(id, text, self.onInputChange, self.removeRow)

  def onInputChange(self, id: int, text: str) -> None:
    self.dataModel.updateGoal(id, text)

  def addItemsFromSelector(self, itemList: List[str]) -> None:
    for item in itemList:
      itemWasFilledIn = self.fillInRows(item)
      if not itemWasFilledIn:
        self.addRow(item)

  def fillInRows(self, text: str) -> bool:
    # Try to fill in rows first
    children = self.children()
    for child in children:
      if (isinstance(child, GoalInputBox)) and child.lineedit.text() == "":
        child.lineedit.setText(text)
        self.onInputChange(child.id, text)
        return True
    
    return False

  def removeRow(self, row: GoalInputBox) -> None:
    self.dataModel.removeGoal(row.id)
    self.vBoxLayout.removeWidget(row)
    row.deleteLater()
    row = None # type: ignore