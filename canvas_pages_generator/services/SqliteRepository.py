
from sqlite3 import Connection
from typing import List, Optional
import logging

from canvas_pages_generator.core.Constants import Constants
from canvas_pages_generator.core.Utils import makeDirIfNotExists
logger = logging.getLogger(__name__)

from pandas import DataFrame
from canvas_pages_generator.core.CanvasTypes import Grade
from canvas_pages_generator.services.DatabaseService import DatabaseService
import pandas as pd

class SqliteRepository:

  databaseService: DatabaseService
  conn: Connection

  def __init__(
    self, 
    databaseService: DatabaseService
  ) -> None:
    self.databaseService = databaseService
    self.conn = self.databaseService.getConnection()

    # self.dropOldTables()
    self.createTables()
    # self.insertTestData()

  def dropOldTables(self) -> None:
    cur = self.conn.cursor()

    cur.execute("DROP TABLE IF EXISTS media")
    cur.execute("DROP TABLE IF EXISTS activity")
    cur.execute("DROP TABLE IF EXISTS goal")
    cur.execute("DROP TABLE IF EXISTS page")
    cur.execute("DROP TABLE IF EXISTS courseyear")

    cur.close()

  def createTables(self) -> None:
    cur = self.conn.cursor()
    
    cur.execute(
      """CREATE TABLE IF NOT EXISTS courseyear(
        id INTEGER NOT NULL PRIMARY KEY, 
        course_id INTEGER,
        grade TEXT, 
        year INTEGER
      );""")

    cur.execute(
      """CREATE TABLE IF NOT EXISTS page(
        id INTEGER NOT NULL PRIMARY KEY, 
        canvas_id INTEGER,
        cy_id INTEGER,
        month INTEGER, 
        body TEXT,
        FOREIGN KEY (cy_id) REFERENCES courseyear (id)
      );""")
    
    cur.execute(
      """CREATE TABLE IF NOT EXISTS goal(
        id INTEGER NOT NULL PRIMARY KEY, 
        cy_id INTEGER,
        page_id INTEGER,
        month INTEGER, 
        description TEXT,
        FOREIGN KEY (page_id) REFERENCES page (id)
      );""")
    
    cur.execute(
      """CREATE TABLE IF NOT EXISTS activity(
        id INTEGER NOT NULL PRIMARY KEY, 
        cy_id INTEGER,
        page_id INTEGER,
        month INTEGER, 
        description TEXT,
        FOREIGN KEY (page_id) REFERENCES page (id)
      );""")
    
    cur.execute(
      """CREATE TABLE IF NOT EXISTS media(
        id INTEGER NOT NULL PRIMARY KEY, 
        activity_id INTEGER, 
        path TEXT,
        canvas_id INTEGER,
        canvas_uuid TEXT,
        canvas_folder_id INTEGER,
        canvas_url TEXT,
        canvas_media_entry_id TEXT,
        FOREIGN KEY (activity_id) REFERENCES activity (id)
      );""")
    
    cur.close()


  def getCYID(self, course_id: int, grade: Grade, year: int) -> int | None:
    """ Returns a courseyear id, or None if not found. """
    cur = self.conn.cursor()

    sql = f"""
      SELECT id 
      FROM courseyear
      WHERE course_id = ? AND
        grade like ? AND
        year = ?;"""
    
    res = cur.execute(sql, (course_id, grade, year))
    id = res.fetchone()

    cur.close()

    if id is None:
      return None
    
    return id[0]
  
  def getAllCYIDs(self) -> List[int]:
    """ Returns all courseyear ids. """
    cur = self.conn.cursor()

    sql = f"""
      SELECT id 
      FROM courseyear;"""
    
    res = cur.execute(sql)

    ids: List[int] = []

    for id in res.fetchall():
      ids.append(id)

    cur.close()
    
    return ids
  
  def insertCourseYear(self, course_id: int, grade: Grade, year: int) -> int:
    """ Creates a new courseyear entry. """
    cur = self.conn.cursor()

    sql = """
      INSERT INTO courseyear (course_id, grade, year)
      VALUES (?, ?, ?);"""
    
    cur.execute(sql, (course_id, grade, year))
    
    logger.info("courseyear inserted with course_id %d, grade %s, and year %d", course_id, grade, year)

    self.conn.commit()

    rowid_res = cur.execute("SELECT last_insert_rowid()")
    id = rowid_res.fetchone()[0]

    cur.close()

    return id

  def getGoals(self, cy_id: int, month: Optional[int] = None) -> DataFrame:
    sql: str
    
    if month is None:
      sql = f"""
          SELECT *
          FROM goal 
          WHERE cy_id = {cy_id};"""
    else:
      sql = f"""
          SELECT *
          FROM goal 
          WHERE cy_id = {cy_id} AND month = {month};"""
      
    return pd.read_sql_query(sql, self.conn)
  
  def updateGoal(self, id: int, text: str, page_id: int | None) -> None:
    sql = """
      UPDATE goal
      SET description = ?, page_id = ?
      WHERE id = ?;"""

    cur = self.conn.cursor()

    logger.info("Updating goal with id %d", id)
    cur.execute(sql, (text, page_id, id))

    self.conn.commit()

    cur.close()

  def removeGoal(self, id: int) -> None:
    sql = """
      DELETE FROM goal
      WHERE id = ?;"""

    cur = self.conn.cursor()

    logger.info("Deleting goal with local_id %d", id)
    cur.execute(sql, (id,))

    self.conn.commit()

    cur.close()

  def insertGoal(self, cy_id: int, month: int, page_id: int | None, text: str = "") -> int:
    sql = "INSERT INTO goal (cy_id, page_id, month, description) VALUES (?, ?, ?, ?)"

    cur = self.conn.cursor()
    logger.info("inserting goal with cy_id %d, month %d", cy_id, month)
    cur.execute(sql, (cy_id, page_id, month, text))

    self.conn.commit()

    rowid_res = cur.execute("SELECT last_insert_rowid()")
    id = rowid_res.fetchone()[0]

    cur.close()

    return id

  def getActivities(self, cy_id: int, month: Optional[int] = None) -> DataFrame:
    sql: str

    if month is None:
      sql = f"""
        SELECT *
        FROM activity 
        WHERE cy_id = {cy_id};"""
    else:
      sql = f"""
        SELECT *
        FROM activity 
        WHERE cy_id = {cy_id} AND month = {month} ;"""
      
    return pd.read_sql_query(sql, self.conn)

  def updateActivity(self, id: int, text: str, page_id: int | None = None) -> None:
    sql = """
      UPDATE activity
      SET description = ?, page_id = ?
      WHERE id = ?;"""
    cur = self.conn.cursor()

    logger.info("Updating activity with id %d and text %s", id, text)
    cur.execute(sql, (text, page_id, id))

    self.conn.commit()

    cur.close()

  def removeActivity(self, id: int) -> None:
    sql = """
      DELETE FROM activity
      WHERE id = ?;"""

    cur = self.conn.cursor()

    logger.info("Deleting activity with id %d", id)
    cur.execute(sql, (id,))

    self.conn.commit()

    cur.close()
  
  def insertActivity(self, cy_id: int, month: int, description: str, page_id: int | None = None) -> int:
    sql = """
      INSERT INTO activity (cy_id, page_id, month, description) 
      VALUES (?, ?, ?, ?)"""

    cur = self.conn.cursor()
    logger.info("inserting activity with cy_id %d, month %d", cy_id, month)
    cur.execute(sql, (cy_id, page_id, month, description))

    self.conn.commit()

    rowid_res = cur.execute("SELECT last_insert_rowid()")
    id = rowid_res.fetchone()[0]

    cur.close()

    return id
  

  def getMedia(self, activity_id: int) -> DataFrame:
    sql = f"""
      SELECT *
      FROM media 
      WHERE activity_id = {activity_id};"""
      
    return pd.read_sql_query(sql, self.conn)
  
  def getAllMediaForCYID(self, cy_id: int) -> DataFrame:
    sql = f"""
      SELECT *
      FROM media
      WHERE activity_id in (
        SELECT id
        FROM activity
        WHERE cy_id = {cy_id}
      );
      """
    
    return pd.read_sql_query(sql, self.conn)

  def updateMedia(
      self, 
      id: int, 
      activity_id: int | None = None, 
      path: str | None = None, 
      canvas_id: int | None = None, 
      canvas_uuid: str | None = None, 
      canvas_folder_id: int | None = None, 
      canvas_url: str | None = None, 
      canvas_media_entry_id: str | None = None
    ) -> None:
    sql = """
      UPDATE media
      SET 
        activity_id = ?, 
        path = ?,
        canvas_id = ?,
        canvas_uuid = ?,
        canvas_folder_id = ?,
        canvas_url = ?,
        canvas_media_entry_id = ?
      WHERE id = ?;"""
    cur = self.conn.cursor()

    logger.info("Updating media with id %d", id)
    cur.execute(sql, (activity_id, path, canvas_id, canvas_uuid, canvas_folder_id, canvas_url, canvas_media_entry_id, id))

    self.conn.commit()

    cur.close()

  def removeMedia(self, id: int) -> None:
    sql = """
      DELETE FROM media
      WHERE id = ?;"""

    cur = self.conn.cursor()

    logger.info("Deleting media with id %d", id)
    cur.execute(sql, (id,))

    self.conn.commit()

    cur.close()

  def insertMedia(
      self,
      activity_id: int | None = None, 
      path: str | None = None, 
      canvas_id: int | None = None, 
      canvas_uuid: str | None = None, 
      canvas_folder_id: int | None = None, 
      canvas_url: str | None = None, 
      canvas_media_entry_id: str | None = None
    ) -> int:
    sql = """
      INSERT INTO media (activity_id, path, canvas_id, canvas_uuid, canvas_folder_id, canvas_url, canvas_media_entry_id) 
      VALUES (?, ?, ?, ?, ?, ?, ?)"""

    cur = self.conn.cursor()
    logger.info("inserting media with path %s", path)
    cur.execute(
      sql, 
      (
        activity_id, 
        path, 
        canvas_id, 
        canvas_uuid, 
        canvas_folder_id, 
        canvas_url, 
        canvas_media_entry_id
      )
    )

    self.conn.commit()

    rowid_res = cur.execute("SELECT last_insert_rowid()")
    id = rowid_res.fetchone()[0]

    cur.close()

    return id


  def insertTestData(self) -> None:
    cur = self.conn.cursor()

    cy_data = [
      (1, 845, "G4", 2023),
      (2, 845, "K", 2023),
    ]

    # id, course_id, grade, year
    cur.executemany(
      "INSERT INTO courseyear VALUES (?, ?, ?, ?)",
      cy_data
    )

    self.conn.commit()

    # cy_id, page_id, month, description
    goal_data = [
      (1, None, 10, "Maintain the music classroom routines."),
      (1, None, 10, "Continue to strengthen friendly relationships through group dances and music games."),
      (1, None, 10, "Read and notate in stick notation."),
      (1, None, 10, "Review the note names they've learned through singing, spelling games, and keyboard playing on treble staff notation."),
      (1, None, 10, "Learn the basic skills of playing the ukulele. Use the ukulele to play songs including 2 chords."),
      (1, None, 10, "Learn various seasonal songs."),

      (1, None, 11, "Maintain the music classroom routines."),
      (1, None, 11, "Develop basic skills in ukulele playing."),
      (1, None, 11, "Learn the basic chord patterns by playing the ukulele."),
      (1, None, 11, "Continue to maintain the singing voice."),
      (1, None, 11, "Learn various seasonal songs."),
      (1, None, 11, "Get ready for the winter concert."),

      (1, None, 12, "Get ready for the winter concert."),
      (1, None, 12, "Continue to develop basic skills in ukulele playing."),
      (1, None, 12, "Continue learning basic chord patterns by playing the ukulele."),
      (1, None, 12, "Continue to maintain the singing voice."),
      (1, None, 12, "Learn various seasonal songs."),
      (1, None, 12, "Get ready for the winter concert."),
      (1, None, 12, "Evaluate performances and compositions by devising criteria."),
      (1, None, 12, "Discuss each performance and provide evidence of quality moments, as well as areas in need of improvement."),

      (2, None, 10, "Maintain the music classroom routines."),
      (2, None, 10, "Feel confident to say one's own name in front of others."),
      (2, None, 10, "Continue to build friendly relationships through group dances and music games."),
      (2, None, 10, "Continue to follow the cues of a conductor to sing or play percussion."),
      (2, None, 10, "Continue to experience the steady beat within a variety of music activities."),
      (2, None, 10, "Continue to use movement and standard music vocabulary to describe what is heard with active listening."),
      (2, None, 10, "Learn various seasonal songs and game songs by using different voices while singing, according to the content of the music."),
      (2, None, 10, "Use different tempos (fast/slow), beats, and dynamics (loud/soft) to accompany familiar simple songs within specified guidelines"),

      (2, None, 11, "Maintain the music classroom routines."),
      (2, None, 11, "Continue to build friendly relationships through group dances and music games."),
      (2, None, 11, "Continue to use movement and standard music vocabulary to describe what is heard with active listening."),
      (2, None, 11, "Continue to use different tempos (fast/slow), beats, and dynamics (loud/soft) to accompany familiar simple songs within specified guidelines."),
      (2, None, 11, "Follow your own imagination to create lyrics on familiar tunes."),
      (2, None, 11, "Use different dynamics while singing, in accordance with the music content."),
      (2, None, 11, "Learn various seasonal songs and game songs by using different voices while singing, in alignment with the content of the music."),

      (2, None, 12, "Maintain music classroom routines."),
      (2, None, 12, "Continue to use movement and standard music vocabulary to describe what is heard through active listening."),
      (2, None, 12, "Continue to use different tempos (fast/slow), beats, and dynamics (loud/soft) to accompany familiar simple songs within specified guidelines."),
      (2, None, 12, "Use suitable dynamics while singing in accordance with the music content."),
      (2, None, 12, "Learn about pitch (s - m) and rhythm (titi, ta)"),
      (2, None, 12, "Get ready for the Christmas Chapel Singing."),
      (2, None, 12, "Gain large-group singing experience."),
      (2, None, 12, "Evaluate our performances using self-developed criteria."),
      (2, None, 12, "Discuss each performance and provide evidence of quality moments."),
    ]

    cur.executemany(
      "INSERT INTO goal (cy_id, page_id, month, description) VALUES (?, ?, ?, ?)",
      goal_data
    )

    self.conn.commit()

    # id, cy_id, page_id, month, description
    activity_data = [
      (1, 1, None, 10, "Music-making teamwork in action! We explored all the possibilities of playing these non-pitched instruments. When different timbres work together, it creates a nice sound."),
      (2, 1, None, 10, "We created our own story for this song by crafting the lyrics together. We also reviewed general rhythms, such as half notes, quarter notes, eighth notes, and sixteenth notes, from this song."),

      (3, 1, None, 11, "We have finally started to learn the ukulele! We even have an awesome assistant student instructor. The dance in this video was created by Mrs. Song, although we think our version is better."),

      (4, 1, None, 12, "Rehearsal in the bell hall for our winter concert! Ready, go! Hmm... Not sure if we really like this song - \"I'm Getting Nothing for Christmas!\""),

      (5, 2, None, 10, "We are using movement and shakers to imitate the sound of rain while singing the song “Pitter patter."),
      (6, 2, None, 10, "Students really love this game and song! They even create their own lyrics for this Naughty cat."),

      (7, 2, None, 11, "Instead of using voices, we tried using instruments to start a conversation. We listened to each other and cooperated together."),
      (8, 2, None, 11, "Our first experience with rhythm score reading! The different sizes of pumpkins represent the length of each note. We attempted to follow the score while maintaining a steady beat at the same time."),

      (9, 2, None, 12, "Ta-tarata~~. We love marching and playing different instruments with the marching song from “The Nutcracker” by Tchaikovsky! Everyone gets a chance to lead the way!"),


    ]

    cur.executemany(
      "INSERT INTO activity (id, cy_id, page_id, month, description) VALUES (?, ?, ?, ?, ?)",
      activity_data
    )

    self.conn.commit()

    # paths = []
    # testFilesDir = makeDirIfNotExists(Constants.TEST_FILES_DIRECTORY)
    # for file in testFilesDir.iterdir():
    #   paths.append(file)

    # # id, activity_id, path, canvas_id, canvas_uuid, canvas_folder_id, canvas_url, canvas_media_entry_id,
    # media_data = [
    #   (1, str(paths[0]), None, None, None, None, None),
    #   (1, str(paths[1]), None, None, None, None, None),
    #   (2, str(paths[2]), None, None, None, None, None),
    # ]

    # cur.executemany(
    #   "INSERT INTO media (activity_id, path, canvas_id, canvas_uuid, canvas_folder_id, canvas_url, canvas_media_entry_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
    #   media_data
    # )

    # self.conn.commit()


    cur.close()






  

  