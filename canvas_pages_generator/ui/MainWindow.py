from typing import cast
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # type: ignore
from canvasapi import Canvas # type: ignore
from canvas_pages_generator.core.Dependencies import Dependencies
from canvas_pages_generator.core.Utils import getLastTwoDigitsOfYear
from canvas_pages_generator.services.ApiService import ApiService
from canvas_pages_generator.core.CanvasTypes import Course
from canvas_pages_generator.ui.CourseTab import CourseTab
from canvas_pages_generator.ui.actions.ConnectAction import ConnectAction
from canvas_pages_generator.ui.actions.CourseSettingsAction import CourseSettingsAction

class MainWindow(QMainWindow):

  api: ApiService
  canvas: Canvas
  tabs: QTabWidget

  WINDOW_TITLE = "Canvas Pages Generator {c}"

  def __init__(self):
    super().__init__()
    
    self.api = Dependencies.apiService
    self.canvas = self.api.getCanvas()

    self.setMinimumSize(QSize(640, 480))
    self.setWindowTitle(self.WINDOW_TITLE.format(c=""))

    self.tabs = QTabWidget()
    self.tabs.setTabPosition(QTabWidget.TabPosition.North)
    self.tabs.setMovable(False)

    self.createMenu()
    self.createCourseTabs()
    self.setStatusBar(QStatusBar(self))
    self.setCentralWidget(self.tabs)

    self.api.signals.connection_change.connect(self.changeConnectedStatus)
    self.changeConnectedStatus(self.api.isConnected())
    
  def createMenu(self) -> None:
    menu = self.menuBar()

    if menu is None:
      return
    
    connection_menu = menu.addMenu("&Connection")
    course_settings = menu.addMenu("Course &Settings")

    if connection_menu is not None:
      connection_menu.addAction(ConnectAction(self))

    if course_settings is not None:
      course_settings.addAction(CourseSettingsAction(self))

  def createCourseTabs(self) -> None:
    courses = self.canvas.get_courses()
    year = Dependencies.config.settings["current_year"]
    month = Dependencies.config.settings["current_month"]

    for course in courses:
      course = cast(Course, course)
      self.tabs.addTab(CourseTab(course, year, month, self), f"{course.name} ({year}-{getLastTwoDigitsOfYear(year + 1)})")

  def removeAllCourseTabs(self) -> None:
    for i in range(self.tabs.count()):
      self.tabs.removeTab(i)

  def remakeCourseTabs(self) -> None:
    self.removeAllCourseTabs()
    self.createCourseTabs()

  @pyqtSlot(bool)
  def changeConnectedStatus(self, value) -> None:
    title = "(Connected)" if value else "(Not Connected)"
    self.setWindowTitle(self.WINDOW_TITLE.format(c=title))
    




