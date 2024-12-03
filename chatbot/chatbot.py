import csv
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os

# Function to load responses from a CSV file
def load_responses(filename):
    responses = {}
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                responses[row["key"].lower()] = row["response"]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load responses: {e}")
    return responses

# Function to generate chatbot responses
def chatbot_response(user_input, responses):
    for key in responses.keys():
        if key in user_input.lower():
            return responses[key]
    return "Sorry, I don't understand that."

# Function to handle user input in the GUI
def handle_user_input():
    user_input = user_input_field.get()
    if user_input.lower() == "exit":
        root.destroy()
    else:
        response = chatbot_response(user_input, responses)
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f"You: {user_input}\n")
        chat_area.insert(tk.END, f"Chatbot: {response}\n\n")
        chat_area.config(state=tk.DISABLED)
        user_input_field.delete(0, tk.END)

# Function to select a CSV file dynamically
def select_csv_file():
    global responses
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")],
        initialdir=os.getcwd()
    )
    if file_path:
        responses = load_responses(file_path)
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Responses loaded successfully!\n\n")
        chat_area.config(state=tk.DISABLED)
    else:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "No file selected. Using default responses.\n\n")
        chat_area.config(state=tk.DISABLED)

# Default responses if no CSV is loaded
default_responses = {
    "hello": "Hi there! How can I assist you?",
    "weather": "The weather is great today!",
    "goodbye": "Goodbye! Have a great day!",
}

# Initialize responses dictionary
responses = default_responses

# Create the main application window
root = tk.Tk()
root.title("Universal Chatbot")

# Chat area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# User input field
user_input_field = tk.Entry(root, width=40)
user_input_field.grid(row=1, column=0, padx=10, pady=10)

# Send button
send_button = tk.Button(root, text="Send", command=handle_user_input)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Load CSV button
load_csv_button = tk.Button(root, text="Load Responses", command=select_csv_file)
load_csv_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
