from worker import *
from main import *

prices=select_prices()

consumption=select_consumption()
automaticsaving(prices,consumption)
