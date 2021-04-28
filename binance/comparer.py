import attr


@attr.s
class ComparerBase(object):
    def compare(self, val):
        cmp_ret = self._compare(val)
        if cmp_ret:
            self._do_change()

        return cmp_ret

    def _compare(self, val):
        return False


    def _do_change(self):
        pass

    @classmethod
    def from_dict(cls, dic):
        return cls(dic['init_val'], dic['rate'], dic['degree'])

    def _do_change(self):
        self.degree += 1


@attr.s
class ComparerDown(ComparerBase):
    init_val = attr.ib(default=0)
    rate = attr.ib(default=0)
    degree = attr.ib(default=0)

    def _get_cur_compare_val(self):
        return self.init_val - self.rate * self.degree

    def _compare(self, val):
        return val < self._get_cur_compare_val()


@attr.s
class ComparerUp(ComparerBase):
    init_val = attr.ib(default=0)
    rate = attr.ib(default=0)
    degree = attr.ib(default=0)

    def _get_cur_compare_val(self):
        return self.init_val + self.rate * self.degree

    def _compare(self, val):
        return val > self._get_cur_compare_val()


def get_comp_from_dic(dic):
    if dic['cmp'] == 'down':
        return ComparerDown.from_dict(dic)
    elif dic['cmp'] == 'up':
        return ComparerUp.from_dict(dic)