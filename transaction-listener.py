from datetime import datetime

from kafka import KafkaConsumer
import json
import psycopg2
from joblib import load
import pandas as pd
from utils import producer

# Replace 'your_kafka_server' with your Kafka server address
kafka_server = 'localhost:9093'

# Create a Kafka consumer
consumer = KafkaConsumer(
    'transactions', # Kafka topic
    bootstrap_servers=[kafka_server],
    auto_offset_reset='earliest', # Start reading at the earliest message
    enable_auto_commit=True,
    group_id='transactions-listener-consumer-group', # Consumer group ID
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) # Deserialize JSON messages
)

# Database connection parameters
db_params = {
    "dbname": "data-warehouse",
    "user": "admin",  # Adjust as per your PostgreSQL setup
    "password": "admin",  # Add your password if required
    "host": "localhost"
}

# SQL statement for inserting data
insert_sql = """
    INSERT INTO public.transactions (
        "time", user_id, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10,
        v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22,
        v23, v24, v25, v26, v27, v28, amount, created_at
    ) VALUES (
        %(Time)s, %(user_id)s, %(V1)s, %(V2)s, %(V3)s, %(V4)s, %(V5)s, %(V6)s,
        %(V7)s, %(V8)s, %(V9)s, %(V10)s, %(V11)s, %(V12)s, %(V13)s, %(V14)s,
        %(V15)s, %(V16)s, %(V17)s, %(V18)s, %(V19)s, %(V20)s, %(V21)s, %(V22)s,
        %(V23)s, %(V24)s, %(V25)s, %(V26)s, %(V27)s, %(V28)s, %(Amount)s, %(created_at)s
    )
    RETURNING id;
"""
model_filename = 'logistic_regression_model.joblib'
# Load the model from disk
model = load(model_filename)


# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()


def save_transaction_into_pg(event):
    # Insert data into the database
    cursor.execute(insert_sql, event)
    transaction_id = cursor.fetchone()[0]
    conn.commit()  # Commit the transaction

    return transaction_id


def calculate_transaction_size(amount):
    # Define thresholds
    small_threshold = 10  # Amounts <= 10 are considered small
    medium_threshold = 100  # Amounts > 10 and <= 100 are considered medium
    # Amounts > 100 are considered large

    if amount <= small_threshold:
        return "Small"
    elif amount <= medium_threshold:
        return "Medium"
    else:
        return "Large"


try:
    # Listen and print messages
    for message in consumer:
        try:
            event = json.loads(message.value)
            event['created_at'] = datetime.now()
            transaction_id = save_transaction_into_pg(event)
            del event['created_at']

            row_data = pd.DataFrame([event])
            row_data = row_data.drop(columns=['Class', 'user_id', 'Time'])

            is_fraud = model.predict(row_data)[0]

            if is_fraud == 1:
                print("The following transaction was recognized as a fraudulent activity: ", event)

            fraudulent_analysis = {
                'transaction_id': transaction_id,
                'user_id': int(event['user_id']),
                'timestamp': int(event['Time']),
                'is_fraud': int(is_fraud)
            }

            producer.publish_message('fraudulent_analysis', fraudulent_analysis)

        except Exception as e:
            print(f"An error occurred: {e}")
finally:
    # Close the database connection
    cursor.close()
    conn.close()
