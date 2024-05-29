from os import path
from pathlib import Path
import sqlite3
from sqlite3 import Connection
from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.core.Utils import makeDirIfNotExists

class DatabaseService:

  conn: Connection
  database_dir: Path = Constants.DATABASE_DIRECTORY
  isNewDatabase: bool

  def __init__(self) -> None:

    self.isNewDatabase = makeDirIfNotExists(self.database_dir)

    self.conn = sqlite3.connect(
      path.join(self.database_dir, "database.db")
    )

  def getConnection(self) -> Connection:
    return self.conn
