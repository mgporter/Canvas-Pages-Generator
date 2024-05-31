from typing import cast
from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from canvas_pages_generator.core.DataModel import DataModel
from canvas_pages_generator.core.Dependencies import Dependencies
from canvas_pages_generator.core.CanvasTypes import Course
from canvas_pages_generator.ui.UploadWidget import UploadWidget
from canvas_pages_generator.ui.GradeTab import GradeTab

class CourseTab(QWidget):

  course: Course
  name: str
  id: int
  year: int
  month: int
  tabs: QTabWidget

  uploadWidget: UploadWidget

  def __init__(self, course: Course, year: int, month: int, parent=None) -> None:
    super().__init__(parent)

    self.course = course
    self.name = self.course.name
    self.id = self.course.id
    self.year = year
    self.month = month

    self.setWindowTitle(f"{self.name} {self.year}-{self.year + 1}")

    self.vbox = QVBoxLayout(self)
    self.vbox.setContentsMargins(2, 2, 0, 0)

    self.tabs = QTabWidget()
    self.tabs.setTabPosition(QTabWidget.TabPosition.West)
    self.tabs.setMovable(False)

    self.uploadWidget = UploadWidget(self, course)

    self.vbox.addWidget(self.uploadWidget)
    self.vbox.addWidget(self.tabs)
    self.setLayout(self.vbox)

    

    self.createTabs()


  def createTabs(self) -> None:
    grades = Dependencies.config.settings['grades']

    for grade in grades[::-1]:
      dataModel = DataModel(self.course, grade, self.year, self.month)

      self.tabs.addTab(
        GradeTab(
          dataModel,
          self
        ),
        grade
      )

  
