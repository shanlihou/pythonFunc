from bmob import BMOB
import json
import ui


class UserInfo(object):
    def __init__(self, objId, host, name, pwd):
        self.objId = objId
        self.host = host
        self.name = name
        self.pwd = pwd


class MyPwd(object):
    def __init__(self):
        self.table = 'myPwd'
        self.infoList = []

    @staticmethod
    def addMyPwd(host, name, pwd):
        data = {'host': host, 'name': name, 'pwd': pwd}
        for k, v in data.items():
            data[k] = BMOB().encrypt(v)
        data = json.dumps(data)
        BMOB().addData('myPwd', data)

    @staticmethod
    def getMyPwd():
        ret = BMOB().get('myPwd')
        ret = json.loads(ret)['results']
        infoList = []
        for pwdInfo in ret:
            host = BMOB().decrypt(pwdInfo['host'])
            name = BMOB().decrypt(pwdInfo['name'])
            pwd = BMOB().decrypt(pwdInfo['pwd'])
            infoList.append(
                UserInfo(pwdInfo['objectId'], host, name, pwd))
        return infoList

    def test(self):
        self.getMyPwd()


class MyTableViewDataSource(object):
    def __init__(self, row_height):
        self.row_height = row_height
        self.width = None
        self.nameList = ['host', 'name', 'pwd']

    def tableview_number_of_rows(self, tableview, section):
        print(tableview.data_source.items)
        if tableview.data_source.items is None:
            return 0

        return len(tableview.data_source.items)

    def tableview_cell_for_row(self, tableview, section, row):
        self.width, height = ui.get_screen_size()
        cell = ui.TableViewCell()
        cell.bounds = (0, 0, self.width, self.row_height)
        for i, name in enumerate(self.nameList):
            item = tableview.data_source.items[row]
            text = getattr(item, name)
            self.make_labels(cell, text, i)

        return cell

    def make_labels(self, cell, text, pos):
        label = ui.Label()
        label.border_color = 'lightgrey'
        label.border_width = 0.5
        label.text = str(text)
        label.action = None
        label.frame = (self.width * 1 / 3 * pos, 0,
                       self.width / 3, self.row_height)
        label.alignment = ui.ALIGN_CENTER
        cell.content_view.add_subview(label)


class MyTableView(ui.View):
    def __init__(self):
        self.myPwd = MyPwd()
        self.tv = ui.TableView()
        self.tv.row_height = 30
        self.tv.data_source = MyTableViewDataSource(self.tv.row_height)
        self.tv.data_source.items = self.myPwd.getMyPwd()
        self.tv.delegate = None
        self.add_subview(self.tv)
        self.tv.reload()

    def layout(self):
        self.tv.reload()
        self.tv.frame = (0, 0, self.width, self.height)


if __name__ == '__main__':
    print('hello')
    MyTableView()
