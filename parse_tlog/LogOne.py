import utils
import const
import Filter
import json
import time
import math


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
    IS_LOGIN = True
    def __init__(self, log_type, server_id, time_str, app_id, plant_id,
                 area_id, zone_id, open_id, client_ver, sec_report_data,
                 sys_software, *args):
        super().__init__(time_str, open_id, args[6])
        self.name = args[7]
        self.end_time = 0
        self.day_set = set()
        self.day_set.add(self.day)
        # self.school = utils.get_gbid_school_dict().get(self.gbid)
        self.school = args[8]
        self.level = args[9]
        self.login_info = [{
            'timestamp': self.timestamp,
            'is_login': True,
        }]

    def is_stay_by_dur(self, day_count):
        first_day = min(self.day_set)
        for i in range(1, day_count + 1):
            day = first_day + i
            if day not in self.day_set:
                # if len(self.day_set) > 1:
                #     print(self.day_set, day, first_day)
                return False

        return True

    def add_day(self, day, is_login, timestamp):
        self.day_set.add(day)
        last_info = self.login_info[-1]
        if last_info['is_login'] and not is_login:
            last_st = time.localtime(last_info['timestamp'])
            cur_st = time.localtime(timestamp)
            for i in range(last_st.tm_mday, cur_st.tm_mday + 1):
                self.day_set.add(i)

        self.login_info.append({
            'timestamp': timestamp,
            'is_login': is_login
        })

    def add_log_out_time(self, timestamp):
        if self.end_time:
            return

        self.end_time = timestamp

    def get_duration(self):
        return int((self.end_time - self.timestamp) // 60)

    @staticmethod
    def get_log_obj_from_line(line):
        tup = line.strip().split('|')
        return LogOne(*tup)


class LogVitality(LogOneBase):
    def __init__(self, log_type, server_id, time_str, _1, gbid, _2, _3, uuid, _4, activity):
        account = utils.get_gbid_2_account_dic()[gbid]
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
    IS_LOGIN = False
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
        self.account = utils.get_gbid_2_account_dic()[str(self.gbid)]

    @staticmethod
    def get_log_obj_from_line(line):
        json_data = json.loads(line)
        try:
            return LogSys(json_data)
        except:
            pass


class LogLevel(LogOneBase):
    def __init__(self, log_type, server_id, time_str, _1, gbid, school, *args):
        account = utils.get_gbid_2_account_dic()[gbid]
        super().__init__(time_str, account, gbid)
        self.school = school

    @staticmethod
    def get_log_obj_from_line(line):
        tup = line.strip().split('|')
        try:
            return LogLevel(*tup)
        except Exception as e:
            return None


class LogGuildContrib(LogOneBase):
    def __init__(self, log_type, server_id, time_str, _1, gbid, num, delta, uuid, src, desc):
        account = utils.get_gbid_2_account_dic()[gbid]
        super().__init__(time_str, account, gbid)
        self.delta = abs(int(delta))
        self.score = utils.get_delta2score_dict()[self.delta]

    @staticmethod
    def get_log_obj_from_line(line):
        tup = line.strip().split('|')
        try:
            return LogGuildContrib(*tup)
        except Exception as e:
            return None

class RoundFlow(LogOneBase):
    def __init__(self, log_type, server_id, time_str, app_id, plant_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, ibattle_type, battle_id, round_time, result, rank, *args):
        super().__init__(time_str, open_id, role_id)
        self.battle_type = ibattle_type
        self.round_time = round_time
        self.result = result

    @staticmethod
    def get_log_obj_from_line(line):
        tup = line.strip().split('|')
        try:
            return RoundFlow(*tup)
        except Exception as e:
            print(e)
            return None


class LogGuildTrain(LogOneBase):
    def __init__(self, log_type, _1, time_str, _2, gbid, train_id, level, score):
        account = utils.get_gbid_2_account_dic()[gbid]
        super().__init__(time_str, account, gbid)
        self.train_id = train_id
        self.level = level
        self.score = score

    @staticmethod
    def get_log_obj_from_line(line):
        tup = line.strip().split('|')
        try:
            return LogGuildTrain(*tup)
        except Exception as e:
            print(e)
            return None


def get_log_from_line(line):
    if line.startswith('SecLogin'):
        return LogOne.get_log_obj_from_line(line)
    elif line.startswith('SecLogout'):
        return LogOut.get_log_obj_from_line(line)
    elif line.startswith('LOG_VITALITY'):
        return LogVitality.get_log_obj_from_line(line)
    elif line.startswith('LOG_GUILD_CONTRIBUTION'):
        return LogGuildContrib.get_log_obj_from_line(line)
    elif line.startswith('LOG_LEVEL'):
        return LogLevel.get_log_obj_from_line(line)
    elif line.startswith('RoundFlow'):
        return RoundFlow.get_log_obj_from_line(line)
    elif line.startswith('LOG_GUILD_TRAIN'):
        return LogGuildTrain.get_log_obj_from_line(line)
    elif line.startswith(' '):
        return LogSys.get_log_obj_from_line(line)
    else:
        return None

