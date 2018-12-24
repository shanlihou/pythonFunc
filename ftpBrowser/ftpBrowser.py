import ui
from TabbedView import TabbedView
if __name__ == '__main__':
    v = TabbedView()
    v.addtab(ui.View(name='red', bg_color='red'))
    v.addtab(ui.View(bg_color='blue'))
    v.addtab(ui.View(name='green', bg_color='green'))
    v.addtab(ui.View(name='green', bg_color='green'))
    v.present()
