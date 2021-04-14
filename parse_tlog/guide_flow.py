# coding:utf-8
import utils
import const
import LogOne
import csv_output


def guide_flow():
    fname = utils.filter_from_origin('GuideFlow')
    id_dic = {}
    avatar_count = utils.get_avatar_count()
    with utils.utf8_open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            if not lo:
                continue
            
            id_dic.setdefault(lo.guide_id, set())
            id_dic[lo.guide_id].add(lo.gbid)
    
    rets = [(int(k), len(v)) for k, v in id_dic.items()]
    rets.sort(key=lambda x: x[0])
    csv = csv_output.CSVOutPut()
    csv.set(0, 0, '节点')
    csv.set(0, 1, '创角数')
    csv.set(0, 2, '节点通过人数')
    csv.set(0, 3, '节点通过率')
    idx = 1
    for key, num in rets:
        csv.set(idx, 0, key)
        csv.set(idx, 1, avatar_count)
        csv.set(idx, 2, num)
        csv.set(idx, 3, num / avatar_count)
        idx += 1
        
    out_name = utils.get_out_name('out', 'guide_flow.csv')
    csv.output(out_name)

if __name__ == '__main__':
    guide_flow()