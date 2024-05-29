from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

from canvas_pages_generator.core.Month import MonthHandler
from canvas_pages_generator.core.PageCreator import PageCreator
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
  
  dataModels: List[DataModel]
  uploadService: UploadService
  courseTab: CourseTab
  course: Course


  uploadAllButton: qtw.QPushButton
  uploadCurrentButton: qtw.QPushButton

  def __init__(self, courseTab: CourseTab, course: Course) -> None:
    super().__init__(courseTab)

    self.courseTab = courseTab
    self.dataModels = []
    self.uploadService = UploadService(course)

    self.defineLayout()

    Dependencies.apiService.signals.connection_change.connect(self.enableUploadButtons)
    self.enableUploadButtons(Dependencies.apiService.isConnected())


  def defineLayout(self) -> None:
    hBox = qtw.QHBoxLayout(self)
    hBox.setContentsMargins(4, 4, 4, 0)

    label = qtw.QLabel("Upload course:")
    label.setObjectName("heading")

    self.uploadAllButton = qtw.QPushButton("Upload all pages")
    self.uploadAllButton.clicked.connect(self.onUploadAll)

    self.uploadCurrentButton = qtw.QPushButton("Upload current page")
    self.uploadCurrentButton.clicked.connect(self.onUploadCurrent)

    hBox.addWidget(label)
    hBox.addWidget(self.uploadAllButton)
    hBox.addWidget(self.uploadCurrentButton)
    hBox.addStretch(2)

  def addDataModel(self, model: DataModel) -> None:
    self.dataModels.append(model)

  def onUploadAll(self) -> None:
    self.enableUploadButtons(False)

    for model in self.dataModels:
      logger.info("Processing %s", model.getGrade())
      self.processData(model)

    self.enableUploadButtons(True)

  def processData(self, dataModel: DataModel) -> None:
    self.uploadNewMedia(dataModel)
    page = self.generatePage(dataModel)
    logger.info("Uploading page for %s", dataModel.getGrade())
    pageUploadResponse = self.uploadService.uploadPage(
      page, 
      f"aa{dataModel.getGrade()}-{MonthHandler.getMonthAbr(dataModel.getMonth())}"
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
    pass

  def enableUploadButtons(self, enabled: bool) -> None:
    self.uploadAllButton.setEnabled(enabled)
    self.uploadCurrentButton.setEnabled(enabled)