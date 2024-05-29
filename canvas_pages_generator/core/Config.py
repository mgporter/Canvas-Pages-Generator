from os import path
import json
from typing import Any, List, TypedDict

from canvas_pages_generator.core.Utils import makeDirIfNotExists
from canvas_pages_generator.core.CanvasTypes import Grade
from canvas_pages_generator.core.Constants import Constants
import configparser

Settings = TypedDict(
    "Settings",
    {
      "current_year": int,
      "current_month": int,
      "grades": List[Grade]
    }
  )

class Config:

  config_dir = Constants.CONFIG_DIRECTORY
  config_file = path.join(config_dir, "config.ini")
  config = configparser.ConfigParser()

  # Program settings
  settings: Settings

  def __init__(self) -> None:

    makeDirIfNotExists(self.config_dir)

    configs = self.readConfigurationFile()

    if len(configs) == 0:
      # config file does not exist
      self.initializeDefaults()
      self.writeToConfigurationFile()
      
      self.readConfigurationFile()

    self.settings = self.loadValuesFromFile()

  def readConfigurationFile(self) -> List[str]:
    return self.config.read(self.config_file)
  
  def writeToConfigurationFile(self) -> None:
    with open(self.config_file, 'w') as cfile:
      self.config.write(cfile)

  def saveValue(self, key: str, value: Any) -> None:
    """Use this method to save config settings. If an invalid
     key is given, a KeyError exception will be thrown. """
    if key not in self.settings:
      raise KeyError("No such key {} in config file.", key)
    self.config["DEFAULT"][key] = json.dumps(value)
    self.settings[key] = value  # type: ignore
    self.writeToConfigurationFile()

  # For later: do this automatically somehow
  def loadValuesFromFile(self) -> Settings:
    return {
      "current_year": self.config["DEFAULT"].getint("current_year"),
      "current_month": self.config["DEFAULT"].getint("current_month"),
      "grades": json.loads(self.config["DEFAULT"].get("grades"))
    }

  def initializeDefaults(self) -> None:
    self.config['DEFAULT'] = {
      "current_year": str(Constants.DEFAULT_YEAR),
      "current_month": str(Constants.DEFAULT_MONTH),
      "grades": json.dumps(Constants.DEFAULT_GRADES)
    }

  def getSettings(self) -> Settings:
    return self.settings