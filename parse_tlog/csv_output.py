class CSVOutPut(object):
    def __init__(self):
        self.table = []

    def set(self, x, y, value):
        while x >= len(self.table):
            self.table.append([])

        row = self.table[x]
        while y >= len(row):
            row.append('')

        row[y] = value

    def get(self, x, y):
        if x >= len(self.table):
            return ''

        row = self.table[x]
        if y >= len(row):
            return ''

        return row[y]

    def get_width(self):
        return max([len(i) for i in self.table])

    def get_height(self):
        return len(self.table)

    def output(self, filename):
        width = self.get_width()
        height = self.get_height()
        with open(filename, 'w') as fw:
            for i in range(height):
                out_str = ','.join([self.get(i, j) for j in range(width)])
                fw.write(out_str + '\n')

