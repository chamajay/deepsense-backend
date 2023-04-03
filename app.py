from flask import Flask, request, jsonify
from flask import Flask, g
import models
import preprocess
import sqlite3
import datetime

# Database
DATABASE = "db/predictions.db"

# Load models and get classifiers
emotion_classifier = models.load_emotion_distilroberta()
suicidal_classifer = models.load_suicidal_text_electra()

# Create the Flask app
app = Flask(__name__)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def create_table():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS predictions
            (prediction_id INTEGER PRIMARY KEY, record_timestamp TEXT, preprocessed_text TEXT, text TEXT,
             emotion_joy REAL, emotion_surprise REAL, emotion_neutral REAL, emotion_sadness REAL,
             emotion_anger REAL, emotion_disgust REAL, emotion_fear REAL, primary_emotion TEXT, 
             suicidal_label_0 REAL, suicidal_label_1 REAL, suicide_risk TEXT)"""
        )

        db.commit()


def get_score(arr, label):
    for item in arr:
        if item["label"] == label:
            return item["score"]


def insert_new(text, predictions):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract data from the predictions
        preprocessed_text = text["preprocessed_text"]
        text = text["text"]

        emotions = {
            "joy": get_score(predictions["emotion"][0], "joy"),
            "surprise": get_score(predictions["emotion"][0], "surprise"),
            "neutral": get_score(predictions["emotion"][0], "neutral"),
            "sadness": get_score(predictions["emotion"][0], "sadness"),
            "anger": get_score(predictions["emotion"][0], "anger"),
            "disgust": get_score(predictions["emotion"][0], "disgust"),
            "fear": get_score(predictions["emotion"][0], "fear"),
        }

        primary_emotion = max(emotions, key=emotions.get)

        suicidal = {
            "non-suicidal": get_score(predictions["suicidal"][0], "LABEL_0"),
            "suicidal": get_score(predictions["suicidal"][0], "LABEL_1"),
        }

        suicide_risk = max(suicidal, key=suicidal.get)

        cursor.execute(
            """INSERT INTO predictions 
                (record_timestamp, preprocessed_text, text, emotion_joy, emotion_surprise, emotion_neutral, emotion_sadness,
                emotion_anger, emotion_disgust, emotion_fear, primary_emotion, suicidal_label_0, suicidal_label_1, suicide_risk)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                timestamp,
                preprocessed_text,
                text,
                emotions["joy"],
                emotions["surprise"],
                emotions["neutral"],
                emotions["sadness"],
                emotions["anger"],
                emotions["disgust"],
                emotions["fear"],
                primary_emotion,
                suicidal["non-suicidal"],
                suicidal["suicidal"],
                suicide_risk,
            ),
        )

        db.commit()


# Define the API endpoint for text processing
# curl -s -X POST -H "Content-Type: application/json" -d '{"text":"i want to kill myself"}' http://localhost:5000/text-input | jq
@app.route("/text-input", methods=["POST"])
def process_text():
    # get the input data from the request
    input_text = request.json["text"]

    app.logger.info("text", input_text)

    # preprocess the text data
    preprocessed_text = preprocess.process_txt(input_text)

    app.logger.info("preprocessed_text", preprocessed_text)

    # generate predictions
    emotion_predictions = emotion_classifier(preprocessed_text)
    suicidal_predictions = suicidal_classifer(preprocessed_text)

    text = {"text": input_text, "preprocessed_text": preprocessed_text}

    predictions = {"emotion": emotion_predictions, "suicidal": suicidal_predictions}

    insert_new(text, predictions)

    return {"text": text, "predictions": predictions}


# Define the API endpoint for retrieving the overall mood of the day
# curl http://localhost:5000/today-mood
@app.route("/today-mood")
def mood_today():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        query = """
            SELECT primary_emotion 
            FROM predictions 
            WHERE DATE(record_timestamp) = DATE('now') 
            GROUP BY primary_emotion 
            ORDER BY COUNT(*) DESC, MAX(record_timestamp) DESC
            LIMIT 1
        """

        # Execute the query to get the highest repeated emotion
        cursor.execute(query)
        result = cursor.fetchone()

        response = {"today_mood": "None"}

        if (result is not None):
            response = {"today_mood": result[0]}

        app.logger.info("result", result)

        return response


# Define the API endpoint for retrieving the main 3 mood percentages of the day
# curl http://localhost:5000/today_mood_percentages
@app.route("/today_mood_percentages")
def mood_percentages_today():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        query = """
            SELECT primary_emotion, COUNT(*) as count
            FROM predictions
            WHERE DATE(record_timestamp) = DATE('now') 
            GROUP BY primary_emotion
            ORDER BY count DESC, MAX(record_timestamp) DESC;
        """

        # Execute the query to get the emotion count
        cursor.execute(query)
        rows = cursor.fetchall()

        response = {"main_mood_percentages": "None"}

        if (rows is not None):
            # Total count
            total_count = sum([row[1] for row in rows])

            result = []

            for row in rows:
                emotion, count = row
                percentage = (count / total_count) * 100
                result.append(
                    {
                        "emotion": emotion,
                        "percentage": round(percentage, 1),
                    }
            )

            response = {"main_mood_percentages": result}

        return response


# Define the API endpoint for retrieving the latest 10 typing activity and their mood percentages
# curl http://localhost:5000/recent-text-activity
@app.route("/recent-text-activity")
def recent_text_activity():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        query = """
            SELECT 
                text, 
                emotion_joy, 
                emotion_surprise, 
                emotion_neutral, 
                emotion_sadness, 
                emotion_anger, 
                emotion_disgust, 
                emotion_fear, 
                primary_emotion, 
                suicidal_label_0, 
                suicidal_label_1, 
                suicide_risk 
            FROM predictions 
            ORDER BY record_timestamp DESC 
            LIMIT 10
        """

        # Execute the query to get the highest repeated emotion
        cursor.execute(query)
        rows = cursor.fetchall()

        response = {"recent_text_activity": "None"}

        if (rows is not None):
            result = []
            for row in rows:
                (
                    text,
                    joy,
                    surprise,
                    neutral,
                    sadness,
                    anger,
                    disgust,
                    fear,
                    primary_emotion,
                    label_0,
                    label_1,
                    risk,
                ) = row
                result.append(
                    {
                        "text": text,
                        "joy": round(joy * 100, 2),
                        "surprise": round(surprise * 100, 2),
                        "neutral": round(neutral * 100, 2),
                        "sadness": round(sadness * 100, 2),
                        "anger": round(anger * 100, 2),
                        "disgust": round(disgust * 100, 2),
                        "fear": round(fear * 100, 2),
                        "primary_emotion": primary_emotion,
                        "suicidal_label_0": round(label_0 * 100, 2),
                        "suicidal_label_1": round(label_1 * 100, 2),
                        "suicide_risk": risk
                    }
                )
                response = {"recent_text_activity": result}

        return response


if __name__ == "__main__":
    create_table()
    app.run(host="0.0.0.0")
    # app.run()
