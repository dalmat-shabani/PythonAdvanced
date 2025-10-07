import pandas as pd

from Module_5.challenge_practice import total

products = ['Apples', 'Bananas', 'Oranges', 'Grapes', 'Pinapples']

sales = [150,200, 180,90,60]

sales_series = pd.Series(sales, index=products)
#print(sales_series)

print(sales_series['Grapes'])

total_sales = sales_series.sum()
print(total_sales)

best_selling_product = sales_series.idmax()
print(best_selling_product)

