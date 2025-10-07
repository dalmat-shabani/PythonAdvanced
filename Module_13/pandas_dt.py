import pandas as pd

data = {'Name':['Alice', 'Bob', 'Charlie'],
        'Age':[25,30,22],
        'City': ['Pristina', 'New York', 'LA']}

df = pd.DataFrame(data)
print(df)

#readig and writing data

#read data from a CSV file
df = pd.read_csv('your_database.csv')

#Write data to CSV File
df.to_csv('output_dataset.csv', index=False)