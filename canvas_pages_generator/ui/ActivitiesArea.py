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
from canvas_pages_generator.ui.ActivityInput import ActivityInput
from canvas_pages_generator.ui.ActivityPreviewWindow import ActivityPreviewWindow


class ActivitiesArea(qtw.QWidget):

  gradeTab: GradeTab
  vBox: qtw.QVBoxLayout

  def __init__(self, gradeTab: GradeTab, parent = None) -> None:
    super().__init__(parent)

    self.gradeTab = gradeTab
    self.vBox = qtw.QVBoxLayout(self)

    heading = qtw.QLabel(f"Activities from {MonthHandler.getMonth(self.gradeTab.getDataModel().getMonth() - 1)}")
    heading.setObjectName("heading")

    activitiesContentLayout = qtw.QHBoxLayout()
    activitiesContentLayout.addWidget(ActivityInput(self), stretch=10)
    activitiesContentLayout.addWidget(ActivityPreviewWindow(self), stretch=1)

    self.vBox.addWidget(heading)
    self.vBox.addLayout(activitiesContentLayout)

    self.setLayout(self.vBox)

  def getGradeTab(self) -> GradeTab:
    return self.gradeTab