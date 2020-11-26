import utils
import const

gbid1 = '8444550313351000881'
gbid2 = '8444550345026384689'

if __name__ == '__main__':
    fname = utils.filter_tlog(const.ORI_FILE_NAME, 'SecSNSGetFlow')
    print(fname)
    with open(fname) as fr:
        for line in fr:
            if gbid1 in line and gbid2 in line:
                print(line)