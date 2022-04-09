class Balance():
    def __init__(self, df):
        def index_number():
            nonlocal ind_num
            ind_num += 1
            return ind_num

        self.CashAndEquivalents = None
        self.ShortTermInvestments = None
        self.AccountsReceivableNet = None
        self.Inventory = None
        self.PrepaidExpenses = None
        self.OtherCurrentAssets = None
        self.TotalCurrentAssets = None
        self.PropertyPlantAndEquipmentNet = None
        self.RealEstateOwned = None
        self.CapitalizedPurchasedSoftware = None
        self.LongtermInvestments = None
        self.Goodwill = None
        self.OtherIntangibles = None
        self.OtherLongtermAssets = None
        self.TotalAssets = None
        self.AccountsPayable = None
        self.AccruedExpenses = None
        self.ShorttermBorrowings = None
        self.CurrentPortionofLTDebt = None
        self.CurrentPortionofCapitalLeaseObligations = None
        self.OtherCurrentLiabilities = None
        self.TotalCurrentLiabilities = None
        self.LongtermDebt = None
        self.CapitalLeases = None
        self.OtherNoncurrentLiabilities = None
        self.TotalLiabilities = None
        self.CommonStock = None
        self.AdditionalPaidInCapital = None
        self.RetainedEarnings = None
        self.TreasuryStock = None
        self.OtherCommonEquityAdj = None
        self.CommonEquity = None
        self.TotalPreferredEquity = None
        self.MinorityInterestTotal = None
        self.OtherEquity = None
        self.TotalEquity = None
        self.TotalLiabilitiesAndEquity = None
        self.CashAndShortTermInvestments = None
        self.TotalDebt = None

        ind_num = 0
        setattr(self, 'CashAndEquivalents', Period(df, ind_num))
        setattr(self, 'ShortTermInvestments', Period(df, index_number()))
        setattr(self, 'AccountsReceivableNet', Period(df, index_number()))
        setattr(self, 'Inventory', Period(df, index_number()))
        setattr(self, 'PrepaidExpenses', Period(df, index_number()))
        setattr(self, 'OtherCurrentAssets', Period(df, index_number()))
        setattr(self, 'TotalCurrentAssets', Period(df, index_number()))
        setattr(self, 'PropertyPlantAndEquipmentNet', Period(df, index_number()))
        setattr(self, 'RealEstateOwned', Period(df, index_number()))
        setattr(self, 'CapitalizedPurchasedSoftware', Period(df, index_number()))
        setattr(self, 'LongtermInvestments', Period(df, index_number()))
        setattr(self, 'Goodwill', Period(df, index_number()))
        setattr(self, 'OtherIntangibles', Period(df, index_number()))
        setattr(self, 'OtherLongtermAssets', Period(df, index_number()))
        setattr(self, 'TotalAssets', Period(df, index_number()))
        setattr(self, 'AccountsPayable', Period(df, index_number()))
        setattr(self, 'AccruedExpenses', Period(df, index_number()))
        setattr(self, 'ShorttermBorrowings', Period(df, index_number()))
        setattr(self, 'CurrentPortionofLTDebt', Period(df, index_number()))
        setattr(self, 'CurrentPortionofCapitalLeaseObligations', Period(df, index_number()))
        setattr(self, 'OtherCurrentLiabilities', Period(df, index_number()))
        setattr(self, 'TotalCurrentLiabilities', Period(df, index_number()))
        setattr(self, 'LongtermDebt', Period(df, index_number()))
        setattr(self, 'CapitalLeases', Period(df, index_number()))
        setattr(self, 'OtherNoncurrentLiabilities', Period(df, index_number()))
        setattr(self, 'TotalLiabilities', Period(df, index_number()))
        setattr(self, 'CommonStock', Period(df, index_number()))
        setattr(self, 'AdditionalPaidInCapital', Period(df, index_number()))
        setattr(self, 'RetainedEarnings', Period(df, index_number()))
        setattr(self, 'TreasuryStock', Period(df, index_number()))
        setattr(self, 'OtherCommonEquityAdj', Period(df, index_number()))
        setattr(self, 'CommonEquity', Period(df, index_number()))
        setattr(self, 'TotalPreferredEquity', Period(df, index_number()))
        setattr(self, 'MinorityInterestTotal', Period(df, index_number()))
        setattr(self, 'OtherEquity', Period(df, index_number()))
        setattr(self, 'TotalEquity', Period(df, index_number()))
        setattr(self, 'TotalLiabilitiesAndEquity', Period(df, index_number()))
        setattr(self, 'CashAndShortTermInvestments', Period(df, index_number()))
        setattr(self, 'TotalDebt', Period(df, index_number()))


class Period:
    def __init__(self, df, df_index):
        self.df = df.iloc[df_index, :]

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
        col_name = '{year}-{month}-{day}'.format(year=year, month=month, day=day)
        res = self.df[col_name]
        return res
