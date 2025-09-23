import datetime

current_datetime = datetime.datetime.now()
print(current_datetime)

print("Year: ", current_datetime.year)
print("Month: ", current_datetime.month)
print("Day: ", current_datetime.day)
print("Hour: " , current_datetime.hour)
print("Minute: ", current_datetime.minute)
print("Second: ", current_datetime.second)
print("Mcrosecond: ", current_datetime.microsecond)

#date class
current_date = datetime.datetime.now().date()
print(current_date)
print("Year: ", current_date.year)
print("Month: ", current_date.month)
print("Day: ", current_date.day)

current_time = datetime.datetime.now().time()
print(current_time)
print("Hour: ", current_time.hour)
print("Minutes: ", current_time.minute)
print("Second: " , current_time.second)

specific_date = datetime.date(2026, 4, 25)
specidic_time = datetime.time(12,30,0)

duration = datetime.timedelta(days=5, hours=3)

previous_date = current_date - duration
print(previous_date)

utc_time = datetime.datetime.now(datetime.timezone.utc)