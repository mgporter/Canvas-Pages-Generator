from os import path
from pathlib import Path
import sqlite3
from sqlite3 import Connection
from canvas_pages_generator.core.Config import Config
from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.core.Utils import makeDirIfNotExists

class DatabaseService:

  conn: Connection
  database_dir: Path
  config: Config

  def __init__(self, config: Config) -> None:

    self.config = config

    self.database_dir = makeDirIfNotExists(self.config.getSettings()["database_dir"])

    self.conn = sqlite3.connect(
      path.join(self.database_dir, "database.db")
    )

    # Turn on foreign key support
    self.conn.execute("PRAGMA foreign_keys = ON;")

  def getConnection(self) -> Connection:
    return self.conn
