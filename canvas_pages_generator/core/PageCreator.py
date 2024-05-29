from pathlib import Path
from typing import List, TypedDict, Literal

from pandas import Series
from canvas_pages_generator.core.Month import Month, MonthHandler
from canvas_pages_generator.core.DataModel import DataModel
from canvas_pages_generator.core.Utils import isImageOrVideo

class PageUpdateRequest(TypedDict):
  title: str
  body: str
  editing_roles: Literal["teachers", "students", "members", "public"]
  notify_of_update: bool
  published: bool

class PageCreator:

  dataModel: DataModel

  BACKGROUND_URL = "/courses/845/files/88867/preview"
  NEXT_MONTH: Month
  LAST_MONTH: Month
  NEXT_MONTH_HEADER = "Here are some of the things we are going to be doing for {m}:"
  LAST_MONTH_HEADER = "Here are some of the things we have been doing in {m}!"
  NEXT_MONTH_TEMPLATE = "<ul style='margin-left: 48px;'>{inner}</ul>"
  SPACER = "<p>&nbsp;</p>"
  HEADER_STYLE = "text-align: center; font-family: 'comic sans ms', sans-serif; font-size: 24pt;"
  MAX_SIZE = 640  # max width and height of images and video

  def __init__(self, dataModel: DataModel) -> None:
    self.dataModel = dataModel
    self.NEXT_MONTH = MonthHandler.getMonth(self.dataModel.getMonth())
    self.LAST_MONTH = MonthHandler.getLastMonth(self.NEXT_MONTH)
    self.NEXT_MONTH_HEADER_TEXT = self.NEXT_MONTH_HEADER.format(m=self.NEXT_MONTH)
    self.LAST_MONTH_HEADER_TEXT = self.LAST_MONTH_HEADER.format(m=self.LAST_MONTH)

  def _generateHeader(self, headerText: str) -> str:
    return """
      <h2 style="{hstyle}">{header}</h2>
      {s}
      """.format(
        header=headerText, 
        s=self.SPACER,
        hstyle=self.HEADER_STYLE
      )

  def _generateNextMonthInfo(self) -> str:

    header = self._generateHeader(self.NEXT_MONTH_HEADER_TEXT)
    
    activity_text = ""

    goals = self.dataModel.getGoalsForCurrentMonth()

    for i, goal in goals.iterrows():
      activity_text += f"""
        <li>{goal["description"]}</li>
        """
      
    body = self.NEXT_MONTH_TEMPLATE.format(inner=activity_text)

    return header + body
  
  def _generateLastMonthInfo(self) -> str:

    header = self._generateHeader(self.LAST_MONTH_HEADER_TEXT)

    activity_text: str = ""

    activities = self.dataModel.getActivitiesForCurrentMonth()

    for i, activity in activities.iterrows():
      activity_text += f"""
        <p style="text-align: center;">{activity["description"]}</p>
        """
      
      mediaList = self.dataModel.getMediaForActivity(activity["id"])
      
      for i, media in mediaList.iterrows():
        activity_text += self._generateImageOrVideoHTML(media)

    return header + activity_text

  def _generateImageOrVideoHTML(self, media: Series) -> str:
    output: str = ""
    path = Path(media["path"])
    filename = path.stem
    type = isImageOrVideo(path)
    
    if type == "image":
      output += """
      <p style="text-align: center;">
        <img 
          style="max-width: {maxs}px; max-height: {maxs}px;"
          src="https://montgomeryschool.instructure.com/courses/845/files/{id}/preview" 
          alt="{displayname}" 
          data-api-endpoint="https://montgomeryschool.instructure.com/api/v1/courses/845/files/{id}" 
          data-api-returntype="File" />
      </p>  
      """.format(
        maxs=self.MAX_SIZE,
        id = media["canvas_id"],
        displayname = filename
      )

    elif type == "video":
      output += """
        <p style="text-align: center;">
          <iframe 
            style="max-width: {maxs}px; max-height: {maxs}px; display: inline-block;" 
            title="{displayname}" 
            data-media-type="video" 
            src="https://montgomeryschool.instructure.com/media_attachments_iframe/{id}?type=video&amp;embedded=true" 
            allowfullscreen="allowfullscreen" 
            allow="fullscreen" 
            data-media-id="{mediaentry}">
          </iframe>
        </p> 
        """.format(
          maxs=self.MAX_SIZE,
          id = media["canvas_id"],
          displayname = filename,
          mediaentry = media["canvas_media_entry_id"]
        )
    
    return output
  
  def _getBody(self) -> str:
    return self._generateNextMonthInfo() + self.SPACER + self.SPACER + self._generateLastMonthInfo()

  def getPage(self) -> str:

    return """
    <div style="
      background-image: linear-gradient(to left, #ffffffcc 0%, #ffffffcc 100%), url('{bg}'); 
      font-family: 'comic sans ms', sans-serif;
      font-size: 18pt;">
    <p>&nbsp;</p>
    {body}
    </div>
    """.format(bg=self.BACKGROUND_URL, body=self._getBody())