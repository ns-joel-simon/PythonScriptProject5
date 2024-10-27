"""1. Write a Python Script to hit a REST API and get the result - json.
2. Use tkiner lib to display the result
3. Hit the api every 3 min & update the result in the GUI
4. Log & JSon file as usual."""

import tkinter as tk
import requests
import json
import time
import logging
from threading import Thread

# Logging setup
logging.basicConfig(filename="api_log.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Function to fetch data from the REST API
def fetch_api_data():
    url = "https://jsonplaceholder.typicode.com/todos/1"  # Example API URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        data = response.json()

        # Save the response to a JSON file
        with open("api_response.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        # Log the successful API call
        logging.info("Fetched data successfully: %s", data)
        return data

    except requests.RequestException as e:
        logging.error("Error fetching data: %s", e)
        return {"error": "Could not fetch data"}

# Function to update GUI with fetched data
def update_gui():
    data = fetch_api_data()  # Fetch new data
    if "error" in data:
        result_label.config(text="Error: Could not fetch data")
    else:
        result_text = f"ID: {data.get('id')}\nTitle: {data.get('title')}\nCompleted: {data.get('completed')}"
        result_label.config(text=result_text)

    # Schedule the next update in 3 minutes
    root.after(180000, update_gui)

# Tkinter GUI setup
root = tk.Tk()
root.title("API Data Fetcher")
root.geometry("400x200")

# Label to display the API data
result_label = tk.Label(root, text="Fetching data...", font=("Helvetica", 12), justify="left")
result_label.pack(pady=20)

# Start the first update and GUI mainloop
update_gui()
root.mainloop()
