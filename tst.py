# ktore sprawozdanai nie są w yuanach
# jakie jeszcze wskazniki moga byc ciekawe
# poprawic raport braku danych
# volatility


# w przypadku braku danych ilosci akcji brałem kwartał poprzedni lub następny
# NetIncometoStockholders vs NetIncometoCompany in P/E
# P/E average for sector = average of P/Es of companies

def calc(f):
    def f2(minl, *args):
        xs = 0
        c, d = minl
        for i in list(range(3)):
            x = f(i, *args)
            x = x + c + d
            xs += x
        return xs
    return f2

@calc
def f1(i, a, b):
    x = a + b + i
    return x

c0 = 10
d0 = 100
a0 = 1
b0 = 2
inl = [c0, d0]
res = f1(inl, a0, b0)
print(res)
