class vector(object):
    def __init__(self):
        pass
    def learn(self):
        matrix = [(1, 4), (2, 5), (5, 1), (4, 2)]
        result = [19, 26, 19, 20]
        w = [0, 0]
        loss = 10.0
        n = 0.01
        for i in xrange(100):
            if loss <= 0.001:
                break
            
            j = i % 4
            
            h = 0
            for k in xrange(2):
                h += matrix[j][k] * w[k]
            error_sum = h - result[j]
            
            for k in xrange(2):
                w[k] -= n * (error_sum) * matrix[j][k]
        