import datetime
from functions import key_error_handler


class Balance():
    def __init__(self, df):
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

        positions_dic = {'Cash And Equivalents': 'CashAndEquivalents', 'Short Term Investments': 'ShortTermInvestments',
                         'Accounts Receivable': 'AccountsReceivableNet', 'Inventory': 'Inventory',
                         'Prepaid Expenses': 'PrepaidExpenses', 'Other Current Assets': 'OtherCurrentAssets',
                         'Total Current Assets': 'TotalCurrentAssets',
                         'Property Plant And Equipment': 'PropertyPlantAndEquipmentNet',
                         'Real Estate Owned': 'RealEstateOwned',
                         'Capitalized / Purchased Software': 'CapitalizedPurchasedSoftware',
                         'Long-term Investments': 'LongtermInvestments', 'Goodwill': 'Goodwill',
                         'Other Intangibles': 'OtherIntangibles', 'Other Long-term Assets': 'OtherLongtermAssets',
                         'Total Assets': 'TotalAssets', 'Accounts Payable': 'AccountsPayable',
                         'Accrued Expenses': 'AccruedExpenses', 'Short-term Borrowings': 'ShorttermBorrowings',
                         'Current Portion of LT Debt': 'CurrentPortionofLTDebt',
                         'Current Portion of Capital Lease Obligations': 'CurrentPortionofCapitalLeaseObligations',
                         'Other Current Liabilities': 'OtherCurrentLiabilities',
                         'Total Current Liabilities': 'TotalCurrentLiabilities', 'Long-term Debt': 'LongtermDebt',
                         'Capital Leases': 'CapitalLeases',
                         'Other Non-current Liabilities': 'OtherNoncurrentLiabilities',
                         'Total Liabilities': 'TotalLiabilities', 'Common Stock': 'CommonStock',
                         'Additional Paid In Capital': 'AdditionalPaidInCapital',
                         'Retained Earnings': 'RetainedEarnings', 'Treasury Stock': 'TreasuryStock',
                         'Other Common Equity Adj': 'OtherCommonEquityAdj', 'Common Equity': 'CommonEquity',
                         'Total Preferred Equity': 'TotalPreferredEquity', 'Minority Interest': 'MinorityInterestTotal',
                         'Other Equity': 'OtherEquity', 'Total Equity': 'TotalEquity',
                         'Total Liabilities And Equity': 'TotalLiabilitiesAndEquity',
                         'Cash And Short Term Investments': 'CashAndShortTermInvestments', 'Total Debt': 'TotalDebt',
                         'Accounts Receivable, Net': 'AccountsReceivableNet',
                         'Property Plant And Equipment, Net': 'PropertyPlantAndEquipmentNet',
                         'Minority Interest, Total': 'MinorityInterestTotal'}

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
        res = key_error_handler(self, year, month, day)
        return res
