#!/usr/bin/python3
class Bubble():
    name_tag = """<p class="name">{}</p>"""
    bubble = """
  <div class="bubble{0}">
    <div class="txt">
      {1}
      <p class="message">{2}</p>
      <span class="timestamp">{3}</span>
    </div>
    {4}
  </div>
  """

    def __init__(self, name, message, time, left=True, hideName=False, hideArrow=False):
        self.name = name
        self.message = message
        self.time = time
        self.left = left
        self.hideName = hideName
        self.hideArrow = hideArrow

    def setName(self, name):
        self.name = name

    def setMessage(self, message):
        self.message = message

    def setTime(self, time):
        self.time = time

    def setLeft(self, left):
        self.left = left

    def doHideName(self):
        self.hideName = True

    def doHideArrow(self):
        self.hideArrow = True

    def addSeparation(self):
        self.bubble += '<br>'

    def inflate(self):
        alt = "" if self.left else " alt"
        name_div = "" if self.hideName else self.name_tag.format(self.name)
        arrow = '' if self.hideArrow else '<div class="bubble-arrow{0}"></div>'.format(alt)

        return self.bubble.format(alt, name_div, self.message, self.time, arrow)


class Broadcast():

    content = """
    <div class="broadcast">
        <p class="broadcast_txt">{}</p>
    </div>
    """

    def __init__(self, message):
        self.message = message

    def inflate(self):
        return self.content.format(self.message)


class Datestamp():

    content = """
    <div class="date">
        <p class="date_txt">{}</p>
    </div>
    """

    def __init__(self, date):
        self.date = date

    def inflate(self):
        return self.content.format(self.date)
