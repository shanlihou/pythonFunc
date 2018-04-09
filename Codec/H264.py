import math
class bitstream:
    def __init__(self, data):
        self.bitItr = self.__bitstream(data)
        self.dataLen = len(data)
    def __bitstream(self, data):
        self.offset = 0
        for hex in data:
            for i in range(7, -1, -1):
                yield (hex >> i) & 0x01
            self.offset += 1
        yield None
    def getBit(self, count):
        ret = 0
        for i in xrange(count):
            bit = self.bitItr.next()
            if bit == None:
                return None
            ret = (ret << 1) + bit
        return ret
    def getLeft(self):
        return self.dataLen - self.offset
    def golomb_parse(self):
        mLen = 0
        while not self.getBit(1):
            mLen += 1
        return int(math.pow(2, mLen)) - 1 + self.getBit(mLen)
class DECODE(object):
    def __init__(self, bs):
        self.bs = bs
        self.printList = []
    def addAttr(self, name, value):
        self.printList.append(name)
        setattr(self, name, value)
    def __str__(self):
        return '\n'.join(map(lambda x:'%s:%s' % (x, str(getattr(self, x))) ,self.printList))
    
class SPS(DECODE):    
    def __init__(self, bs):
        super(SPS, self).__init__(bs)
        
        self.addAttr('idc', self.bs.getBit(8))
        self.addAttr('constraint_set_flags', self.bs.getBit(6))
        self.bs.getBit(2)
        self.addAttr('level_idc', self.bs.getBit(8))
        self.addAttr('sps_id', self.bs.golomb_parse())
        self.addAttr('chroma_format_idc', self.bs.golomb_parse())
        self.addAttr('bit_depth_luma', self.bs.golomb_parse() + 8)
        self.addAttr('bit_depth_chroma', self.bs.golomb_parse() + 8)
        self.addAttr('transform_bypass', self.bs.getBit(1))
        self.addAttr('is_scaling_matrix', self.bs.getBit(1))
        self.addAttr('log2_max_frame_num', self.bs.golomb_parse() + 4)
        self.addAttr('poc_type', self.bs.golomb_parse())
        self.addAttr('log2_max_poc_lsb', self.bs.golomb_parse() + 4)
        self.addAttr('ref_frame_count', self.bs.golomb_parse())
        self.addAttr('gaps_in_frame_num_allowed_flag', self.bs.getBit(1))
        self.addAttr('mb_width', self.bs.golomb_parse() + 1)
        self.addAttr('mb_height', self.bs.golomb_parse() + 1)
        self.addAttr('frame_mbs_only_flag', self.bs.getBit(1))
        self.mb_height *= 2 - self.frame_mbs_only_flag
        self.addAttr('direct_8x8_inference_flag', self.bs.getBit(1))
        self.addAttr('crop', self.bs.getBit(1))
        self.addAttr('crop_left', self.bs.golomb_parse())
        self.addAttr('crop_right', self.bs.golomb_parse())
        self.addAttr('crop_top', self.bs.golomb_parse())
        self.addAttr('crop_bottom', self.bs.golomb_parse())
        self.addAttr('vui_parameters_present_flag', self.bs.golomb_parse())
        print 'left:', self.bs.getLeft()
class PPS(DECODE):
    def __init__(self, bs, spsList):
        super(PPS, self).__init__(bs)
        self.addAttr('pps_id', self.bs.golomb_parse())
        self.addAttr('sps_id', self.bs.golomb_parse())
        self.sps = spsList[self.sps_id]
        self.addAttr('cabac', self.bs.getBit(1))
        self.addAttr('pic_order_present', self.bs.getBit(1))
        self.addAttr('slice_group_count', self.bs.golomb_parse() + 1)
        self.addAttr('ref_count_0', self.bs.golomb_parse() + 1)
        self.addAttr('ref_count_1', self.bs.golomb_parse() + 1)
        qp_bd_offset = 6 * (self.sps.bit_depth_luma - 8)
        self.addAttr('weighted_pred', self.bs.getBit(1))
        self.addAttr('weighted_bipred_idc', self.bs.getBit(2))
        self.addAttr('init_qp', self.bs.golomb_parse() + 26 + qp_bd_offset)
        self.addAttr('init_qs', self.bs.golomb_parse() + 26 + qp_bd_offset)
        
        self.chroma_qp_index_offset = []
        self.chroma_qp_index_offset.append(self.bs.golomb_parse())
        self.printList.append('chroma_qp_index_offset')
        
        self.addAttr('deblocking_filter_parameters_present', self.bs.getBit(1))
        self.addAttr('constrained_intra_pred', self.bs.getBit(1))
        self.addAttr('redundant_pic_cnt_present', self.bs.getBit(1))
        print 'left:', self.bs.getLeft()
class H264:
    def __init__(self, filename):
        self.name = filename
        self.fileRead = open(filename, 'rb')
        self.typeList = ['not use', 'SLICE', 'DPA', 'DPB', 'DPC', 'IDR', 'SEI', 'SPS',
                     'PPS', 'AUD', 'EOSEQ', 'EOSTREAM', 'FILL']
        self.spsList = []
        self.ppsList = []
    def readBit(self):
        tmp = self.fileRead.read(1)
        while tmp:
            code = ord(tmp)
            if code == 0:
                codeList = [0]
                while not code:
                    code = ord(self.fileRead.read(1))
                    codeList.append(code)
                codeLen = len(codeList) 
                if codeLen < 3:
                    for i in codeList:
                        yield i
                elif codeLen == 3:
                    if codeList[2] == 3:
                        yield 0
                        yield 0
                    elif codeList[2] == 1:
                        yield 's2'
                    else:
                        for i in codeList:
                            yield i
                elif codeLen == 4:
                    if codeList[3] == 1:
                        yield 's3'
                    else:
                        print("not find code:", codeList)
                        break
                else:
                    print "not find code:", codeList
                    break
            else:
                yield code
            tmp = self.fileRead.read(1)
        yield None
    def iterNalU(self):
        NalU = []
        for i in self.readBit():
            if isinstance(i, int):
                #print '%x' % i
                NalU.append(i)
            elif i == 's3':
                if NalU:
                    yield NalU
                NalU = []
            elif i == 's2':
                if NalU:
                    yield NalU
                NalU = []
                
            else:
                print 'not find i:', i
                break
        yield None
    def SPS(self):
        sps = SPS(self.bs)
        print sps
        self.spsList.append(sps)
    def PPS(self):
        pps = PPS(self.bs, self.spsList)
        print pps
        self.ppsList.append(pps)
    def SEI(self):
        print self.bs.getLeft()
    def IDR(self):
        print self.bs.getLeft()
        
    def parseNalu(self, nalu):
        self.bs = bitstream(nalu)
        self.forbid = self.bs.getBit(1)
        self.ref = self.bs.getBit(2)
        self.type = self.bs.getBit(5)
        
        #print self.type
        print 'type:', self.typeList[self.type]
        if hasattr(self, self.typeList[self.type]):
            getattr(self, self.typeList[self.type])()
    def parse(self):
        nalus = self.iterNalU()
        count = 0
        for i in nalus:
            self.parseNalu(i)
            count += 1
            if count == 5:
                break
if __name__ == '__main__':
    h264 = H264(r'D:\eclipse\live555-master\live555-master\mediaServer\mediaServer\test.264')
    h264.parse()