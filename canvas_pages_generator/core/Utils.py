import os
from pathlib import Path
from typing import List, Literal

from .CanvasTypes import Grade
from .Constants import Constants


def toNLengthString(text: str, length: int) -> str:
  if len(text) <= length:
    return text
  text = text[0:length-3]
  return text + "..."

def isImageOrVideo(filename: Path | str) -> Literal["image", "video"] | None:
  path = Path(filename)

  if path.suffix in Constants.SUPPORTED_IMAGE_TYPES:
    return "image"
  elif path.suffix in Constants.SUPPORTED_VIDEO_TYPES:
    return "video"
  else:
    return None
  
def getLastTwoDigitsOfYear(year: int) -> str:
  ending = year % 100
  if ending < 10:
    return "0" + str(ending)
  return str(ending)

def sortGrades(unsorted_grades: List[Grade]) -> List[Grade]:
  sorted_grades = Constants.SUPPORTED_GRADES
  output: List[Grade] = []

  for grade in sorted_grades:
    if grade in unsorted_grades:
      output.append(grade)

  return output

def makeDirIfNotExists(path: Path | str) -> Path:
  """Returns True if a directory was created."""
  newPath = Path(path)

  if not newPath.exists():
    os.makedirs(newPath, exist_ok=True)
    return newPath
  
  return newPath