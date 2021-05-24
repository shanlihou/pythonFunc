
MAX = 10000

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

        qty *= 3
        start += rate
        if isLog:
            print(f'\tafter down_count:{down_count}')

    return {
        'sum': sum,
        'quantity': down_count,
        'avg_rice': sum / down_count,
        'rice_list': rice_list,
        'quantity_list': quantity_list,
        'cur_quantity_list': cur_quantitiy_list,
    }


def get_open_rice(level, max_quantity):
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


def calc_by_final_rice(start, count, diff, final, rate):
    quality = get_open_rice(count, final)



    ret = calc(start, count, diff, quality)
    return ret


def cacl_by_avg_rice(start, level, target, max_quantity):
    diff = get_diff(level, start, target)
    quantity = get_open_rice(level, max_quantity)

    return calc(start, level, diff, quantity)

def main():
    ret = cacl_by_avg_rice(0.95, 3, 1.6, 59)
    for k, v in ret.items():
        print(k, v)

    curQuantity = 0.012
    cur = 2143 * curQuantity
    rice = 2375
    quantity = 0.027
    print((cur + rice * quantity) / (curQuantity + quantity))


if __name__ == '__main__':
    main()