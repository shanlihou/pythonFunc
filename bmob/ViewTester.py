import ui
from TabbedView import TabbedView
from MyPwd import MyPwd
from MyPwd import MyTableView


class MainView(ui.View):
    def __init__(self):
        self.navi = ui.NavigationView()
        self.add_subview(self.navi)
        self.addNavi('123')
        self.addNavi('234')
        self.addNavi('567')
        self.present('full_screen')

    def addNavi(self, name):
        tmpView = ui.TextView()
        tmpView.name = name
        tmpView.text = name
        self.navi.push_view(tmpView)

    def layout(self):
        self.navi.frame = (0, 0, self.width, self.height)


class AddUserInfoView(ui.View):
    def __init__(self):
        self.button_height = 30
        self.viewDict = {}
        self.editNames = ['host', 'name', 'pwd']
        self.addButton('add')
        for name in self.editNames:
            self.addEdit(name)

    def addEdit(self, name):
        edit = ui.TextField()
        edit.name = name
        edit.border_color = 'blue'
        self.add_subview(edit)
        self.viewDict[name] = edit

    def addButton(self, name):
        button = ui.Button()
        button.name = name
        button.title = name
        button.border_color = 'blue'
        button.border_width = 1
        button.corner_radius = 3
        button.action = self.addAction
        self.add_subview(button)
        self.postButton = button

    def addAction(self, sender):
        host = self.viewDict['host'].text
        name = self.viewDict['name'].text
        pwd = self.viewDict['pwd'].text
        print(host, name, pwd)
        MyPwd.addMyPwd(host, name, pwd)

    def layout(self):
        for index, name in enumerate(self.editNames):
            view = self.viewDict[name]
            view.frame = (0, index * self.button_height, self.width,
                          self.button_height)

        self.postButton.frame = (0, 3 * self.button_height, self.width,
                                 self.button_height)


class WebTest(ui.View):
    def __init__(self):
        self.button_height = 30
        self.view = ui.WebView()
        self.view.load_url('https://www.baidu.com')
        self.add_subview(self.view)
        self.addButton('test')

    def addButton(self, name):
        button = ui.Button()
        button.name = name
        button.title = name
        button.border_color = 'blue'
        button.border_width = 1
        button.corner_radius = 3
        button.action = self.testAction
        self.add_subview(button)
        self.testButton = button

    def testAction(self, sender):
        ret = self.view.evaluate_javascript('alert("hello");1;')
        print('ret is:', ret)

    def layout(self):
        self.addButton
        self.testButton.frame = (0, 0, self.width, self.button_height)
        self.view.frame = (0, self.button_height, self.width,
                           self.height - self.button_height)


if __name__ == '__main__':
    v = TabbedView()
    v.addtab(AddUserInfoView())
    v.addtab(MyTableView())
    v.addtab(WebTest())
    v.present()
