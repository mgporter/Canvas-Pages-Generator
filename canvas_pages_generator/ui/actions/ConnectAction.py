from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal, QObject

from canvas_pages_generator.core.Dependencies import Dependencies
from canvas_pages_generator.ui.dialogs.ConnectionDialog import ConnectionDialog

class ConnectionSignal(QObject):
  refresh_signal = pyqtSignal(bool)

class ConnectAction(QAction):

  signals: ConnectionSignal

  def __init__(self, parent=None):
    super().__init__("Canvas Connection", parent)

    self.signals = ConnectionSignal()

    self.setStatusTip("Settings for how this program connects to your Canvas account")
    self.triggered.connect(self.onTriggered)
    self.setShortcut(QKeySequence("Alt+c"))

  def onTriggered(self):

    oldToken = Dependencies.config.settings["api_token"]
    oldUrl = Dependencies.config.settings["api_url"]

    connection_dialog = ConnectionDialog()
    connection_dialog.exec()

    if (Dependencies.config.settings["api_token"] != oldToken or 
        Dependencies.config.settings["api_url"] != oldUrl):
      self.signals.refresh_signal.emit(True)
      print("signal emitted")

