from __future__ import annotations
from pathlib import Path
import time
from typing import TYPE_CHECKING

from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.core.Month import MonthHandler
from canvas_pages_generator.core.PageCreator import PageCreator
from canvas_pages_generator.core.Utils import nongui
from canvas_pages_generator.ui.GradeTab import GradeTab
from canvas_pages_generator.ui.dialogs.UploadStatusDialog import UploadStatusDialog
if TYPE_CHECKING:
  from canvas_pages_generator.ui.CourseTab import CourseTab

from canvas_pages_generator.core.CanvasTypes import Course
from canvas_pages_generator.core.Dependencies import Dependencies
from canvas_pages_generator.services.UploadService import UploadService


from typing import List
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw
import logging
logger = logging.getLogger(__name__)

from canvas_pages_generator.core.DataModel import DataModel

class UploadWidget(qtw.QWidget):
  
  uploadService: UploadService
  courseTab: CourseTab
  course: Course


  uploadAllButton: qtw.QPushButton
  uploadCurrentButton: qtw.QPushButton

  def __init__(self, courseTab: CourseTab, course: Course) -> None:
    super().__init__(courseTab)

    self.courseTab = courseTab
    self.uploadService = UploadService(course)

    self.defineLayout()

    Dependencies.apiService.signals.connection_change.connect(self.enableUploadButtons)
    self.enableUploadButtons(Dependencies.apiService.isConnected())


  def defineLayout(self) -> None:
    hBox = qtw.QHBoxLayout(self)
    hBox.setContentsMargins(4, 4, 4, 0)

    label = qtw.QLabel("Upload course:")
    label.setObjectName("heading")
    label.setStyleSheet("color: #1c9834;")

    self.uploadAllButton = qtw.QPushButton("Upload all pages")
    self.uploadAllButton.clicked.connect(self.onUploadAll)

    self.uploadCurrentButton = qtw.QPushButton("Create currently open page")
    self.uploadCurrentButton.clicked.connect(self.onUploadCurrent)

    hBox.addWidget(label)
    hBox.addWidget(self.uploadAllButton)
    hBox.addWidget(self.uploadCurrentButton)
    hBox.addStretch(2)

  def onUploadAll(self) -> None:
    self.enableUploadButtons(False)

    modelsToProcess: List[DataModel] = []

    for n in range(self.courseTab.tabs.count()):
      tab = self.courseTab.tabs.widget(n)
      if isinstance(tab, GradeTab):
        modelsToProcess.append(tab.getDataModel())

    statusDialog = UploadStatusDialog(modelsToProcess, self.courseTab)
    statusDialog.show()
    statusDialog.activateWindow()

    for i, model in enumerate(modelsToProcess):
      
      statusDialog.updateStatus(i, "processing")
      logger.info("Processing page %s", model.getPagename())
      qtw.QApplication.processEvents()

      self.processData(model)

      statusDialog.updateStatus(i, "done")
      qtw.QApplication.processEvents()

    statusDialog.close()

    self.enableUploadButtons(True)

  def processData(self, dataModel: DataModel) -> None:
    logger.info("Processing %s", dataModel.getGrade())
    self.uploadNewMedia(dataModel)
    page = self.generatePage(dataModel)
    logger.info("Uploading page for %s", dataModel.getGrade())
    pageUploadResponse = self.uploadService.uploadPage(
      page, 
      dataModel.getPagename()
    )

  def generatePage(self, dataModel: DataModel) -> str:
    return PageCreator(dataModel).getPage()

  def uploadNewMedia(self, model: DataModel) -> None:

    mediaDataFrame = model.getAllMediaForCYID()
    unuploadedMedia = mediaDataFrame.loc[mediaDataFrame["canvas_id"] != None, :]

    for i, media in unuploadedMedia.iterrows():

      path = media["path"]
      logger.info("Uploading media %s", path)

      fileUploadResponse = self.uploadService.uploadToFolder(
        Path(path),
        f"Year{model.getYear()}-{model.getGrade()}"
      )

      if fileUploadResponse is not None:
        model.updateMedia(
          media["id"],
          media["activity_id"],
          path,
          fileUploadResponse["id"],
          fileUploadResponse["uuid"],
          fileUploadResponse["folder_id"],
          fileUploadResponse["url"],
          fileUploadResponse["media_entry_id"]
        )

  def onUploadCurrent(self) -> None:
    self.enableUploadButtons(False)

    currentTab = self.courseTab.tabs.currentWidget()

    if isinstance(currentTab, GradeTab):
      self.processData(currentTab.getDataModel())

    self.enableUploadButtons(True)

  def enableUploadButtons(self, enabled: bool) -> None:
    self.uploadAllButton.setEnabled(enabled)
    self.uploadCurrentButton.setEnabled(enabled)