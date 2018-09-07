# coding: utf-8
import ui
import os
import datetime
from operator import itemgetter
from search import magnet, getMagnet
import clipboard
import pickle


class MyTableViewDataSource (object):
    def __init__(self, row_height):
        self.row_height = row_height
        self.width = None

    def tableview_number_of_rows(self, tableview, section):
        return len(tableview.data_source.items)

    def tableview_cell_for_row(self, tableview, section, row):
        self.width, height = ui.get_screen_size()
        cell = ui.TableViewCell()
        cell.bounds = (0, 0, self.width, self.row_height)
        for i in range(2):
            self.make_labels(cell, tableview.data_source.items[row][i], i)
        return cell

    def make_labels(self, cell, text, pos):
        label = ui.Label()
        label.border_color = 'lightgrey'
        label.border_width = 0.5
        label.text = str(text)
        label.action = self.copy
        #print('lebal pos:', pos)
        if pos == 0:
            label.frame = (0, 0, self.width * 4 / 5, self.row_height)
        else:
            label.frame = (self.width * 4 / 5, 0,
                           self.width / 5, self.row_height)
        label.alignment = ui.ALIGN_CENTER
        cell.content_view.add_subview(label)

    def copy(self, sender):
        print(sender)


class MyTableViewDelegate(object):
    def __init__(self, info, func):
        self.info = info
        self.func = func
        print(len(self.info))

    def tableview_did_select(self, tableview, section, row):
        self.func.text = 'start'
        print(tableview)
        print(section)
        print(row)
        print(type(row))
        print(len(self.info))
        print(self.info[row])
        url = self.info[row][2]
        if url == 'e':
            return
        mag = getMagnet(url)
        print(mag)
        clipboard.set(mag)
        str_display = 'finished:' + str(row)
        self.func.text = str_display

    def tableview_did_deselect(self, tableview, section, row):
        print('deselect')


class MyTableView(ui.View):
    def __init__(self):
        self.dirs = []
        self.files = []
        self.select_color = 'lightgrey'
        self.unselect_color = 'white'
        self.active_button = None
        self.button_height = 50
        #self.btn_name = self.make_buttons('Name')
        #self.btn_size = self.make_buttons('Size')
        self.make_edit('search')
        func_mody = self.make_text('status')
        self.btn_date = self.make_buttons('search')
        self.tv = ui.TableView()
        self.tv.row_height = 30
        self.tv.data_source = MyTableViewDataSource(self.tv.row_height)
        # self.get_dir()
        #self.all_items = self.dirs + self.files
        #self.mag_info = magnet('海贼王')
        #self.tv.data_source.items = self.all_items
        #info = self.mag_info.get_magnet()
        info = [['q', 'w', 'e']]
        self.tv.data_source.items = info
        self.name = 'TableView-Test'
        self.tv.delegate = MyTableViewDelegate(info, self.status)
        #self.tv.allows_selection = False
        self.tv.action = self.copy
        self.add_subview(self.tv)
        self.present('full_screen')

    def make_text(self, name):
        tx_view = ui.TextView()
        tx_view.name = name
        tx_view.text = 'status'
        self.add_subview(tx_view)
        self.status = tx_view

    def make_edit(self, name):
        edit = ui.TextField()
        edit.name = name
        edit.border_color = 'blue'
        self.add_subview(edit)
        self.search = edit

        def modify_status(str_status):
            edit.text = str_status
        return modify_status

    def make_buttons(self, name):
        button = ui.Button()
        button.name = name
        button.title = name
        button.border_color = 'blue'
        button.border_width = 1
        button.corner_radius = 3
        button.background_color = self.unselect_color
        button.action = self.search_action
        self.add_subview(button)
        return button

    def copy(self, sender):
        print(sender)

    def search_action(self, sender):
        code = self.search.text
        self.mag_info = magnet(code)
        self.tv.data_source.items = self.mag_info.get_magnet()
        self.tv.delegate = MyTableViewDelegate(
            self.mag_info.get_magnet(), self.status)
        self.tv.reload()

    def btn_action(self, sender):
        names = [self.btn_name.name, self.btn_size.name, self.btn_date.name]
        sender_index = names.index(sender.name)
        # thrid click on the same column doesn't work if it's no hardcoded
        # color
        if sender.background_color == (1.0, 1.0, 1.0, 1.0):
            if sender.background_color == self.unselect_color:
                sender.background_color = self.select_color
                self.all_items = sorted(
                    self.all_items, key=itemgetter(sender_index))
            else:
                sender.background_color = self.unselect_color
                self.all_items = sorted(
                    self.all_items, key=itemgetter(sender_index), reverse=True)
        else:
            if self.active_button == None:
                self.active_button = sender.name
            if sender.name == self.btn_name.name:
                self.btn_name.background_color = self.select_color
                self.all_items = sorted(
                    self.all_items, key=itemgetter(sender_index))
            else:
                self.btn_name.background_color = self.unselect_color
            if sender.name == self.btn_size.name:
                self.btn_size.background_color = self.select_color
                self.all_items = sorted(
                    self.all_items, key=itemgetter(sender_index))
            else:
                self.btn_size.background_color = self.unselect_color
            if sender.name == self.btn_date.name:
                self.btn_date.background_color = self.select_color
                self.all_items = sorted(
                    self.all_items, key=itemgetter(sender_index))
            else:
                self.btn_date.background_color = self.unselect_color
        self.tv.data_source.items = self.all_items
        self.tv.reload()
        self.active_button = sender.name

    def layout(self):
        self.tv.reload()
        #self.btn_name.frame =(0*self.width/3, 0, self.width/3, self.button_height)
        #self.btn_size.frame =(1*self.width/3, 0, self.width/3, self.button_height)
        self.search.frame = (0 * self.width / 3, 0, 2 *
                             self.width / 3, self.button_height)
        self.btn_date.frame = (2 * self.width / 3, 0,
                               self.width / 3, self.button_height)
        self.status.frame = (0, self.button_height,
                             self.width, self.button_height)
        self.tv.frame = (0, 2 * self.button_height, self.width,
                         self.height - 2 * self.button_height)

    def get_dir(self):
        path = os.getcwd()
        self.dirs = [] if path == os.path.expanduser(
            '~') else [['..', '<DIR>', 0.0]]
        self.files = []
        for entry in sorted(os.listdir(path)):
            full_pathname = path + '/' + entry
            if os.path.isdir(full_pathname):
                date = os.path.getmtime(full_pathname)
                self.dirs.append((entry, '<DIR>', date))
            else:
                size = os.path.getsize(full_pathname)
                date = os.path.getmtime(full_pathname)
                self.files.append((entry, size, date))


MyTableView()
