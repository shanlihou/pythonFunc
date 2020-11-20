import utils
import const
import Filter
import json
import time


class LogOneBase(object):
    def __init__(self, time_str, open_id, gbid):
        self.time_str = time_str
        self.timestamp = utils.get_time_stamp(time_str)
        self.day = utils.get_day(time_str)
        self.account = open_id
        self.gbid = gbid

    def get_day(self):
        return self.day

    def unique_key(self):
        if const.UNIQUE_BY_ACCOUNT:
            return self.account
        else:
            return self.gbid



class LogOne(LogOneBase):
    def __init__(self, log_type, server_id, time_str, app_id, plant_id,
                 area_id, zone_id, open_id, client_ver, sec_report_data,
                 sys_software, *args):
        super().__init__(time_str, open_id, args[6])
        self.name = args[7]

    @staticmethod
    def get_log_obj_from_line(line):
        tup = line.strip().split('|')
        return LogOne(*tup)


class LogVitality(LogOneBase):
    def __init__(self, log_type, server_id, time_str, _1, gbid, _2, _3, uuid, _4, activity):
        account = Filter.Filter.get_gbid_2_account_dic()[gbid]
        super().__init__(time_str, account, gbid)
        self.act = activity.strip().split(' ')[-1]

    @staticmethod
    def get_log_obj_from_line(line):
        tup = line.strip().split('|')
        try:
            return LogVitality(*tup)
        except:
            return None


class LogOut(LogOneBase):
    def __init__(self, log_type, server_id, time_str, app_id, plant_id,
                 area_id, zone_id, open_id, client_ver, sec_report_data,
                 sys_software, *args):
        gbid = args[6]
        level = args[9]
        super().__init__(time_str, open_id, gbid)
        self.level = level

    @staticmethod
    def get_log_obj_from_line(line):
        tup = line.strip().split('|')
        try:
            return LogOut(*tup)
        except:
            return None


class LogSys(LogOneBase):
    def __init__(self, data_dict):
        self.gbid = data_dict['gbId']
        timestamp = data_dict['timestamp'] // 1000
        time_st = time.localtime(timestamp)

        self.timestamp = timestamp
        self.day = time_st.tm_mday
        self.account = Filter.Filter.get_gbid_2_account_dic()[str(self.gbid)]

    @staticmethod
    def get_log_obj_from_line(line):
        json_data = json.loads(line)
        try:
            return LogSys(json_data)
        except:
            pass

