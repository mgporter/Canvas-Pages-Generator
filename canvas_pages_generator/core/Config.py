import sys
import json
from pathlib import Path
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
      "grades": List[Grade],
      "api_url": str,
      "api_token": str,
      "database_dir": str
    }
  )

class Config:

  config_dir: Path
  config_file: Path
  config: configparser.ConfigParser = configparser.ConfigParser()

  # Program settings
  settings: Settings

  def __init__(self) -> None:

    self.config_dir = makeDirIfNotExists(Constants.DEFAULT_CONFIG_DIRECTORY)
    self.config_file = Path.joinpath(self.config_dir, "config.ini")

    configs = self._readConfigurationFile()

    if len(configs) == 0:
      # config file does not exist
      self._initializeDefaults()
      self._writeToConfigurationFile()
      self._readConfigurationFile()

    self.settings = self._loadValuesFromFile()

  def _readConfigurationFile(self) -> List[str]:
    return self.config.read(self.config_file)
  
  def _writeToConfigurationFile(self) -> None:
    with open(self.config_file, 'w') as cfile:
      self.config.write(cfile)

  def saveSetting(self, key: str, value: Any) -> None:
    """Use this method to save config settings. If an invalid
     key is given, a KeyError exception will be thrown. """
    if key not in self.settings:
      raise KeyError("No such key {} in config file.", key)
    self.config["DEFAULT"][key] = json.dumps(value)
    self.settings[key] = value  # type: ignore
    self._writeToConfigurationFile()

  # For later: do this automatically somehow
  def _loadValuesFromFile(self) -> Settings:
    return {
      "current_year": self.config["DEFAULT"].getint("current_year"),
      "current_month": self.config["DEFAULT"].getint("current_month"),
      "grades": json.loads(self.config["DEFAULT"].get("grades")),
      "api_url": json.loads(self.config["DEFAULT"].get("api_url")),
      "api_token": json.loads(self.config["DEFAULT"].get("api_token")),
      "database_dir": json.loads(self.config["DEFAULT"].get("database_dir"))
    }

  def _initializeDefaults(self) -> None:
    self.config['DEFAULT'] = {
      "current_year": str(Constants.DEFAULT_YEAR),
      "current_month": str(Constants.DEFAULT_MONTH),
      "grades": json.dumps(Constants.DEFAULT_GRADES),
      "api_url": json.dumps(Constants.DEFAULT_API_URL),
      "api_token": json.dumps(Constants.DEFAULT_API_TOKEN),
      "database_dir": json.dumps(Constants.DEFAULT_DATABASE_DIRECTORY)
    }

  def getSettings(self) -> Settings:
    return self.settings