from __future__ import annotations
from os import path
from typing import TYPE_CHECKING, Self

from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.ui.CloseButton import CloseButton
if TYPE_CHECKING:
  from canvas_pages_generator.ui.ActivityInput import ActivityInput 

from pathlib import Path
from typing import Any, Callable
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # type: ignore

from canvas_pages_generator.core.DataModel import DataModel
from canvas_pages_generator.ui.AddButton import AddButton
from canvas_pages_generator.ui.MediaBox import MediaBox


class ActivityInputBox(QWidget):

  vBoxLayout: QVBoxLayout
  id: int
  dataModel: DataModel
  activityInput: ActivityInput
  mediaHBox: QHBoxLayout
  addMediaButton: AddButton

  MEDIA_FILTER: str = (
    "Images and Videos (*.jpg *.png *.jpeg *.bmp *.gif *.svg "
    "*.flv *.asf *.qt *.mov *.mpg *.mpeg *.avi *.m4v *.wmv *.mp4 *.3gp)"
  )

  def __init__(
    self, 
    activityInput: ActivityInput, 
    id: int, 
    text: str, 
    onRemove: Callable[[Self], None],
    parent=None
  ) -> None:
    super().__init__(parent)

    self.id = id
    self.activityInput = activityInput
    self.dataModel = self.activityInput.getActivitiesArea().getGradeTab().getDataModel()
    self.vBoxLayout = QVBoxLayout()

    lineedit = QLineEdit(text, self)
    lineedit.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
    lineedit.textChanged.connect(
      lambda newText: self.activityInput.onDescriptionChange(self.id, newText)
    )

    self.mainHbox = QHBoxLayout(self)

    self.vBoxLayout.addWidget(lineedit)

    self.mediaHBox = QHBoxLayout()
    self.mediaHBox.setContentsMargins(16, 0, 0, 0)
    self.mediaHBox.setSpacing(6)
    self.mediaHBox.setAlignment(Qt.AlignmentFlag.AlignLeft)

    media_label = QLabel("Media: ")
    media_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    self.mediaHBox.addWidget(media_label)
    
    self.initializeMediaBoxes(self.mediaHBox)

    self.addMediaButton = AddButton("image or video", self.addMediaAction)
    self.addMediaButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    self.mediaHBox.addWidget(self.addMediaButton)

    self.vBoxLayout.addLayout(self.mediaHBox)

    self.mainHbox.addLayout(self.vBoxLayout)

    removeButton = CloseButton(lambda: onRemove(self))

    self.mainHbox.addWidget(removeButton)

  def initializeMediaBoxes(self, layout: QHBoxLayout) -> None:
    media = self.dataModel.getMediaForActivity(self.id)

    for i, m in media.iterrows():
      path = Path(m["path"])
      if path.exists():
        mediaBox = self.createMediaBox(m["id"], path)
        layout.addWidget(mediaBox)

  def createMediaBox(self, id: int, path: Path) -> MediaBox:
    return MediaBox(self, id, path)

  def addMediaAction(self) -> None:
    filelist, types = QFileDialog.getOpenFileNames(self, "Choose media to upload", None, self.MEDIA_FILTER)
    pathlist = [Path(file) for file in filelist]

    count = self.mediaHBox.count()

    for path in pathlist:
      id = self.dataModel.insertMedia(self.id, str(path))
      mediaBox = self.createMediaBox(id, path)
      self.mediaHBox.insertWidget(count - 1, mediaBox)
      count += 1

  def removeMedia(self, media_id) -> None:
    for child in self.children():
      if isinstance(child, MediaBox) and child.id == media_id:
        self.mediaHBox.removeWidget(child)
        child.deleteLater()
        self.dataModel.removeMedia(media_id)

  def getActivityInput(self) -> ActivityInput:
    return self.activityInput