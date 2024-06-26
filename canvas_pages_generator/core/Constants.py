import os
from datetime import datetime
from os import path
from pathlib import Path
from typing import List

from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw

from .CanvasTypes import Grade

current_year = datetime.now().year
current_month = datetime.now().month

if current_month <= 6:
  current_year -= 1

class Constants:
  DEFAULT_FONT_SIZE: int = 14
  
  SECTION_MARGIN: int = 10
  SUBSECTION_MARGIN: int = 25
  SECTION_SPACING: int = 18
  SUBSECTION_SPACING: int = 12
  MEDIA_BOX_SIZE: qtc.QSize = qtc.QSize(64, 42)
  MEDIA_PREVIEW_SIZE: qtc.QSize = qtc.QSize(600, 500)
  DIALOG_BOX_WIDTH: int = 640

  DEFAULT_API_URL: str = "https://YOUR_ORGANIZATION_HERE.instructure.com/"
  DEFAULT_API_TOKEN: str = "<SEE INSTRUCTIONS BELOW>"

  PAGE_FILENAME_TEMPLATE: str = "aa{grade}-{month}"

  PROJECT_HOME: Path = Path(os.getcwd())
  TEST_FILES_DIRECTORY = path.join(PROJECT_HOME, "test_files")
  DEFAULT_DATABASE_DIRECTORY = path.join(PROJECT_HOME, "database")
  DEFAULT_CONFIG_DIRECTORY = path.join(PROJECT_HOME, "config")
  RESOURCES_DIRECTORY = path.join(PROJECT_HOME, "resources")

  DEFAULT_YEAR: int = current_year
  DEFAULT_MONTH: int = current_month
  DEFAULT_GRADES: List[Grade] = ["PreK", "K", "G1", "G2", "G3", "G4"]
  SUPPORTED_GRADES: List[Grade] = ["PreK", "K", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12"]
  SUPPORTED_IMAGE_TYPES: List[str] = [".jpg", ".png", ".jpeg", ".bmp", ".gif", ".svg"]
  SUPPORTED_VIDEO_TYPES: List[str] = [".flv", ".asf", ".qt", ".mov", ".mpg", ".mpeg", ".avi", ".m4v", ".wmv", ".mp4", ".3gp"]
  