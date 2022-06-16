class Price:
    def __init__(self, df):
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.adj_close = None
        self.volume = None

        positions_list = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        for position, i in zip(positions_list, df.index):
            setattr(self, position, Period(df, i))


class Period:
    def __init__(self, df, df_index):
        self.df = df.loc[df_index, :]

    def period(self, year, quarter):
        quarter_dic = {1: ['03', '31'], 2: ['06', '30'], 3: ['09', '30'], 4: ['12', '31']}
        year = str(year)
        if quarter == 1:
            month = quarter_dic[1][0]
            day = quarter_dic[1][1]
        elif quarter == 2:
            month = quarter_dic[2][0]
            day = quarter_dic[2][1]
        elif quarter == 3:
            month = quarter_dic[3][0]
            day = quarter_dic[3][1]
        elif quarter == 4:
            month = quarter_dic[4][0]
            day = quarter_dic[4][1]
        ind = '{year}-{month}-{day}'.format(year=year, month=month, day=day)
        res = float(self.df.loc[ind])
        return res