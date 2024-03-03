from kafka import KafkaConsumer
import json
import psycopg2
from utils import producer

# Replace 'your_kafka_server' with your Kafka server address
kafka_server = 'localhost:9093'

# Create a Kafka consumer
consumer = KafkaConsumer(
    'fraudulent_analysis',  # Kafka topic
    bootstrap_servers=[kafka_server],
    auto_offset_reset='earliest',  # Start reading at the earliest message
    enable_auto_commit=True,
    group_id='fraudulent_analysis-listener-consumer-group',  # Consumer group ID
    value_deserializer=lambda x: json.loads(x.decode())
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
    INSERT INTO public.fraudulent_analysis (
        transaction_id, user_id, is_fraud
    ) VALUES (
        %(transaction_id)s, %(user_id)s, %(is_fraud)s
    )
    RETURNING id;
"""

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()


def save_fraudulent_analysis_into_pg(fraudulent_analysis):
    # Insert data into the database
    cursor.execute(insert_sql, fraudulent_analysis)
    analysis_id = cursor.fetchone()[0]
    conn.commit()  # Commit the transaction

    return analysis_id


try:
    # Listen and print messages
    for message in consumer:
        try:
            fraudulent_analysis = message.value
            fraudulent_analysis['is_fraud'] = fraudulent_analysis['is_fraud'] == 1
            analysis_id = save_fraudulent_analysis_into_pg(fraudulent_analysis)

            fraudulent_analysis['analysis_id'] = analysis_id

            # Returning it back, lazy Ivan
            fraudulent_analysis['is_fraud'] = 1 if fraudulent_analysis['is_fraud'] else 0

            producer.publish_message('fraudulent_analysis', fraudulent_analysis)

            # influx.write_into_influx('transactions', 'fraudulent_analysis', fraudulent_analysis,
            #                          {
            #                              'user_id': fraudulent_analysis['user_id'],
            #                              'status': 'Fraud' if fraudulent_analysis['is_fraud'] == 1 else 'Normal'
            #                          })

        except Exception as e:
            print(f"An error occurred: {e}")
finally:
    # Close the database connection
    cursor.close()
    conn.close()
