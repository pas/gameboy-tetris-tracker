import datetime
import humanize

class RoundValues:
  def __init__(self, start : datetime.date, end : datetime.date, time_passed : datetime.time):
    self.start = start
    self.end = end
    self.time_passed = time_passed

  def __str__(self):
    return "Start: " + datetime.datetime.strftime(self.start, "%Y/%m/%d %H:%M:%S") + \
            " End: " + datetime.datetime.strftime(self.end, "%Y/%m/%d %H:%M:%S") + \
            " Time: " + str(self.time_passed)
