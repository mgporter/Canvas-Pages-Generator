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
  tabs: QTabWidget

  WINDOW_TITLE = "Canvas Pages Generator {c}"

  def __init__(self):
    super().__init__()
    
    self.api = Dependencies.apiService
    self.api.createConnection()

    # self.setMinimumSize(QSize(640, 480))
    self.setWindowTitle(self.WINDOW_TITLE.format(c=""))

    self.createMenu()
    self.setStatusBar(QStatusBar(self))

    self.api.signals.connection_change.connect(self.changeConnectedStatus)

    self.refreshWindow()


  def refreshWindow(self) -> None:
    print("refresh window")
    if self.api.isConnected():
      # self.removeAllCourseTabs()
      self.createCourseTabs()
    else:
      self.createConnectionMessage()
    
  def createMenu(self) -> None:
    menu = self.menuBar()

    if menu is None:
      return
    
    connection_menu = menu.addMenu("&Connection")
    course_settings = menu.addMenu("Course &Settings")

    if connection_menu is not None:
      connection_action = ConnectAction(self)
      connection_action.signals.refresh_signal.connect(self.refreshWindow)
      connection_menu.addAction(connection_action)
      # connection_menu.addAction(ConnectAction(self))

    if course_settings is not None:
      course_settings.addAction(CourseSettingsAction(self))

  def createCourseTabs(self) -> None:
    self.tabs = QTabWidget()
    self.tabs.setTabPosition(QTabWidget.TabPosition.North)
    self.tabs.setMovable(False)

    canvas = self.api.getCanvas()

    if canvas is None:
      self.createConnectionMessage()
      return
    
    courses = canvas.get_courses()
    year = Dependencies.config.settings["current_year"]
    month = Dependencies.config.settings["current_month"]

    for course in courses:
      course = cast(Course, course)
      self.tabs.addTab(CourseTab(course, year, month, self), f"{course.name} ({year}-{getLastTwoDigitsOfYear(year + 1)})")

    self.setCentralWidget(self.tabs)

    self.changeConnectedStatus(True)

  def createConnectionMessage(self) -> None:
    message = QLabel("Could not connect to Canvas. Please set the Canvas URL and TOKEN in the Connections menu.")
    message.setWordWrap(True)
    # message.setMaximumWidth(500)
    message.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.setCentralWidget(message)

  def removeAllCourseTabs(self) -> None:
    print(self.tabs.count())
    for i in range(self.tabs.count()):
      self.tabs.removeTab(i)

  def remakeCourseTabs(self) -> None:
    # self.removeAllCourseTabs()
    self.createCourseTabs()

  @pyqtSlot(bool)
  def changeConnectedStatus(self, value) -> None:
    title = "(Connected)" if value else "(Not Connected)"
    self.setWindowTitle(self.WINDOW_TITLE.format(c=title))
    




