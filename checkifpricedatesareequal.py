import datetime


def check_if_price_dates_are_equal(close_price_in_sector_dict):
    def shorten_l(f_l):
        nl = []
        for x in f_l:
            x = datetime.datetime.strptime(str(x), '%Y-%m-%d').date()
            if md <= x <= mxd:
                nl.append(x)
        return nl

    my_l = []
    attempt = 0
    md = datetime.date(year=2018, month=1, day=1)
    mxd = datetime.date(year=2021, month=12, day=31)
    for sec in close_price_in_sector_dict.keys():
        sector_dict = close_price_in_sector_dict[sec]
        for comp in sector_dict.keys():
            print(comp)
            attempt += 1
            tmp_l = sector_dict[comp].loc[:, 'Date']
            tmp_l = shorten_l(tmp_l)
            if attempt == 1:
                my_l = shorten_l(tmp_l)
            if attempt > 1:
                for x, y in zip(my_l, tmp_l):
                    if x != y:
                        print('not equal: ', x, y)
