class FileUploadException(Exception):
  
  def __init__(self, message: str | None) -> None:
    self.message = message

  def __str__(self):
    return str(self.message)