import attr


@attr.s
class ComparerBase(object):
    init_val = attr.ib(default=0)
    rate = attr.ib(default=0)
    degree = attr.ib(default=0)

    def compare(self, val):
        cmp_ret = self._compare(val)
        if cmp_ret:
            self._do_change(val)

        return cmp_ret

    def _compare(self, val):
        return False

    @classmethod
    def from_dict(cls, dic):
        return cls(dic['init_val'], dic['rate'], dic['degree'])

    def _do_change(self, val):
        self.degree += 1


@attr.s
class ComparerDown(ComparerBase):
    def _get_cur_compare_val(self):
        return self.init_val - self.rate * self.degree

    def _compare(self, val):
        return val < self._get_cur_compare_val()


@attr.s
class ComparerUp(ComparerBase):
    def _get_cur_compare_val(self):
        return self.init_val + self.rate * self.degree

    def _compare(self, val):
        return val > self._get_cur_compare_val()


@attr.s
class ComparerDouble(ComparerBase):
    up_degree = attr.ib(default=0)
    down_degree = attr.ib(default=0)

    def _compare(self, val):
        return not (self.init_val - self.rate * self.down_degree < val < self.init_val + self.rate * self.up_degree)

    def _do_change(self, val):
        if val < self.init_val - self.rate * self.down_degree:
            self.down_degree += 1
        elif val > self.init_val + self.rate * self.up_degree:
            self.up_degree += 1


def get_comp_from_dic(dic):
    if dic['cmp'] == 'down':
        return ComparerDown.from_dict(dic)
    elif dic['cmp'] == 'up':
        return ComparerUp.from_dict(dic)
    elif dic['cmp'] == 'double':
        return ComparerDouble.from_dict(dic)