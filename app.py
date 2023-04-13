from flask import Flask, render_template, request, jsonify
import psycopg2
import openai
import config
app = Flask(__name__)
openai.api_key = config.OPENAI_API_KEY

def connect_to_db():
    return psycopg2.connect(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

def generate_sql_query(prompt):
    openai.api_key = config.OPENAI_API_KEY

    db_context = (
        "I have a PostgreSQL database called 'chatbotdb' with a table named 'foot_traffic'. "
        "The 'foot_traffic' table contains data on foot traffic in stores. "
        "The columns in this table include: "
        "'store_name' (text) - the name of the store, "
        "'date' (date) - the date the foot traffic was recorded, "
        "'foot_traffic.recorded_at__hour' (integer) - the hour of the day the foot traffic was recorded, "
        "'foot_traffic.people_count' (integer) - the total number of people recorded, "
        "'foot_traffic.Male(PC)' (integer) - the number of male customers counted by the device, "
        "'foot_traffic.Female(PC)' (integer) - the number of female customers counted by the device, "
        "'foot_traffic.Male(Passer)' (integer) - the number of male passersby counted by the device, "
        "'foot_traffic.Female(Passer)' (integer) - the number of female passersby counted by the device, "
        "'foot_traffic.Passer_Count' (integer) - the total number of passersby counted by the device, "
        "'foot_traffic.0-12' (integer) - the number of people in the age range of 0-12 years old, "
        "'foot_traffic.13-18' (integer) - the number of people in the age range of 13-18 years old, "
        "'foot_traffic.19-25' (integer) - the number of people in the age range of 19-25 years old, "
        "'foot_traffic.26-35' (integer) - the number of people in the age range of 26-35 years old, "
        "'foot_traffic.36-45' (integer) - the number of people in the age range of 36-45 years old, "
        "'foot_traffic.46-60' (integer) - the number of people in the age range of 46-60 years old, "
        "'foot_traffic.61-100' (integer) - the number of people in the age range of 61-100 years old, "
        "'foot_traffic.Dwell TIme <2' (integer) - the number of people who spent less than 2 minutes in the store, "
        "'foot_traffic.Dwell TIme >2' (integer) - the number of people who spent more than 2 minutes but less than 10 minutes in the store, "
        "'foot_traffic.Dwell TIme >10' (integer) - the number of people who spent more than 10 minutes in the store."
    )

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{db_context}"
               f"Strictly write only full, complete and accurate SQl queries for the data and answer the following questions: {prompt}",

        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    query = response.choices[0].text.strip()
    query = query.replace("and", ";") # split the query into two separate queries
    return query




def fetch_data_from_db(query):
    conn = psycopg2.connect(**config.DB_PARAMS)
    cur = conn.cursor()

    cur.execute(query)
    result = cur.fetchall()

    cur.close()
    conn.close()

    return result


def generate_response(data):
    response = "Here are the results: " + ", ".join([str(x[0]) for x in data])
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.form["prompt"]
        query = generate_sql_query(user_message)
        print(f"Generated SQL query: {query}")
        data = fetch_data_from_db(query)
        print(f"Fetched data: {data}")
        if data:
            response = ", ".join(str(datum[0]) for datum in data)
            return jsonify({"response": response})
        else:
            return jsonify({"response": "No data found."})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"response": "An error occurred while processing your request."})




if __name__ == "__main__":
    app.run()
