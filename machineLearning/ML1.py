from numpy import *
#help(random)
randMat = mat(random.rand(4, 4))
print randMat
reverse = randMat.I
ret = randMat * reverse
print ret
print ret - eye(4)                                          