import sys
import logging
from PyQt6.QtWidgets import QApplication
from .Dependencies import Dependencies
from canvas_pages_generator.stylesheets.StyleSheets import StyleSheets
from canvas_pages_generator.ui.MainWindow import MainWindow

logger = logging.getLogger(__name__)


class MainGui:

  @staticmethod
  def start() -> None:

    loggingFormat = "%(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
      stream=sys.stdout, 
      level=logging.INFO, 
      format=loggingFormat
    )

    logger.info("Starting Api connection")
    apiService = Dependencies.apiService
    apiService.createConnection()

    logger.info("Starting PyQt")
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheets.APP)

    window = MainWindow()
    window.show()

    app.exec()