import os
from os import path
from pathlib import Path
from typing import List

from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw

from .CanvasTypes import Grade


class Constants:
  DEFAULT_FONT_SIZE: int = 14
  
  SECTION_MARGIN: int = 10
  SUBSECTION_MARGIN: int = 25
  SECTION_SPACING: int = 18
  SUBSECTION_SPACING: int = 12
  MEDIA_BOX_SIZE: qtc.QSize = qtc.QSize(64, 42)
  MEDIA_PREVIEW_SIZE: qtc.QSize = qtc.QSize(600, 500)
  DIALOG_BOX_WIDTH: int = 640

  DEFAULT_API_URL: str = "https://montgomeryschool.instructure.com/"
  YUTAO_API_TOKEN: str = "14162~som8NXE370MK0x7g7QlesROizCBHfTmvVBQYZgSGDNRwFerAwGq3H3iLO3yz2DuN"
  DEFAULT_API_TOKEN: str = "14162~som8NXE370MK0x7g7QlesROizCBHfTmvVBQYZgSGDNRwFerAwGq3H3iLO3yz2DuN"

  PROJECT_HOME: Path = Path(os.getcwd())
  FILES_DIRECTORY = Path(path.join(PROJECT_HOME, "files"))
  DATABASE_DIRECTORY = Path(path.join(PROJECT_HOME, "database"))
  CONFIG_DIRECTORY = Path(path.join(PROJECT_HOME, "config"))

  DEFAULT_YEAR: int = 2023
  DEFAULT_MONTH: int = 9
  DEFAULT_GRADES: List[Grade] = ["PreK", "K", "G1", "G2", "G3", "G4"]
  SUPPORTED_GRADES: List[Grade] = ["PreK", "K", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12"]
  SUPPORTED_IMAGE_TYPES: List[str] = [".jpg", ".png", ".jpeg", ".bmp", ".gif", ".svg"]
  SUPPORTED_VIDEO_TYPES: List[str] = [".flv", ".asf", ".qt", ".mov", ".mpg", ".mpeg", ".avi", ".m4v", ".wmv", ".mp4", ".3gp"]
  