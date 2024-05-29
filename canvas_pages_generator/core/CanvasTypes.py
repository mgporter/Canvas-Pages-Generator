from typing import Literal, Optional, TypedDict
from canvasapi.course import Folder as CAFolder # type: ignore
from canvasapi.course import Course as CACourse # type: ignore
from canvasapi.page import Page as CAPage # type: ignore
from canvasapi.section import Section as CASection # type: ignore

class Page(CAPage):
  page_id: int
  url: str
  title: str
  created_at: str
  updated_at: str
  # "hide_from_students": false, DEPRECATED
  editing_roles: Literal["teachers", "students", "members", "public"]
  last_edited_by: Optional[str]
  body: str
  published: bool
  publish_at: str
  front_page: bool
  locked_for_user: bool
  lock_info: Optional[str]
  lock_explanation: Optional[str]


class Course(CACourse):
  id: int
  sis_course_id: Optional[int]
  uuid: str
  integration_id: Optional[str]
  sis_import_id: Optional[int]
  name: str # will be nickname for course if one is set
  course_code: str
  original_name: str
  workflow_state: Literal["unpublished", "available", "completed", "deleted"]
  account_id: int
  root_account_id: int
  enrollment_term_id: int
  # grading_periods: Optional[]
  grading_standard_id: int
  grade_passback_setting: str
  created_at: str
  start_at: str
  end_at: str
  locale: str
  # enrollments: Optional[]
  total_students: int
  # calendar: Optional[]
  default_view: Literal["feed", "wiki", "modules", "assignments", "syllabus"]
  syllabus_body: str # html code
  needs_grading_count: int
  # term: Optional[]
  # course_progress: null
  apply_assignment_group_weights: bool
  # permissions: Optional[]{"create_discussion_topic":true,"create_announcement":true},
  is_public: bool
  is_public_to_auth_users: bool
  public_syllabus: bool
  public_syllabus_to_auth: bool
  public_description: str
  storage_quota_mb: int
  storage_quota_used_mb: int
  hide_final_grades: bool
  license: str
  allow_student_assignment_edits: bool
  allow_wiki_comments: bool
  allow_student_forum_attachments: bool
  open_enrollment: bool
  self_enrollment: bool
  restrict_enrollments_to_course_dates: bool
  course_format: str
  access_restricted_by_date: Optional[bool]
  time_zone: str
  blueprint: Optional[bool]
  # "blueprint_restrictions": Optional{"content":true,"points":true,"due_dates":false,"availability_dates":false},
  # "blueprint_restrictions_by_object_type": Optional[]{"assignment":{"content":true,"points":true},"wiki_page":{"content":true}},
  template: Optional[bool]


class Section(CASection):
  id: int
  name: str
  sis_section_id: Optional[str]
  integration_id: Optional[str]
  sis_import_id: Optional[int]
  course_id: int
  sis_course_id: Optional[str]
  start_at: str
  end_at: Optional[str]
  restrict_enrollments_to_section_dates: Optional[bool]
  nonxlist_course_id: Optional[int]
  total_students: int

File = TypedDict(
  "File",
  {
    "id": int,
    "uuid": str,
    "folder_id": int,
    "display_name": str,
    "filename": str,
    "content-type": str,
    "url": str,
    "size": int,
    "created_at": str,
    "updated_at": str,
    "unlock_at": str,
    "locked": bool,
    "hidden": bool,
    "lock_at": str,
    "hidden_for_user": bool,
    "visibility_level": Literal["inherit", "course", "institution", "public"],
    "thumbnail_url": Optional[str],
    "modified_at": str,
    "mime_class": str,
    "media_entry_id": str,
    "locked_for_user": bool,
    "preview_url": str,
  }
)

# Differences
# File: lock_info, lock_explanation
    # "lock_info": Optional[str],
    # "lock_explanation": str,
# FileUploadResponse: instfs_uuid, category

# FileUploadResponse = TypedDict(
#   "FileUploadResponse",
#   {
#     'location': str, 
#     'instfs_uuid': str, 
#     'id': int, 
#     'uuid': str, 
#     'folder_id': int, 
#     'display_name': str, 
#     'filename': str, 
#     'upload_status': str, 
#     'content-type': str, 
#     'url': str, 
#     'size': int, 
#     'created_at': str, 
#     'updated_at': str, 
#     'unlock_at': Optional[str], 
#     'locked': bool, 
#     'hidden': bool, 
#     'lock_at': Optional[str], 
#     'hidden_for_user': bool, 
#     'thumbnail_url': Optional[str], 
#     'modified_at': str, 
#     'mime_class': str, 
#     'media_entry_id': Optional[int], 
#     'category': str, 
#     'locked_for_user': bool, 
#     'visibility_level': Literal["inherit", "course", "institution", "public"],
#     'preview_url': str,
#   }
# )

class Folder(CAFolder):
  context_type: str
  context_id: int
  files_count: int
  position: int
  updated_at: str
  folders_url: str
  files_url: str
  full_name: str
  lock_at: str
  id: int
  folders_count: int
  name: str
  parent_folder_id: int
  created_at: str
  unlock_at: Optional[str]
  hidden: bool
  hidden_for_user: bool
  locked: bool
  locked_for_user: bool
  for_submissions: bool


class FileUploadArgs(TypedDict):
  parent_folder_path: Optional[str]
  on_duplicate: Optional[Literal["overwrite", "rename"]]

Grade = Literal["PreK", "K", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12"]