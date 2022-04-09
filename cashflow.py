class CashFlow():
    def __init__(self, df):
        def index_number():
            nonlocal ind_num
            ind_num += 1
            return ind_num

        self.NetIncometoStockholders = None
        self.DepreciationAmortizationCF = None
        self.AmortizationofDeferredChargesCF = None
        self.StockBasedComp = None
        self.ChangeInAccountsReceivable = None
        self.ChangeInInventories = None
        self.ChangeinOtherNetOperatingAssets = None
        self.OtherOperatingActivities = None
        self.CashfromOperations = None
        self.CapitalExpenditures = None
        self.CashAcquisitions = None
        self.OtherInvestingActivities = None
        self.CashfromInvesting = None
        self.DividendsPaidExSpecialDividends = None
        self.SpecialDividendPaid = None
        self.LongTermDebtIssued = None
        self.LongTermDebtRepaid = None
        self.RepurchaseofCommonStock = None
        self.OtherFinancingActivities = None
        self.CashfromFinancing = None
        self.BeginningCashCF = None
        self.ForeignExchangeRateAdjustments = None
        self.AdditionsReductions = None
        self.EndingCashCF = None
        self.LeveredFreeCashFlow = None
        self.CashInterestPaid = None

        ind_num = 0
        setattr(self, 'NetIncometoStockholders', Period(df, ind_num))
        setattr(self, 'DepreciationAmortizationCF', Period(df, index_number()))
        setattr(self, 'AmortizationofDeferredChargesCF', Period(df, index_number()))
        setattr(self, 'StockBasedComp', Period(df, index_number()))
        setattr(self, 'ChangeInAccountsReceivable', Period(df, index_number()))
        setattr(self, 'ChangeInInventories', Period(df, index_number()))
        setattr(self, 'ChangeinOtherNetOperatingAssets', Period(df, index_number()))
        setattr(self, 'OtherOperatingActivities', Period(df, index_number()))
        setattr(self, 'CashfromOperations', Period(df, index_number()))
        setattr(self, 'CapitalExpenditures', Period(df, index_number()))
        setattr(self, 'CashAcquisitions', Period(df, index_number()))
        setattr(self, 'OtherInvestingActivities', Period(df, index_number()))
        setattr(self, 'CashfromInvesting', Period(df, index_number()))
        setattr(self, 'DividendsPaidExSpecialDividends', Period(df, index_number()))
        setattr(self, 'SpecialDividendPaid', Period(df, index_number()))
        setattr(self, 'LongTermDebtIssued', Period(df, index_number()))
        setattr(self, 'LongTermDebtRepaid', Period(df, index_number()))
        setattr(self, 'RepurchaseofCommonStock', Period(df, index_number()))
        setattr(self, 'OtherFinancingActivities', Period(df, index_number()))
        setattr(self, 'CashfromFinancing', Period(df, index_number()))
        setattr(self, 'BeginningCashCF', Period(df, index_number()))
        setattr(self, 'ForeignExchangeRateAdjustments', Period(df, index_number()))
        setattr(self, 'AdditionsReductions', Period(df, index_number()))
        setattr(self, 'EndingCashCF', Period(df, index_number()))
        setattr(self, 'LeveredFreeCashFlow', Period(df, index_number()))
        setattr(self, 'CashInterestPaid', Period(df, index_number()))


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
