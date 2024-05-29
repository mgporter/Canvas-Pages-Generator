from PyQt6.QtGui import QAction, QKeySequence

from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.ui.dialogs.ConnectionDialog import ConnectionDialog

class ConnectAction(QAction):
  def __init__(self, parent=None):
    super().__init__("Canvas Connection", parent)

    self.setStatusTip("Settings for how this program connects to your Canvas account")
    self.triggered.connect(self.onTriggered)
    self.setShortcut(QKeySequence("Alt+c"))

  def onTriggered(self):
    connection_dialog = ConnectionDialog()
    result = connection_dialog.exec()