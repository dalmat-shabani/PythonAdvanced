import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("avgIQpercountry.csv")
nobel_prizes_per_country = df.groupby('Continent')['Nobel Prices'].sum()

no_of_continents = nobel_prizes_per_country.count()

print(no_of_continents)

colors = ['gold', 'violet', 'yellow', 'pink', 'orange', 'blue', 'aquamarine', 'red']

plt.figure(figsize=(10,10))

nobel_prizes_per_country.plot(kind='pie', colors=colors , autopct='%1.1f%%')

plt.title('Distribution of Nobel Prizes by Continent')

plt.axis('equal')

plt.ylabel('')

plt.tight_layout()

plt.show()