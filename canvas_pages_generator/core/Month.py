from typing import List, Literal


Month = Literal['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

class MonthHandler:
  months: List[Month] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  monthArrayInSchoolOrder: List[int] = [8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7]

  @staticmethod
  def getMonth(n: int) -> Month:
    """Gets month name from index. Can handle negative values."""
    while n <= 0:
      n += 12
    return MonthHandler.months[n-1]
  
  @staticmethod
  def getMonthAbr(n: int) -> str:
    return MonthHandler.getMonth(n)[:3]
  
  @staticmethod
  def getMonthArray() -> List[int]:
    return MonthHandler.monthArrayInSchoolOrder
  
  @staticmethod
  def getMonthArrayInSchoolOrder() -> List[Month]:
    return [MonthHandler.getMonth(m) for m in MonthHandler.getMonthArray()]
  
  @staticmethod
  def monthToIndex(month: Month) -> int:
    return MonthHandler.months.index(month) + 1
  
  @staticmethod
  def getLastMonth(month: Month) -> Month:
    if month == 'January':
      return "December"
    else:
      return MonthHandler.getMonth(
        MonthHandler.monthToIndex(month) - 1
      )