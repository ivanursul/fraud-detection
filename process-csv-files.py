import pandas as pd
import seaborn as sns
import time
from kafka import KafkaProducer
import json
from utils import producer

sns.set()

df = pd.read_csv('creditcard.csv')
print(df.shape)
df.head()
df.info()
df.describe()
feature_names = df.iloc[:, 2:31].columns


# def json_serializer(data):
#     return json.dumps(data).encode('utf-8')
#
#
# def publish_message(topic_name, value):
#     producer.send(topic_name, value)
#     producer.flush()
#
#
# producer = KafkaProducer(
#     bootstrap_servers=['localhost:9093'],  # Update the port if your Kafka runs on a different one
#     value_serializer=json_serializer
# )

# Coefficient to scale the time differences
# For example, if your times are in tenths of a second, and you want to simulate
# one-tenth of a second as one second, you could set this to 10.
# Adjust this value to control the speed of your simulation.
time_coefficient = 100.0

# Initialize the previous time to 0 for the first record
prev_time = 0

# Loop through the DataFrame and make predictions for each row
for index, row in df.iterrows():
    # Keep the row in DataFrame format to maintain feature names
    row_data = pd.DataFrame([row[feature_names]])

    # Extract the time from the current row
    current_time = int(row['Time'])

    # Calculate the time difference from the previous row
    time_diff = current_time - prev_time

    # Adjust the time difference using the coefficient
    adjusted_time_diff = time_diff / time_coefficient

    # Sleep for the adjusted time difference to simulate real-time processing
    time.sleep(adjusted_time_diff)

    transaction = row.to_json()
    topic_name = 'transactions'

    producer.publish_message(topic_name, transaction)
    print("Transaction published successfully: ", transaction)

    # Update the previous time to the current time for the next iteration
    prev_time = current_time