from pathlib import Path
from typing import List, cast
from canvas_pages_generator.core.CanvasTypes import Course, File, Folder, Page

class UploadService:

  course: Course

  def __init__(self, course: Course):
    self.course = course

  def getId(self) -> int:
    return self.course.id
  
  def getName(self) -> str:
    return self.course.name
  
  def getCourseCode(self) -> str:
    return self.course.course_code
  
  def getCourse(self) -> Course:
    return self.course
  
  def getFolders(self) -> List[Folder]:
    folders = self.course.get_folders()
    return [cast(Folder, x) for x in folders]

  def getFile(self, id: int) -> File:
    return self.course.get_file(id)

  def uploadToFolder(self, path: Path, dest_folder: str) -> File | None:
    if not path.exists() or not path.is_file():
      return None
    
    result, response = self.course.upload(
      path,
      parent_folder_path = dest_folder,
    )

    if result is False:
      return None
    
    return response 
  
  def uploadPage(self, body: str, title: str, published: bool = True) -> Page:
    return self.course.create_page({
      "title": title,
      "body": body,
      "published": published
    })
  
  def uploadDirToFolder(self, dirpath: Path, dest_folder: str) -> List[File | None]:
    responses: List[File | None] = []
    if not dirpath.is_dir():
      return responses
    
    for path in dirpath.iterdir():
      response = self.uploadToFolder(
          path,
          dest_folder
        )
      responses.append(response)
        
    return responses