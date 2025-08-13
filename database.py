import sqlite3
import json
import csv

DB_NAME = "new_client_data.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_data (
            client_name TEXT PRIMARY KEY,
            sentiment TEXT,
            catalog TEXT,
            suggestions TEXT,
            last_reply TEXT,
            list_of_convo TEXT
        )
    ''')

    conn.commit()
    conn.close()


def insert_or_update_chat_data(data: dict):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    client_name = data.get("client_name")
    new_sentiment = data.get("sentiment")
    new_catalog = data.get("catalog")
    new_suggestions = data.get("suggestions")
    new_last_reply = data.get("last_reply")
    new_convo = data.get("list_of_convo", [])

    # Check if the client already exists
    c.execute("SELECT catalog, suggestions, list_of_convo FROM chat_data WHERE client_name = ?", (client_name,))
    existing_row = c.fetchone()

    if existing_row:
        existing_catalog, existing_suggestions, existing_convo_json = existing_row

        # Handle catalog: once True stays True
        updated_catalog = "True" if existing_catalog == "True" or new_catalog == "True" else "False"

        # Suggestions logic
        old_sug = existing_suggestions.strip().lower() if existing_suggestions else "no"
        new_sug = new_suggestions.strip().lower() if new_suggestions else "no"

        if old_sug == "no" and new_sug == "no":
            updated_suggestions = "No"
        elif old_sug == "no" and new_sug != "no":
            updated_suggestions = new_suggestions
        elif old_sug != "no" and new_sug != "no":
            updated_suggestions = f"{existing_suggestions}, {new_suggestions}"
        else:  # old != "no" and new == "no"
            updated_suggestions = existing_suggestions

        # Conversations: merge and keep last 3
        try:
            existing_convo = json.loads(existing_convo_json)
        except (json.JSONDecodeError, TypeError):
            existing_convo = []

        updated_convo = existing_convo + new_convo
        updated_convo = updated_convo[-3:]

        c.execute('''
            UPDATE chat_data SET
                sentiment = ?,
                catalog = ?,
                suggestions = ?,
                last_reply = ?,
                list_of_convo = ?
            WHERE client_name = ?
        ''', (
            new_sentiment,
            updated_catalog,
            updated_suggestions,
            new_last_reply,
            json.dumps(updated_convo),
            client_name
        ))
    else:
        # Limit convo to last 3 on insert
        new_convo = new_convo[-3:]
        c.execute('''
            INSERT INTO chat_data (
                client_name,
                sentiment,
                catalog,
                suggestions,
                last_reply,
                list_of_convo
            )
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            client_name,
            new_sentiment,
            new_catalog,
            new_suggestions,
            new_last_reply,
            json.dumps(new_convo)
        ))

    conn.commit()
    conn.close()


def get_chat_data_by_client(client_name):
    """Fetch stored chat data by client name/number"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT list_of_convo FROM chat_data WHERE client_name = ?", (client_name,))
    row = c.fetchone()
    conn.close()

    if row:
        try:
            return json.loads(row[0])  # list_of_convo is stored as JSON
        except:
            return []
    return None


def export_to_csv(filename="client_chat_data.csv"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM chat_data")
    rows = c.fetchall()
    columns = [desc[0] for desc in c.description]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"✅ Data exported to '{filename}'")


def delete_client_data(client_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM chat_data WHERE client_name = ?", (client_name,))

    conn.commit()
    conn.close()


# Example usage
if __name__ == "__main__":
    setup_database()

    # insert_or_update_chat_data({
    #     "client_name": "+91 30238 88888",
    #     "sentiment": "neutral",
    #     "catalog": "True",
    #     "suggestions": "No",
    #     "last_reply": "5-6 din bs",
    #     "list_of_convo": [
    #         {"client_message": "delivery ka kya seen hai", "reply": "5-6 din bs"}
    #     ]
    # })

    # insert_or_update_chat_data({
    #     "client_name": "+91 30238 88888",
    #     "sentiment": "positive",
    #     "catalog": "False",
    #     "suggestions": "give more options",
    #     "last_reply": "ok",
    #     "list_of_convo": [
    #         {"client_message": "ok", "reply": "thanks for the order!"}
    #     ]
    # })


    # print(get_chat_data_by_client("+91 83029 07895"))
    #delete_client_data("+91 83028 07895")
    # export_to_csv()
    print("main func called")
