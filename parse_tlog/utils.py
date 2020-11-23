import time
import os
import const
import sys
import functools
import pickle
import math
import LogOne


def get_openid_info(filename):
    openid_set = set()
    with open(filename, encoding='utf-8') as fr:
        for line in fr:
            if ' ' in line:
                tup = line.strip().split(' ')
            else:
                tup = line.strip().split('\t')

#                 print(tup)
            if len(tup) > 2:
                openid_set.add(tup[2])

    return openid_set


@functools.lru_cache(1)
def get_out_first_account_set():
    return get_openid_info(const.OUT_FILTER_NAME)


def get_time_stamp(time_str):
    time_st = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return time.mktime(time_st)


def get_day(time_str):
    time_st = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return time_st.tm_mday


def get_dir(dir_name):
    new_dir = '{}\\{}'.format(const.ROOT_NAME, dir_name)
    try:
        os.mkdir(new_dir)
    except Exception as e:
        pass

    return new_dir


def get_out_name(dir_name, out_name):
    new_dir = get_dir(dir_name)
    fw_name = os.path.join(new_dir, out_name)

    return fw_name


def filter_tlog(filename, filter_str):
    basename = os.path.basename(filename)
    dirname = get_dir('tmp')
    fw_name = os.path.join(dirname, '{}.{}.log'.format(basename, filter_str))
    if os.path.exists(fw_name):
        return fw_name

    fw = open(fw_name, 'w')
    with open(filename, encoding='utf-8') as fr:
        for line in fr:
            if not line.startswith(filter_str):
                continue

            tup = line.strip().split('|')
            time_str = tup[2]
            day = get_day(time_str)
            if day < 12:
                continue

            fw.write(line)

    fw.close()
    return fw_name


@functools.lru_cache(1)
def get_gbid_2_account_dic():
    import LogOne
    tmp_dir = get_dir('tmp')
    save_path = os.path.join(tmp_dir, 'gbid_2_account')
    if os.path.exists(save_path):
        return pickle.load(open(save_path, 'rb'))

    ret_dic = {}

    sec_name = filter_tlog(const.ORI_FILE_NAME, 'SecLogin')
    with open(sec_name) as fr:
        for line in fr:
            lo = LogOne.LogOne.get_log_obj_from_line(line)
            ret_dic[lo.gbid] = lo.account

    pickle.dump(ret_dic, open(save_path, 'wb'))

    return ret_dic


@functools.lru_cache(1)
def get_out_first_day_score_dict():
    tmp_dir = get_dir('tmp')
    save_path = os.path.join(tmp_dir, 'out_first_day_score_dict')
    if os.path.exists(save_path):
        return pickle.load(open(save_path, 'rb'))

    dirname = os.path.dirname(const.DAY_SCORE)
    sys.path.append(dirname)
    basename = os.path.basename(const.DAY_SCORE)
    day_score_dict = __import__(basename.split('.')[0]).a

    score_dict = {}
    for k, avatar2score in day_score_dict.items():
        day = int(k.split('-')[-1])
        day_dict = {}
        for gbid, score in avatar2score.items():
            account = get_gbid_2_account_dic()[gbid]
            if account not in get_out_first_account_set():
                continue

            if gbid in day_dict:
                if score > day_dict[gbid]:
                    day_dict[gbid] = score
            else:
                day_dict[gbid] = score

        day_list = list(day_dict.items())
        day_list.sort(key=lambda x: x[1], reverse=True)
        size = math.ceil(len(day_list) * 0.75)
        day_set = set()
        for i in range(size):
            day_set.add(day_list[i][0])

        score_dict[day] = day_set


    pickle.dump(score_dict, open(save_path, 'wb'))
    return score_dict


@functools.lru_cache(1)
def get_delta2score_dict():
    import sys
    sys.path.append(const.DATA_FOLDER)
    datas = __import__(const.GUILD_TRAIN_TABLE).datas
    ret_dict = {}
    for index, data in datas.items():
        delta = data['upgradeContributionCost']
        if index == 1:
            score = data['score']
        else:
            score = data['score'] - datas[index - 1]['score']

        ret_dict[delta] = score

    return ret_dict


@functools.lru_cache(1)
def get_gbid_school_dict():
    tmp_dir = get_dir('tmp')
    save_path = os.path.join(tmp_dir, 'gbid_2_school_dict')
    if os.path.exists(save_path):
        return pickle.load(open(save_path, 'rb'))


    fname = filter_tlog(const.ORI_FILE_NAME, 'LOG_LEVEL')
    ret_dict = {}
    with open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            ret_dict[lo.gbid] = lo.school

    pickle.dump(ret_dict, open(save_path, 'wb'))

    return ret_dict
