from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from canvas_pages_generator.ui.GradeTab import GradeTab

from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw

from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.core.DataModel import DataModel
from canvas_pages_generator.core.Month import MonthHandler
from canvas_pages_generator.ui.GoalInput import GoalInput
from canvas_pages_generator.ui.GoalsSelector import GoalsSelector


class GoalsArea(qtw.QWidget):

  gradeTab: GradeTab
  vBox: qtw.QVBoxLayout

  def __init__(self, gradeTab: GradeTab, parent = None) -> None:
    super().__init__(parent)

    self.gradeTab = gradeTab

    self.vBox = qtw.QVBoxLayout(self)

    heading = qtw.QLabel(f"Goals for {MonthHandler.getMonth(self.gradeTab.getDataModel().getMonth())}")
    heading.setObjectName("heading")

    goalsContentLayout = qtw.QHBoxLayout()
    goalsContentLayout.addWidget(GoalInput(self))
    goalsContentLayout.addWidget(GoalsSelector(self))
    goalsContentLayout.setContentsMargins(0, 0, 0, Constants.SECTION_SPACING)

    self.vBox.addWidget(heading)
    self.vBox.addLayout(goalsContentLayout)

    self.setLayout(self.vBox)

  def getGradeTab(self) -> GradeTab:
    return self.gradeTab
