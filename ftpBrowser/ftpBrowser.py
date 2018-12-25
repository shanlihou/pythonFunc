import ui
from TabbedView import TabbedView

class LoginView(ui.View):
    def __init__(self):
        self.button_height = 30
        self.viewDict = {}

    def addEdit(self, name):
        edit = ui.TextField()
        edit.name = name
        edit.border_color = 'blue'
        self.add_subview(edit)
        self.viewDict[name] = edit
    
    
if __name__ == '__main__':
    v = TabbedView()
    v.addtab(ui.View(name='red', bg_color='red'))
    v.addtab(ui.View(bg_color='blue'))
    v.addtab(ui.View(name='green', bg_color='green'))
    v.addtab(ui.View(name='green', bg_color='green'))
    v.present()
