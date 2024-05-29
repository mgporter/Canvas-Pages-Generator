import logging
from typing import Optional
from canvasapi import Canvas # type: ignore
from canvas_pages_generator.services.ApiSignals import ApiSignals
from canvas_pages_generator.core.Constants import Constants
from canvasapi.current_user import CurrentUser # type: ignore
from canvasapi.exceptions import CanvasException # type: ignore

logger = logging.getLogger(__name__)

_canvas: Optional[Canvas] = None
_user: Optional[CurrentUser] = None
_username: str = ""
_userid: int = 0
_connected: bool = False
_errors: str = ""


class ApiService():

  # connection_change: pyqtBoundSignal

  def __init__(self) -> None:
    self.signals = ApiSignals()

  def createConnection(self) -> bool:
    global _canvas

    logger.info(f"Connecting to Api with URL {Constants.DEFAULT_API_URL}"
                f" and Token {Constants.DEFAULT_API_TOKEN}")

    try:
      self._resetStatus()
      _canvas = Canvas(
        Constants.DEFAULT_API_URL, 
        Constants.DEFAULT_API_TOKEN
      )
      self.updateConnectedUser()
      return True
    except Exception as e:
      logger.exception(
        f"Error connecting to Api with URL {Constants.DEFAULT_API_URL}"
        f" and Token {Constants.DEFAULT_API_TOKEN}", e
      )
      self._resetStatus()
      self.emitConnectionChangeSignal()
      return False

  def getCanvas(self) -> Canvas | None:
    global _canvas 
    if _canvas == None:
      self.createConnection()
    return _canvas

  def updateConnectedUser(self) -> None:
    global _canvas
    global _user
    global _username
    global _userid
    global _connected
    global _errors

    if _canvas == None:
      return
    
    try:
      assert _canvas is not None
      _user = _canvas.get_current_user()
      _username = _user.name
      _userid = _user.id
      _connected = True
    except CanvasException as e:
      _connected = False

      logger.error(f"Error getting user information from Api")

      error = e.message
      if isinstance(error, str):
        _errors = error
      elif isinstance(error, list):
        if len(error) > 0:
          error = error[0]
          if isinstance(error, str):
            _errors = error
          elif isinstance(error, dict):
            _errors = error["message"]

    self.emitConnectionChangeSignal()
  
  def emitConnectionChangeSignal(self) -> None:
    global _connected
    self.signals.connection_change.emit(_connected)

  def getUserName(self) -> str:
    global _connected
    global _username

    if _connected == False:
      return ""
    return _username

  def getUserId(self) -> int:
    global _connected
    global _userid

    if _connected == False:
      return 0
    return _userid

  def isConnected(self) -> bool:
    global _connected
    return _connected
  
  def getErrors(self) -> str:
    global _errors
    return _errors

  def _resetStatus(self) -> None:
    global _canvas
    global _user
    global _username
    global _userid
    global _connected
    global _errors
    _canvas = None
    _user = None
    _username = ""
    _userid = 0
    _connected = False
    _errors = ""