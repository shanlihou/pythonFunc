import LogOne
import utils
import const
import os


def filter_item_flow_by_src(src):
    fw_name = utils.get_out_name('tmp', f'itme_flow_{src}.log')
    if os.path.exists(fw_name):
        return fw_name
    
    fname = utils.filter_from_origin(LogOne.ItemFlow.FILTER_STR)
    fw = utils.utf8_open(fw_name, 'w')
    with utils.utf8_open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            if lo.src != src:
                continue

            fw.write(line)

    fw.close()
    return fw_name


def filter_resource_flow_by_src(src):
    fw_name = utils.get_out_name('tmp', f'resource_flow_{src}.log')
    if os.path.exists(fw_name):
        return fw_name

    fname = utils.filter_from_origin(LogOne.ResourceFlow.FILTER_STR)
    fw = utils.utf8_open(fw_name, 'w')
    with utils.utf8_open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            if lo.src != src:
                continue

            fw.write(line)

    fw.close()
    return fw_name


def get_login_out_log_new():
    fw_name = utils.get_out_name('tmp', 'log_and_out_new.log')
    if os.path.exists(fw_name):
        return fw_name

    fw = utils.utf8_open(fw_name, 'w')
    for line in utils.get_origin_line_stream():
        lo = LogOne.get_log_from_line(line)
        if not lo:
            continue

        if lo.FILTER_STR == 'PlayerLogin' or lo.FILTER_STR == 'PlayerLogout':
            fw.write(line)

    fw.close()
    return fw_name


def filter_by_log_one_all():
    fw_name = utils.get_out_name('tmp', 'log_one.log')
    if os.path.exists(fw_name):
        return fw_name

    fw = utils.utf8_open(fw_name, 'w')
    for line in utils.get_origin_line_stream():
        lo = LogOne.get_log_from_line(line)
        if not lo:
            continue

        fw.write(line)

    fw.close()
    return fw_name
