from PyQt6.QtCore import pyqtSignal, QObject

class ApiSignals(QObject):
  connection_change = pyqtSignal(bool)