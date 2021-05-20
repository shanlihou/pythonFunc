
def calc(start, count, rate, multi, isLog=False):
    down_count = 0
    sum = 0
    rice_list = []
    quantity_list = []
    cur_quantitiy_list = []
    for i in range(count):
        if isLog:
            print(f'cur:{start}, multi:{multi}')

        rice_list.append(start)
        quantity_list.append(multi)
        sum += start * multi
        down_count += multi
        cur_quantitiy_list.append(down_count)

        multi *= 3
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


def get_open_rice(level, target, rate):
    l = 0
    r = target // rate
    while (l <= r):
        mid = (l + r) // 2
        val = calc(1, level, 1, mid * rate)['quantity']
        # print(f'l:{l}, r:{r}, mid:{mid}, rate:{rate}')
        if val <= target:
            l = mid + 1
        else:
            r = mid - 1

    return r * rate


def calc_by_final_rice(start, count, diff, final, rate):
    quality = get_open_rice(count, final, rate)

    ret = calc(start, count, diff, quality)
    return ret


def main():
    ret = calc_by_final_rice(2800, 5, 100, 0.1, 0.0001)
    for k, v in ret.items():
        print(k, v)

if __name__ == '__main__':
    main()