from typing import List, Optional
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from canvas_pages_generator.core.CanvasTypes import Grade
from canvas_pages_generator.core.Config import Config
from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.core.Dependencies import Dependencies
from canvas_pages_generator.core.Month import Month, MonthHandler
from canvas_pages_generator.core.Utils import getLastTwoDigitsOfYear, sortGrades
from canvas_pages_generator.ui.dialogs.AbstractLabeledItem import AbstractLabeledItem
from canvas_pages_generator.ui.dialogs.LabeledComboBox import LabeledComboBox
from canvas_pages_generator.ui.dialogs.LabeledInput import LabeledInput
from canvas_pages_generator.ui.dialogs.LabeledListWidget import LabeledListWidget
from canvas_pages_generator.ui.dialogs.LabeledSpinBox import LabeledSpinBox

class CourseSettingsDialog(qtw.QDialog):

  config: Config
  courseyear_input: LabeledSpinBox
  coursemonth_input: LabeledComboBox
  coursegrades_input: LabeledListWidget[Grade]

  selectedYear: int
  selectedMonth: int
  selectedGrades: List[Grade]
  ok_button: Optional[qtw.QPushButton] = None

  def __init__(self, parent=None) -> None:
    super().__init__(parent)

    self.config = Dependencies.config

    self.setWindowTitle("Course Settings")
    self.setMinimumWidth(Constants.DIALOG_BOX_WIDTH)

    self.defineLayout()

    self.setValuesToConfigDefaults()


  def defineLayout(self) -> None:
    vbox = qtw.QVBoxLayout(self)
    vbox.setSpacing(12)


    self.courseyear_input = LabeledSpinBox(
      "Course Year:",
      "Set the year that your course starts in the fall",
      True
    )
    self.courseyear_input.getField().setRange(2000, 2999)
    self.courseyear_input.getField().valueChanged.connect(self.onYearChange)


    self.coursemonth_input = LabeledComboBox(
      "Course Month:",
      MonthHandler.getMonthArrayInSchoolOrder(), # type: ignore
      "Select the month that is just starting.",
      True
    )
    self.coursemonth_input.getField().setEditable(False)
    self.coursemonth_input.getField().currentTextChanged.connect(self.onMonthChange)


    self.coursegrades_input = LabeledListWidget[Grade](
      "Grade Levels:",
      Constants.SUPPORTED_GRADES,
      [],
      "Select the grades that you teach.",
      True
    )
    self.coursegrades_input.getField().itemSelectionChanged.connect(self.onGradesChange)

    vbox.addWidget(self.courseyear_input)
    vbox.addWidget(self.coursemonth_input)
    vbox.addWidget(self.coursegrades_input)
    vbox.addSpacing(20)


    buttons = (
      qtw.QDialogButtonBox.StandardButton.Ok | 
      qtw.QDialogButtonBox.StandardButton.Cancel |
      qtw.QDialogButtonBox.StandardButton.Reset)

    self.buttonBox = qtw.QDialogButtonBox(buttons)
    self.buttonBox.accepted.connect(self.accept)
    self.buttonBox.rejected.connect(self.reject)
    
    reset_button = self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Reset)
    if reset_button:
      reset_button.clicked.connect(self.setValuesToConfigDefaults)

    self.ok_button = self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)

    vbox.addWidget(self.buttonBox)
    
    vbox.addStretch(2)

    self.setLayout(vbox)

  def onYearChange(self, value: int) -> None:
    self.selectedYear = value
    self.courseyear_input.setSelectionTipText(
      f"The year will be set to the {value}-{getLastTwoDigitsOfYear(value + 1)} school year"
    )
    

  def onMonthChange(self, value: Month) -> None:
    self.selectedMonth = MonthHandler.monthToIndex(value)
    self.coursemonth_input.setSelectionTipText(
      f"The upcoming month will be {value}, and last month will be {MonthHandler.getLastMonth(value)}"
    )

  def onGradesChange(self) -> None:
    values = self.coursegrades_input.getValue()

    if len(values) == 0:
      self.coursegrades_input.setSelectionTipText("No grades currently selected. You must select at least one grade!")
      self.setOkButtonEnabled(False)
      return
    
    tipText = "Current grades selected: "

    sortedGrades = sortGrades(values)
    self.selectedGrades = sortedGrades

    for grade in sortedGrades:
      tipText += f"{grade}, "

    self.coursegrades_input.setSelectionTipText(tipText[0:-2])
    self.setOkButtonEnabled(True)

  def setOkButtonEnabled(self, enabled: bool) -> None:
    if self.ok_button:
      self.ok_button.setEnabled(enabled)

  def setValuesToConfigDefaults(self) -> None:
    self.selectedYear = self.config.settings["current_year"]
    self.selectedMonth = self.config.settings["current_month"]
    self.selectedGrades = self.config.settings["grades"]

    self.courseyear_input.setValue(self.selectedYear)
    self.onYearChange(self.selectedYear)

    self.coursemonth_input.getField().setCurrentText(
      MonthHandler.getMonth(self.selectedMonth)
    )
    self.onMonthChange(MonthHandler.getMonth(self.selectedMonth))

    self.coursegrades_input.setValue(self.selectedGrades)
    self.onGradesChange()