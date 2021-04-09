import LogOne
import utils
import const
import os


def filter_item_flow_by_src(src):
    fw_name = utils.get_out_name('tmp', f'itme_flow_{src}.log')
    if os.path.exists(fw_name):
        return fw_name
    
    fname = utils.filter_tlog(const.ORI_FILE_NAME, LogOne.ItemFlow.FILTER_STR)
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
    
    fname = utils.filter_tlog(const.ORI_FILE_NAME, LogOne.ResourceFlow.FILTER_STR)
    fw = utils.utf8_open(fw_name, 'w')
    with utils.utf8_open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            if lo.src != src:
                continue

            fw.write(line)

    fw.close()
    return fw_name