from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from canvas_pages_generator.ui.ActivityInputBox import ActivityInputBox

from pathlib import Path
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw

from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.core.Utils import toNLengthString
from canvas_pages_generator.core.Utils import isImageOrVideo

class MediaBox(qtw.QLabel):

  id: int
  path: Path
  activityInputBox: ActivityInputBox

  def __init__(self, activityInputBox: ActivityInputBox, id: int, path: Path, parent = None) -> None:
    super().__init__(parent)

    self.path = path
    self.id = id
    self.activityInputBox = activityInputBox

    self.setWordWrap(True)

    pathtype = isImageOrVideo(self.path)

    if pathtype == "image":
      pix = qtg.QPixmap(str(path.absolute()))
      scaled_pixmap = pix.scaled(Constants.MEDIA_BOX_SIZE, qtc.Qt.AspectRatioMode.KeepAspectRatio)
      self.setPixmap(scaled_pixmap)
      self.setStyleSheet("padding: 0px")
    elif pathtype == "video":
      self.setText(toNLengthString(path.stem, 20))
      self.setStyleSheet("border: 1px solid black; font-size: 8pt;")
    else:
      self.setText("Not valid media")
      self.setStyleSheet("border: 1px solid black; font-size: 8pt;")

    self.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
    self.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
    self.setFixedSize(Constants.MEDIA_BOX_SIZE)

  def mousePressEvent(self, ev: qtg.QMouseEvent | None) -> None:
    (self.activityInputBox
      .getActivityInput()
      .getActivitiesArea()
      .getGradeTab()
      .getEventService()
      .dispatch(
        "media_thumbnail_selected",
        self.path,
        self.activityInputBox.id,
        self.id
      )
    )
    return super().mousePressEvent(ev)
  
