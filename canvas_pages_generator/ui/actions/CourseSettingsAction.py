from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from canvas_pages_generator.ui.MainWindow import MainWindow

from typing import Any
from PyQt6.QtGui import QAction
from PyQt6 import QtWidgets as qtw
from canvas_pages_generator.core.Dependencies import Dependencies
from canvas_pages_generator.ui.dialogs.CourseSettingsDialog import CourseSettingsDialog

class CourseSettingsAction(QAction):
      
  mainWindow: MainWindow

  def __init__(self, parent: MainWindow) -> None:

    super().__init__("Course Settings", parent)

    self.mainWindow = parent

    self.triggered.connect(self.onTriggered)
    self.setStatusTip("Set the current year, month, and grade levels that you want to use")

  def onTriggered(self) -> None:
    dialog = CourseSettingsDialog()

    oldSettings = Dependencies.config.getSettings()
    
    if dialog.exec():
      
      # only run if the values have actually changed
      if (
        oldSettings["current_year"] != dialog.selectedYear or
        oldSettings["current_month"] != dialog.selectedMonth or
        oldSettings["grades"] != dialog.selectedGrades
      ):
        Dependencies.config.saveValue("current_year", dialog.selectedYear)
        Dependencies.config.saveValue("current_month", dialog.selectedMonth)
        Dependencies.config.saveValue("grades", dialog.selectedGrades)

        self.mainWindow.remakeCourseTabs()



  