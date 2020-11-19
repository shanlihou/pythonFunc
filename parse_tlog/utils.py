import time
import os
import const


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
