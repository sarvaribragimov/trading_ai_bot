from barchart import *
from insider_transaction import *
from volume import *

def all_information(ticker):
    a= transaction(ticker)
    b=get_volume(ticker)


ticker = 'NVDA'
a = all_information(ticker)
print(a)