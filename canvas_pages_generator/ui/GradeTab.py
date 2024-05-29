from typing import cast
from PyQt6.QtWidgets import QWidget
from canvas_pages_generator.services.EventService import EventService

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # type: ignore

from canvas_pages_generator.core.DataModel import DataModel

import logging

from canvas_pages_generator.ui.ActivitiesArea import ActivitiesArea
from canvas_pages_generator.ui.GoalsArea import GoalsArea
logger = logging.getLogger(__name__)

class GradeTab(QWidget):

  dataModel: DataModel
  eventService: EventService

  def __init__(
      self, 
      dataModel: DataModel,
      parent=None
    ) -> None:
    super().__init__(parent)

    self.dataModel = dataModel
    self.eventService = EventService()

    self.setWindowTitle(self.dataModel.getGrade())
    
    self.defineLayout()


  def defineLayout(self) -> None:

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setContentsMargins(0,0,0,0)

    scrollView = QScrollArea(self)
    scrollView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scrollView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    scrollView.setContentsMargins(0,0,0,0)

    innerWidget = self.defineInnerWidget()
    
    scrollView.setWidget(innerWidget)
    scrollView.setWidgetResizable(True)

    self.mainLayout.addWidget(scrollView)
    self.setLayout(self.mainLayout)

  def defineInnerWidget(self) -> QWidget:
    innerWidget = QWidget()

    innerWidgetLayout = QVBoxLayout(innerWidget)

    goalsWidget = GoalsArea(self)
    actvitiesWidget = ActivitiesArea(self)

    innerWidgetLayout.addWidget(goalsWidget)
    innerWidgetLayout.addWidget(actvitiesWidget)
    innerWidgetLayout.addSpacing(100)

    innerWidget.setLayout(innerWidgetLayout)
    
    return innerWidget

  def getDataModel(self) -> DataModel:
    return self.dataModel
  
  def getEventService(self) -> EventService:
    return self.eventService