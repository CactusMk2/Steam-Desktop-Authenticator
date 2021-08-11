import mouse
class Test:
  testmode=False
  def __init__(self, testmode):
    self.testmode=testmode
 
  def initt(self, root):
    if self.testmode:
      # root.lower()
      mouse.click(button="left")

  def on_second(self, var):
    if self.testmode:
      return var-1500
    else:
      return var
