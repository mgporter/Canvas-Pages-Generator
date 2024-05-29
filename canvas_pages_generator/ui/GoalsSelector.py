from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from canvas_pages_generator.ui.GoalsArea import GoalsArea

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # type: ignore

from canvas_pages_generator.core.DataModel import DataModel
from canvas_pages_generator.core.Month import MonthHandler


class GoalsSelector(QWidget):
  
  treeWidget: QTreeWidget
  goalsArea: GoalsArea
  
  def __init__(self, goalsArea: GoalsArea, parent=None) -> None:
    super().__init__(parent)

    self.goalsArea = goalsArea
    self.dataModel = goalsArea.getGradeTab().getDataModel()
    self.setMinimumHeight(400)

    mainLayout = QVBoxLayout(self)

    self.treeWidget = self.createSelectorWidget()
    

    button_row = QHBoxLayout()
    addall_button = QPushButton("Add all")
    addall_button.clicked.connect(self.getSelectedItems)
    clearall_button = QPushButton("Clear selection")
    clearall_button.clicked.connect(self.clearAllItems)
    button_row.addWidget(addall_button)
    button_row.addWidget(clearall_button)
    button_row.setAlignment(Qt.AlignmentFlag.AlignRight)

    mainLayout.addWidget(self.treeWidget)
    mainLayout.addLayout(button_row)

    self.setLayout(mainLayout)

  def createSelectorWidget(self) -> QTreeWidget:
    
    data = self.goalsArea.getGradeTab().getDataModel().getGoalsForCurrentYear()

    treeWidget = QTreeWidget()
    treeWidget.setHeaderLabels(["Past goals"])
    treeWidget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    for monthNum in MonthHandler.getMonthArray():
      monthlyData = data[data["month"] == monthNum]

      if not monthlyData.empty:
        monthNode = QTreeWidgetItem(treeWidget, [MonthHandler.getMonth(monthNum)])
        monthNode.setExpanded(True)
      
        for i, row in monthlyData.iterrows():
          QTreeWidgetItem(monthNode, [row["description"]])

    return treeWidget
  
  def getSelectedItems(self) -> None:
    widgetItemList = self.treeWidget.selectedItems()
    itemList = [item.text(0) for item in widgetItemList if item.parent() is not None]
    self.goalsArea.getGradeTab().getEventService().dispatch(
      "goals_added_from_selector",
      itemList
    )
  
  def clearAllItems(self) -> None:
    self.treeWidget.clearSelection()

    

