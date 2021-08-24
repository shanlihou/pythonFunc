import utils
import const
import Filter
import json
import time
import math
import re
import functools


LOG_DIC = {}


def log_wrapper(cls):
    if cls.FILTER_STR:
        LOG_DIC[cls.FILTER_STR] = cls
    return cls


class LogOneBase(object):
    FILTER_STR = None

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

    @classmethod
    def get_log_obj_from_line(cls, line):
        tup = line.strip().split('|')
        try:
            return cls(*tup)
        except Exception as e:
            print(cls, e)
            return None


@log_wrapper
class LogOne(LogOneBase):
    FILTER_STR = 'SecLogin'
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
        self.max_level = int(self.level)


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


@log_wrapper
class LogVitality(LogOneBase):
    FILTER_STR = 'LOG_VITALITY'

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


@log_wrapper
class LogOut(LogOneBase):
    FILTER_STR = 'SecLogout'
    IS_LOGIN = False

    def __init__(self, log_type, server_id, time_str, app_id, plant_id,
                 area_id, zone_id, open_id, client_ver, sec_report_data,
                 sys_software, *args):
        gbid = args[6]
        level = args[9]
        super().__init__(time_str, open_id, gbid)
        self.level = level
        self.app_id = app_id
        self.battle_point = args[10]

    @staticmethod
    def get_log_obj_from_line(line):
        tup = line.strip().split('|')
        try:
            return LogOut(*tup)
        except:
            return None
        
    def __str__(self):
        return f'LogOut gbid:{self.gbid}'


@log_wrapper
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


@log_wrapper
class LogLevel(LogOneBase):
    FILTER_STR = 'LOG_LEVEL'

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


@log_wrapper
class LogGuildContrib(LogOneBase):
    FILTER_STR = 'LOG_GUILD_CONTRIBUTION'

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


@log_wrapper
class RoundFlow(LogOneBase):
    FILTER_STR = 'RoundFlow'

    def __init__(self, log_type, server_id, time_str, app_id, plant_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, ibattle_type, battle_id, round_time, result, rank, *args):
        super().__init__(time_str, open_id, role_id)
        self.battle_type = ibattle_type
        self.round_time = round_time
        self.result = result


@log_wrapper
class LogGuildTrain(LogOneBase):
    FILTER_STR = 'GuildTrainFlow'

    def __init__(self, log_type, server_id, time_str, app_id, plant_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, train_level, train_id, score):
        super().__init__(time_str, open_id, role_id)
        self.train_id = train_id
        self.level = train_level
        self.score = score


@log_wrapper
class PlayerLogOut(LogOneBase):
    FILTER_STR = 'PlayerLogout'

    def __init__(self, log_type, server_id, time_str, app_id, plant_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, *args):
        super().__init__(time_str, open_id, role_id)
        self.level = level
        self.battle_point = irole_ce
        self.login_channel = args[10]


@log_wrapper
class PlayerLogin(LogOneBase):
    FILTER_STR = 'PlayerLogin'

    def __init__(self, log_type, server_id, time_str, app_id, plant_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, *args):
        super().__init__(time_str, open_id, role_id)
        self.level = level
        self.battle_point = irole_ce
        self.login_channel = args[9]


@log_wrapper
class GuideFlowLog(LogOneBase):
    FILTER_STR = 'GuideFlow'

    def __init__(self, log_type, server_id, time_str, app_id, plant_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, guide_id, is_can_skip):
        super().__init__(time_str, open_id, role_id)
        self.guide_id = guide_id
        

@log_wrapper
class ItemFlow(LogOneBase):
    FILTER_STR = 'ItemFlow'

    def __init__(self, log_type, server_id, time_str, app_id, plant_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, *args):
        super().__init__(time_str, open_id, role_id)
        self.item_id = args[3]
        self.src = int(args[7])
        self.detail = args[9]


@log_wrapper
class ResourceFlow(LogOneBase):
    FILTER_STR = 'ResourceFlow'

    def __init__(self, log_type, server_id, time_str, app_id, plant_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, *args):
        super().__init__(time_str, open_id, role_id)
        self.resource_id = int(args[1])
        self.count = int(args[3])
        self.src = int(args[4])


@log_wrapper
class GuildFlow(LogOneBase):
    FILTER_STR = 'GuildFlow'

    def __init__(self, log_type, server_id, time_str, app_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, act_type, guild_uuid, guild_name, guild_level, member_num, member_num_max=0):
        super().__init__(time_str, open_id, role_id)
        self.name = role_name
        self.act_type = act_type
        self.guild_uuid = guild_uuid
        self.guild_name = guild_name
        self.guild_level = guild_level
        self.member_num = member_num
        self.member_num_max = member_num_max


@log_wrapper
class LingxuAttackFlow(LogOneBase):
    FILTER_STR = 'LingxuAttackFlow'

    def __init__(self, log_type, server_id, time_str, app_id, plat_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce, lingxu_type, completion, occupy):
        super().__init__(time_str, open_id, role_id)
        self.name = role_name
        self.lingxu_type = lingxu_type
        self.completion = completion
        self.occupy = occupy


@log_wrapper
class PlayerFriendsList(LogOneBase):
    FILTER_STR = 'PlayerFriendsList'

    def __init__(self, log_type, server_id, time_str, app_id, plat_id, zone_id, open_id, role_id, role_name, level, vip_level, irole_ce,
            school, nickName, headId, headUrl, seq, friendZoneId, fOpenId, fRoleId, fRoleName, fSchool, fNickName, fHeadId, fHeadUrl, friendType):
        super().__init__(time_str, open_id, role_id)
        self.name = role_name
        self.friend_gbid = fRoleId
        self.friend_name = fRoleName


@functools.lru_cache(1)
def get_pat():
    pat_str = '|'.join(LOG_DIC.keys())
    pat_str = f'^({pat_str})\\|'
    return re.compile(pat_str)


def get_log_from_line(line):
    find = get_pat().search(line)
    if find:
        return LOG_DIC[find.group(1)].get_log_obj_from_line(line)
    elif line.startswith(' '):
        return LogSys.get_log_obj_from_line(line)
    else:
        return None

if __name__ == '__main__':
    pat = get_pat()
    find = pat.search('ItemFlow|')
    print(find)