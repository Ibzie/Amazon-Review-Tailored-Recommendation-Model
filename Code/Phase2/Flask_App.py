from flask import Flask, render_template, request
from kafka import KafkaProducer, KafkaConsumer
import pandas as pd
import json


app = Flask(__name__)

# sample list of ASINs for demonstration purposes
ASINS = ['B08CJF6KGY', 'B07RF1XD36', 'B07K7VTFJ1', 'B08HJTH61J']

def filter_products(asins, rating):
    data = pd.read_parquet('user_recommendations.parquet')
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    id_to_match = "id"
    for asin in asins:
        filtered_data = data[data[id_to_match] == asin]
        for index, row in filtered_data.iterrows():
            # Create a dictionary with the relevant data
            dic = {
                "id": row['id'],
                "movie_title": row['movie_title'],
                "genre": row['genre'],
                "imdb_rating": row['imdb_rating'],
                "recommendation_score": row['recommendation_score']
            }
            # Send the dictionary to the Kafka topic
            producer.send('user_recommendations', dic)
            producer.flush()
    # Close the producer
    producer.close()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        asin = request.form['asin']
        rating = int(request.form['rating'])

        # Create Kafka consumer
        consumer = KafkaConsumer('user_recommendations', bootstrap_servers=['localhost:9092'],
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        # Create a list to store filtered products
        filtered_products = []

        # Iterate over Kafka messages
        for message in consumer:
            # Check if the received product's asin and rating match the user input
            if message.value["asin"] == asin and message.value["overall"] >= rating:
                # Add the matching product to the list
                filtered_products.append(message.value)

        # Close the Kafka consumer
        consumer.close()

        return render_template('display.html', products=filtered_products)

    return render_template('home.html')


class SimpleProducer(KafkaProducer):
    def __init__(self, *args, **kwargs):
        self.is_async = kwargs.pop('async', False)
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<SimpleProducer batch=%s>' % self.is_async


if __name__ == '__main__':
    app.run(debug=True)
