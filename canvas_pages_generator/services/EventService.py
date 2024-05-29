from pathlib import Path
from typing import Any, Callable, Dict, Generic, List, Literal, Self, TypeVar, TypedDict

EventType = Literal[
  "media_thumbnail_selected",
  "goals_added_from_selector",
  "media_removed"
]

EventList = TypedDict(
  "EventList", 
  {
    "media_thumbnail_selected": List[Callable[[Path, int, int], None]],
    "goals_added_from_selector": List[Callable[[List[str]], None]],
    "media_removed": List[Callable[[int, int], None]]
  }
)


class EventService():

  events: EventList

  def __init__(self) -> None:
    self.events = {
      "media_thumbnail_selected": [],
      "goals_added_from_selector": [],
      "media_removed": []
    }

  def subscribe(self, type: EventType, cb: Any) -> Callable[[], None]:
    self.events[type].append(cb)

    return lambda: self.events[type].remove(cb)
  
  def dispatch(self, type: EventType, *args) -> None:
    callbackList = self.events[type]

    for cb in callbackList:
      cb(*args)

