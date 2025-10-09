import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('avgIQpercountry.csv')

plt.figure(figsize=(12,6))
sns.boxplot(data=df, x='Continent', y='Average IQ')
plt.title('Boxplot of Average IQ by Continent')
plt.xlabel('Continent')
plt.ylabel('Average IQ')
plt.tight_layout()
plt.show()