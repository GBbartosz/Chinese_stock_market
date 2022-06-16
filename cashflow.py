class CashFlow():
    def __init__(self, df):
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

        positions_dic = {'Net Income to Stockholders': 'NetIncometoStockholders',
                         'Depreciation & Amortization (CF)': 'DepreciationAmortizationCF',
                         'Amortization of Deferred Charges (CF)': 'AmortizationofDeferredChargesCF',
                         'Stock-Based Comp': 'StockBasedComp',
                         'Change In Accounts Receivable': 'ChangeInAccountsReceivable',
                         'Change In Inventories': 'ChangeInInventories',
                         'Change in Other Net Operating Assets': 'ChangeinOtherNetOperatingAssets',
                         'Other Operating Activities': 'OtherOperatingActivities',
                         'Cash from Operations': 'CashfromOperations', 'Capital Expenditures': 'CapitalExpenditures',
                         'Cash Acquisitions': 'CashAcquisitions',
                         'Other Investing Activities': 'OtherInvestingActivities',
                         'Cash from Investing': 'CashfromInvesting',
                         'Dividends Paid (Ex Special Dividends)': 'DividendsPaidExSpecialDividends',
                         'Special Dividend Paid': 'SpecialDividendPaid', 'Long-Term Debt Issued': 'LongTermDebtIssued',
                         'Long-Term Debt Repaid': 'LongTermDebtRepaid',
                         'Repurchase of Common Stock': 'RepurchaseofCommonStock',
                         'Other Financing Activities': 'OtherFinancingActivities',
                         'Cash from Financing': 'CashfromFinancing', 'Beginning Cash (CF)': 'BeginningCashCF',
                         'Foreign Exchange Rate Adjustments': 'ForeignExchangeRateAdjustments',
                         'Additions / Reductions': 'AdditionsReductions', 'Ending Cash (CF)': 'EndingCashCF',
                         'Levered Free Cash Flow': 'LeveredFreeCashFlow', 'Cash Interest Paid': 'CashInterestPaid'}

        for position in positions_dic.keys():
            ind_num = df[df['Positions'] == position].index.values
            setattr(self, positions_dic[position], Period(df, ind_num))


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
        res = float(self.df[col_name])
        return res
