from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from canvas_pages_generator.core.Utils import isImageOrVideo
from canvas_pages_generator.core.Constants import Constants
if TYPE_CHECKING:
  from canvas_pages_generator.ui.ActivitiesArea import ActivitiesArea

from pathlib import Path
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw

from canvas_pages_generator.services.EventService import EventService


class ActivityPreviewWindow(qtw.QWidget):

  vBoxLayout: qtw.QVBoxLayout
  activity_id: int
  media_id: int
  activitiesArea: ActivitiesArea
  eventService: EventService

  placeholder: qtw.QLabel
  current_img: qtw.QLabel
  previewContainer: qtw.QWidget
  previewContainerLayout: qtw.QVBoxLayout

  def __init__(self, activitiesArea: ActivitiesArea, parent=None) -> None:
    super().__init__(parent)

    self.id = -1
    self.activitiesArea = activitiesArea
    self.eventService = self.activitiesArea.getGradeTab().getEventService()

    self.eventService.subscribe(
      "media_thumbnail_selected",
      self.onMediaSelected
    )

    self.vBoxLayout = qtw.QVBoxLayout()
    self.vBoxLayout.setSpacing(8)
    self.vBoxLayout.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)

    self.current_img = self.createPlaceHolder()

    self.previewContainer = qtw.QWidget()
    self.previewContainer.setFixedSize(Constants.MEDIA_PREVIEW_SIZE)
    self.previewContainer.setSizePolicy(
      qtw.QSizePolicy.Policy.Maximum,
      qtw.QSizePolicy.Policy.Maximum
    )
    self.previewContainerLayout = qtw.QVBoxLayout(self.previewContainer)
    self.previewContainerLayout.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
    self.previewContainerLayout.addWidget(self.current_img)
    self.previewContainerLayout.setContentsMargins(0,0,0,0)
    self.previewContainer.setLayout(self.previewContainerLayout)

    remove_button = qtw.QPushButton("Remove")
    remove_button.setSizePolicy(
      qtw.QSizePolicy.Policy.Fixed,
      qtw.QSizePolicy.Policy.Fixed
    )
    remove_button.clicked.connect(lambda: self.onRemoveButtonClicked())

    self.vBoxLayout.addWidget(self.previewContainer)
    self.vBoxLayout.addWidget(remove_button)

    self.setLayout(self.vBoxLayout)

  def onMediaSelected(self, path: Path, activity_id: int, media_id: int) -> None:
    self.activity_id = activity_id
    self.media_id = media_id

    label = qtw.QLabel("")
    label.setWordWrap(True)

    pathtype = isImageOrVideo(path)

    if pathtype == "image":
      pixmap = qtg.QPixmap(str(path.absolute()))
      scaled_pixmap = pixmap.scaled(Constants.MEDIA_PREVIEW_SIZE, qtc.Qt.AspectRatioMode.KeepAspectRatio)
      label.setPixmap(scaled_pixmap)
    elif pathtype == "video":
      label.setText("Video previews are not supported yet!")
    else:
      label.setText("This filetype is not supported.")

    self.setPreviewPaneImage(label)

  def setPreviewPaneImage(self, image: qtw.QLabel) -> None:
    self.previewContainerLayout.removeWidget(self.current_img)
    self.current_img.deleteLater()
    self.previewContainerLayout.addWidget(image)

    self.current_img = image

  def createPlaceHolder(self) -> qtw.QLabel:
    placeholder = qtw.QLabel("Media Preview")
    placeholder.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
    placeholder.setStyleSheet(
      "background-color: transparent;"
      "color: gray;"
      "border: 1px solid black"
    )

    placeholder.setSizePolicy(
      qtw.QSizePolicy.Policy.Expanding,
      qtw.QSizePolicy.Policy.Expanding
    )

    return placeholder
    
  def onRemoveButtonClicked(self) -> None:
    self.eventService.dispatch(
      "media_removed",
      self.activity_id,
      self.media_id
    )
    self.setPreviewPaneImage(self.createPlaceHolder())