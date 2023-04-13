import random
import datetime
import psycopg2
import config

# Generate random store names
stores = ['Store A', 'Store B', 'Store C', 'Store D', 'Store E']

# Connect to the database
conn = psycopg2.connect(
    host=config.DB_PARAMS['host'],
    port=config.DB_PARAMS['port'],
    user=config.DB_PARAMS['user'],
    password=config.DB_PARAMS['password'],
    dbname=config.DB_PARAMS['database']
)

# Insert dummy data
cur = conn.cursor()
for i in range(1000):
    store_name = random.choice(stores)
    date = datetime.date(2023, random.randint(1, 12), random.randint(1, 28))
    recorded_at_hour = random.randint(0, 23)
    people_count = random.randint(1, 100)
    male_pc = random.randint(0, people_count)
    female_pc = people_count - male_pc
    male_passer = random.randint(0, people_count)
    female_passer = people_count - male_passer
    passer_count = male_passer + female_passer
    age_counts = [random.randint(0, people_count) for _ in range(7)]
    dwell_time_2 = random.randint(0, people_count)
    dwell_time_2_plus = random.randint(0, people_count)
    dwell_time_10_plus = random.randint(0, people_count)
    query = f"""
        INSERT INTO foot_traffic (store_name, date, recorded_at__hour, people_count, "Male(PC)", "Female(PC)", "Male(Passer)", "Female(Passer)", "Passer_Count", "0-12", "13-18", "19-25", "26-35", "36-45", "46-60", "61-100", "Dwell TIme <2", "Dwell TIme >2", "Dwell TIme >10")
        VALUES ('{store_name}', '{date}', {recorded_at_hour}, {people_count}, {male_pc}, {female_pc}, {male_passer}, {female_passer}, {passer_count}, {age_counts[0]}, {age_counts[1]}, {age_counts[2]}, {age_counts[3]}, {age_counts[4]}, {age_counts[5]}, {age_counts[6]}, {dwell_time_2}, {dwell_time_2_plus}, {dwell_time_10_plus});
    """
    cur.execute(query)
conn.commit()
cur.close()
conn.close()
