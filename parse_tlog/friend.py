import utils
import const

gbid1 = '8444836520213977514'
gbid2 = '8444836521690372514'

if __name__ == '__main__':
    fname = utils.filter_from_origin('SecSNSGetFlow')
    print(fname)
    with utils.utf8_open(fname) as fr:
        for line in fr:
            if gbid1 in line and gbid2 in line:
                print(line)