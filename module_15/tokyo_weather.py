import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("weather_tokyo_data.csv")


df.columns = df.columns.str.strip().str.lower()

# Clean and convert temperature
df['temperature'] = (
    df['temperature']
    .astype(str)
    .str.replace('℃', '', regex=False)
    .str.replace('°C', '', regex=False)
    .str.replace(',', '.', regex=False)
)
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')


df[['month', 'day_num']] = df['day'].str.split('/', expand=True).astype(float)


df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(int).astype(str) + '-' + df['day_num'].astype(int).astype(str), errors='coerce')


df = df.dropna(subset=['date', 'temperature'])


avg_temp = df['temperature'].mean()
print(f"\nAverage Temperature (Overall): {avg_temp:.2f}°C")


monthly_avg = df.groupby('month')['temperature'].mean()

plt.figure(figsize=(10,6))
plt.bar(monthly_avg.index, monthly_avg.values, color='skyblue', edgecolor='black')
plt.title("Average Monthly Temperature in Tokyo")
plt.xlabel("Month")
plt.ylabel("Average Temperature (°C)")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.show()


hottest_day = df.loc[df['temperature'].idxmax()]
coldest_day = df.loc[df['temperature'].idxmin()]

print("\nHottest Day:")
print(hottest_day[['date', 'temperature']])

print("\nColdest Day:")
print(coldest_day[['date', 'temperature']])


top5_hot = df.nlargest(5, 'temperature')[['date', 'temperature']]
top5_cold = df.nsmallest(5, 'temperature')[['date', 'temperature']]

plt.figure(figsize=(10,5))
plt.bar(top5_hot['date'].dt.strftime('%Y-%m-%d'), top5_hot['temperature'], color='red')
plt.title("Top 5 Hottest Days in Tokyo")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))
plt.bar(top5_cold['date'].dt.strftime('%Y-%m-%d'), top5_cold['temperature'], color='blue')
plt.title("Top 5 Coldest Days in Tokyo")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


yearly_avg = df.groupby('year')['temperature'].mean()

plt.figure(figsize=(10,5))
plt.plot(yearly_avg.index, yearly_avg.values, marker='o', color='orange')
plt.title("Average Yearly Temperature in Tokyo")
plt.xlabel("Year")
plt.ylabel("Average Temperature (°C)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


df['season'] = pd.cut(
    df['month'],
    bins=[0, 2, 5, 8, 11, 12],
    labels=['Winter', 'Spring', 'Summer', 'Autumn', 'Winter'],
    right=False,
    ordered=False
)

seasonal_avg = df.groupby('season')['temperature'].mean()

plt.figure(figsize=(7,5))
plt.bar(seasonal_avg.index.astype(str), seasonal_avg.values, color='salmon', edgecolor='black')
plt.title("Average Seasonal Temperature in Tokyo")
plt.ylabel("Average Temperature (°C)")
plt.tight_layout()
plt.show()
