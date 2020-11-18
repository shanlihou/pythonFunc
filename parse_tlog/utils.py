import time
import os


def get_time_stamp(time_str):
    time_st = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return time.mktime(time_st)


def get_day(time_str):
    time_st = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return time_st.tm_mday


def get_out_name(filename, dir_name, out_name):
    dirname = os.path.dirname(filename)
    newdir = os.path.join(dirname, dir_name)
    fw_name = os.path.join(newdir, out_name)

    try:
        os.mkdir(newdir)
    except Exception as e:
        pass

    return fw_name
