import datetime
from functions import key_error_handler


class IncomeStatement:
    def __init__(self, df):
        self.Revenue = None
        self.RevenueGrowthYoY = None
        self.CostofRevenues = None
        self.GrossProfit = None
        self.GrossProfitMargin = None
        self.RDExpenses = None
        self.SellingandMarketingExpense = None
        self.SellingAdminExpenses = None
        self.SellingGeneralAdminExpenses = None
        self.GeneralAdminExpenses = None
        self.OtherIncExp = None
        self.OperatingExpenses = None
        self.OperatingIncome = None
        self.NetInterestExpenses = None
        self.EBTInclUnusualItems = None
        self.EarningsofDiscontinuedOps = None
        self.IncomeTaxExpense = None
        self.NetIncometoCompany = None
        self.MinorityInterestinEarnings = None
        self.NetIncometoStockholders = None
        self.PreferredDividendsOtherAdj = None
        self.NetIncometoCommonExclExtraItems = None
        self.BasicEPSContOps = None
        self.DilutedEPSContOps = None
        self.WeightedAverageBasicSharesOut = None
        self.WeightedAverageDilutedSharesOut = None
        self.EBITDA = None
        self.EBIT = None
        self.RevenueReported = None
        self.OperatingIncomeReported = None
        self.OperatingIncomeAdjusted = None

        positions_dic = {'Revenue': 'Revenue', 'Revenue Growth (YoY)': 'RevenueGrowthYoY',
                         'Cost of Revenues': 'CostofRevenues', 'Gross Profit': 'GrossProfit',
                         'Gross Profit Margin': 'GrossProfitMargin', 'R&D Expenses': 'RDExpenses',
                         'Selling and Marketing Expense': 'SellingandMarketingExpense',
                         'Selling, General & Admin Expenses': 'SellingGeneralAdminExpenses',
                         'General & Admin Expenses': 'GeneralAdminExpenses', 'Other Inc / (Exp)': 'OtherIncExp',
                         'Operating Expenses': 'OperatingExpenses', 'Operating Income': 'OperatingIncome',
                         'Net Interest Expenses': 'NetInterestExpenses',
                         'EBT, Incl. Unusual Items': 'EBTInclUnusualItems', 'EBT': 'EBT',
                         'Earnings of Discontinued Ops.': 'EarningsofDiscontinuedOps',
                         'Income Tax Expense': 'IncomeTaxExpense', 'Net Income to Company': 'NetIncometoCompany',
                         'Minority Interest in Earnings': 'MinorityInterestinEarnings',
                         'Net Income to Stockholders': 'NetIncometoStockholders',
                         'Preferred Dividends & Other Adj.': 'PreferredDividendsOtherAdj',
                         'Net Income to Common Excl Extra Items': 'NetIncometoCommonExclExtraItems',
                         'Basic EPS (Cont. Ops)': 'BasicEPSContOps', 'Diluted EPS (Cont. Ops)': 'DilutedEPSContOps',
                         'Weighted Average Basic Shares Out.': 'WeightedAverageBasicSharesOut',
                         'Weighted Average Diluted Shares Out.': 'WeightedAverageDilutedSharesOut', 'EBITDA': 'EBITDA',
                         'EBIT': 'EBIT', 'Revenue (Reported)': 'RevenueReported',
                         'Operating Income (Reported)': 'OperatingIncomeReported',
                         'Operating Income (Adjusted)': 'OperatingIncomeAdjusted'}

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

