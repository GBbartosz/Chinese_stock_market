
# poprawic raporty chyba recznie bedzie najszybciej
# jakie jeszcze wskazniki moga byc ciekawe




# w przypadku braku danych ilosci akcji brałem kwartał poprzedni lub następny
# NetIncometoStockholders vs NetIncometoCompany in P/E
# P/E average for sector = average of P/Es of companies

import functions as f
import pandas as pd

#def calc(f):
#    def f2(minl, *args):
#        xs = 0
#        c, d = minl
#        for i in list(range(3)):
#            x = f(i, *args)
#            x = x + c + d
#            xs += x
#        return xs
#    return f2
#
#@calc
#def f1(i, a, b):
#    x = a + b + i
#    return x
#
#c0 = 10
#d0 = 100
#a0 = 1
#b0 = 2
#inl = [c0, d0]
#res = f1(inl, a0, b0)
#print(res)


f.dataframe_display_options()
sector_companys_dic = f.create_sector_companys_dictionary()
companies = sector_companys_dic['Industrials']
for company in companies:
    print(company)
    path = 'C:\\Users\\Bartek\\Desktop\\ALK praca magisterska\\China_stock_data\\{} - Income Statement.csv'.format(company)
    try:
        df = pd.read_csv(path)
        print(df.iloc[24, :])
    except:
        continue

