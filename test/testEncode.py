# mask1 = 0x00550055
# d1 = 3
# mask2 = 0x0000cccc
# d2 = 6
#  
#  
# def encodeShuffle(x):
#     t = (x ^ (x >> d1)) & mask1
#     u = x ^ t ^ (t << d1)
#     t = (u ^ (u >> d2)) & mask2
#     y = u ^ t ^ (t << d2)
#     return y
#  
#  
# def decodeShuffle(y):
#     t = (y ^ (y >> d2)) & mask2
#     u = y ^ t ^ (t << d2)
#     t = (u ^ (u >> d1)) & mask1
#     z = u ^ t ^ (t << d1)
#     return z
#  
#  
# def encodeParity(x):
#     t = (x ^ (x >> 1)) & 0x00444444
#     u = (x ^ (x << 2)) & 0x00cccccc
#     y = ((x & 0x00888888) >> 3) | (t >> 1) | u
#     return y
#  
#  
# def decodeParity(y):
#     t = ((y & 0x00111111) << 3) | (
#         ((y & 0x00111111) << 2) ^ ((y & 0x00222222) << 1))
#     z = t | ((t >> 2) ^ ((y >> 2) & 0x00333333))
#     return z
#  
#  
# def obfuscateDBID(dbid):
#     return encodeParity(encodeShuffle(dbid))
#  
#  
# def restoreDBID(dbid):
#     return decodeShuffle(decodeParity(dbid))

 
mask1 = 0x00550055
d1 = 3
mask2 = 0x0000cccc
d2 = 6
 
 
def encodeShuffle(x):
    t = (x ^ (x >> d1)) & mask1;
    u = x ^ t ^ (t << d1);
    t = (u ^ (u >> d2)) & mask2;
    y = u ^ t ^ (t << d2);
    return y
 
 
def decodeShuffle(y):
    t = (y ^ (y >> d2)) & mask2;
    u = y ^ t ^ (t << d2);
    t = (u ^ (u >> d1)) & mask1;
    z = u ^ t ^ (t << d1);
    return z
 
 
def encodeParity(x):
    t = (x ^ (x >> 1)) & 0x44444444
    u = (x ^ (x << 2)) & 0xcccccccc
    y = ((x & 0x88888888) >> 3) | (t >> 1) | u
    return y
 
 
def decodeParity(y):
    t = ((y & 0x11111111) << 3) | (((y & 0x11111111) << 2) ^ ((y & 0x22222222) << 1));
    z = t | ((t >> 2) ^ ((y >> 2) & 0x33333333));
    return z
 
 
def obfuscateDBID(dbid):
    return encodeParity(encodeShuffle(dbid))
 
def restoreDBID(dbid):
    return decodeShuffle(decodeParity(dbid))


def test16384():
    a = encodeShuffle(4194303)
    a = encodeParity(a)
    print(a)
    

def isBeyond24(x):
    #return bool(x & 0xff000000)
    return x >= 90000000


def main():
    for i in range(16777215):
        enc = obfuscateDBID(i)
        res = restoreDBID(enc)
        if i != res:
            print('not eq:', i, enc, res)
            break
        
        if isBeyond24(enc):
            print('beyond 24:', i, enc, res)
            break


if __name__ == '__main__':
    main()
