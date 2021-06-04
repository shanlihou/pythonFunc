import attr
MAX = 10000
MULTI = 3

@attr.s
class CalcRet(object):
    sum = attr.ib()
    quantity = attr.ib()
    avg_rice = attr.ib()
    rice_list = attr.ib()
    quantity_list = attr.ib()
    cur_quantity_list = attr.ib()


def calc(start, count, rate, qty, isLog=False):
    down_count = 0
    sum = 0
    rice_list = []
    quantity_list = []
    cur_quantitiy_list = []
    for i in range(count):
        if isLog:
            print(f'cur:{start}, multi:{qty}')

        rice_list.append(start)
        quantity_list.append(qty)
        sum += start * qty
        down_count += qty
        cur_quantitiy_list.append(down_count)

        qty *= MULTI
        start += rate
        if isLog:
            print(f'\tafter down_count:{down_count}')

    return CalcRet(
        sum,
        down_count,
        sum / down_count,
        rice_list,
        quantity_list,
        cur_quantitiy_list,
    )


def get_open_qty(level, max_quantity):
    l = 0
    r = MAX

    while (l <= r):
        mid = (l + r) // 2
        val = calc(1, level, 1, max_quantity / MAX * mid)['quantity']
        # print(f'l:{l}, r:{r}, mid:{mid}, rate:{rate}')
        if val <= max_quantity:
            l = mid + 1
        else:
            r = mid - 1

    return max_quantity / MAX * mid


def get_diff(level, start, target):
    l = 0
    r = MAX
    duration = target - start
    while l <= r:
        mid = (l + r) // 2
        val = duration / MAX * mid
        ret = calc(start, level, val, 1)
        if ret['avg_rice'] < target:
            l = mid + 1
        else:
            r = mid - 1

    return duration / MAX * l


def calc_by_final_rice(start, count, final_price, quantity):
    """
    根据最终价格统计
    """
    diff = (final_price - start) / (count - 1)
    return calc(start, count, diff, quantity)


def cacl_by_avg_rice_max(start, level, target, max_quantity):
    """
    根据平均价格及最大数量来计算
    """
    diff = get_diff(level, start, target)
    quantity = get_open_qty(level, max_quantity)
    return calc(start, level, diff, quantity)


def cacl_by_avg_rice(start, level, target, quantity):
    """
    根据最终平均价格来计算
    """
    diff = get_diff(level, start, target)
    return calc(start, level, diff, quantity)


def main():
    # ret = cacl_by_avg_rice_max(19, 3, 1.6, 59)
    # for k, v in ret.items():
    #     print(k, v)

    ret = calc(2557, 3, 100, 0.008)
    print(ret)

    curQuantity = 0.04
    cur_rice = 2556
    rice = 2671
    quantity = 0.2
    print((cur_rice * curQuantity + rice * quantity) / (curQuantity + quantity))

    val = 0.08 * 3627 + 150 * 0.454 + 50 * 1.958 + 78
    print(val)

if __name__ == '__main__':
    main()