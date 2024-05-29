# from PyQt6.QtGui import 
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSlot
from canvas_pages_generator.core.Dependencies import Dependencies
from canvas_pages_generator.services.ApiService import ApiService
from canvas_pages_generator.core.Constants import Constants

class ConnectionDialog(QDialog):

  api: ApiService

  button_box: QDialogButtonBox
  retry_button: QPushButton
  close_button: QPushButton

  api_url_label: QLabel
  api_url_input: QLineEdit
  api_token_label: QLabel
  api_token_input: QLineEdit
  connection_status: QLabel
  api_token_instructions: QLabel

  CONNECTION_MESSAGE_CONNECTED: str = "Connection Status: Connected! (User: {u})"
  CONNECTION_MESSAGE_CONNECTING: str = "Connection Status: Trying connection..."
  CONNECTION_MESSAGE_REJECTED: str = "Connection Status: Unable to connect :("
  CONNECTION_MESSAGE_NOTCONNECTED: str = "Connection Status: Not connected"

  def __init__(self, parent=None) -> None:
    super().__init__(parent)

    self.api = Dependencies.apiService

    self.setWindowTitle("Connection settings")
    self.setFixedWidth(Constants.DIALOG_BOX_WIDTH)

    self.api.signals.connection_change.connect(self.setConnectionInfoString)

    self.defineLayout()

    self.setConnectionInfoString(self.api.isConnected())

  def defineLayout(self):
    self.api_url_label = QLabel("API URL")
    self.api_url_input = QLineEdit(Constants.DEFAULT_API_URL, self)

    self.api_token_label = QLabel("API TOKEN")
    self.api_token_input = QLineEdit(Constants.YUTAO_API_TOKEN, self)
    self.api_token_input.setContentsMargins(0, 0, 0, 40)

    self.connection_status = QLabel(self.CONNECTION_MESSAGE_NOTCONNECTED)

    self.api_token_instructions = QLabel(
      "To get an API Token, log into Canvas, go to Settings -> Web Services. "
      "From there you can generate a new token. After creating a new token, "
      "copy it from the browser and paste it here. This token is what allows "
      "this program to connect with your Canvas account." 
      )
    
    self.api_token_instructions.setWordWrap(True)

    self.retry_button = QPushButton("Retry connection", self)
    self.retry_button.clicked.connect(self.retryConnection)
    self.close_button = QPushButton("Close", self)

    self.button_box = QDialogButtonBox()
    self.button_box.addButton(self.retry_button, QDialogButtonBox.ButtonRole.ApplyRole)
    self.button_box.addButton(self.close_button, QDialogButtonBox.ButtonRole.RejectRole)
    self.button_box.accepted.connect(self.accept)
    self.button_box.rejected.connect(self.reject)
    
    
    layout = QVBoxLayout()
    layout.addWidget(self.api_url_label)
    layout.addWidget(self.api_url_input)
    layout.addWidget(self.api_token_label)
    layout.addWidget(self.api_token_input)
    layout.addWidget(self.connection_status)
    layout.addWidget(self.api_token_instructions)
    layout.addWidget(self.button_box)

    self.setLayout(layout)

  @pyqtSlot(bool)
  def setConnectionInfoString(self, connected: bool) -> None:
    connection_message = (
      self.CONNECTION_MESSAGE_CONNECTED.format(u = self.api.getUserName()) 
      if connected
      else self.CONNECTION_MESSAGE_NOTCONNECTED
    )
    self.connection_status.setText(connection_message)
  
  def retryConnection(self):
    self.connection_status.setText("Connecting...")
    Constants.DEFAULT_API_URL = self.api_url_input.text()
    Constants.DEFAULT_API_TOKEN = self.api_token_input.text()

    self.api.createConnection()
      

