import ui
from TabbedView import TabbedView


class LoginView(ui.View):
    def __init__(self):
        self.button_height = 30
        self.viewDict = {}
        self.addEdit('ip')
        self.addEdit('name')
        self.addEdit('pwd')

    def addEdit(self, name):
        edit = ui.TextField()
        edit.name = name
        edit.border_color = 'blue'
        self.add_subview(edit)
        self.viewDict[name] = edit

    def layout(self):
        for index, view in enumerate(self.viewDict.values()):
            view.frame = (0, index * self.button_height, self.width,
                          self.button_height)


if __name__ == '__main__':
    v = TabbedView()
    v.addtab(LoginView())
    v.present()
