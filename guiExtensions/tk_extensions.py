from tkinter import *
from tkinter.ttk import *
from tkinter.font import *

class ScrollableTV(Treeview):
  def __init__(self, master, **kw):
    super().__init__(master, **kw)
    self.columns=[]

  # column now records the name and details of each column in the TV just before they're added
  def column(self, column, **kw):
    if column not in [column[0] for column in self.columns]:
      self.columns.append((column, kw))
    super().column(column, **kw)

  # keep a modified, heavier version of Style around that you can use in cases where ScrollableTVs are involved
  class ScrollableStyle(Style):
    def __init__(self, tv, *args, **kw):
      super().__init__(*args, **kw)
      self.tv = tv

    # override Style's configure method to reset all its TV's columns to their initial settings before it returns into TtkResizeWidget(). since we undo the TV's automatic changes before the screen redraws, there's no need to cause flickering by redrawing a second time after the width is reset
    def configure(self, item, **kw):
      super().configure(item, **kw)
      for column in self.tv.columns:
        name, kw = column
        self.tv.column(name, **kw)