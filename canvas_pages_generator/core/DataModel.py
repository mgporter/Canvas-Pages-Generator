from typing import List, Tuple

from pandas import DataFrame
from canvas_pages_generator.core.Dependencies import Dependencies
from canvas_pages_generator.services.SqliteRepository import SqliteRepository
from canvas_pages_generator.core.CanvasTypes import Course, Grade

import logging
logger = logging.getLogger(__name__)

class DataModel:

  course_id: int
  course: Course
  grade: Grade
  year: int
  month: int

  cy_id: int  # courseyear id (sqlite identifier for course, grade, and year)

  goals: DataFrame
  activities: DataFrame

  repo: SqliteRepository = Dependencies.repository

  def __init__(self, course: Course, grade: Grade, year: int, month: int) -> None:
    self.course_id = course.id
    self.course = course
    self.grade = grade
    self.year = year
    self.month = month
    self.cy_id = self.queryCYID()

  def getYear(self) -> int:
    return self.year
  
  def getMonth(self) -> int:
    return self.month
  
  def getGrade(self) -> Grade:
    return self.grade

  def queryCYID(self) -> int:
    id = self.repo.getCYID(
      self.course_id,
      self.grade,
      self.year
    )

    if id is None:
      id = self.repo.insertCourseYear(
        self.course_id,
        self.grade,
        self.year
      )

    return id
  
  def getCYID(self) -> int:
    return self.cy_id
  
  def filterBlanks(self, df: DataFrame) -> DataFrame:
    """Returns results without blank descriptions and removes blanks
    from database. The given dataframe MUST have a "description" column."""
    blanks = df.loc[df["description"] == "", "id"]
    for id in blanks:
      self.removeGoal(id)
    return df.loc[df["description"] != "", :]

  def getGoalsForCurrentMonth(self) -> DataFrame:
    return self.filterBlanks(self.repo.getGoals(self.cy_id, self.month))
  
  def getGoalsForCurrentYear(self) -> DataFrame:
    return self.filterBlanks(self.repo.getGoals(self.cy_id))
  
  def updateGoal(self, id: int, text: str, page_id: int | None = None) -> None:
    self.repo.updateGoal(id, text, page_id)

  def removeGoal(self, id: int) -> None:
    self.repo.removeGoal(id)

  def insertGoal(self, text: str) -> int:
    return self.repo.insertGoal(self.cy_id, self.month, None, text)

  def getActivitiesForCurrentYear(self) -> DataFrame:
    return self.filterBlanks(self.repo.getActivities(self.cy_id))
  
  def getActivitiesForCurrentMonth(self) -> DataFrame:
    return self.filterBlanks(self.repo.getActivities(self.cy_id, self.month))
  
  def updateActivity(self, id: int, text: str, page_id: int | None = None) -> None:
    self.repo.updateActivity(id, text, page_id)

  def removeActivity(self, id: int) -> None:
    self.repo.removeActivity(id)

  def insertActivity(self, text: str) -> int:
    return self.repo.insertActivity(self.cy_id, self.month, text)
  
  def getMediaForActivity(self, activity_id: int) -> DataFrame:
    return self.repo.getMedia(activity_id)
  
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
    self.repo.updateMedia(
      id, 
      activity_id, 
      path, 
      canvas_id, 
      canvas_uuid, 
      canvas_folder_id, 
      canvas_url, 
      canvas_media_entry_id
    )

  def removeMedia(self, id: int) -> None:
    self.repo.removeMedia(id)

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
    return self.repo.insertMedia(
      activity_id, 
      path, 
      canvas_id, 
      canvas_uuid, 
      canvas_folder_id, 
      canvas_url, 
      canvas_media_entry_id
    )
  
  def getAllMediaForCYID(self) -> DataFrame:
    return self.repo.getAllMediaForCYID(self.cy_id)