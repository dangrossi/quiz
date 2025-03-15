import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
import json
import random

# Create the main window
window = tk.Tk()
window.title("Quiz")

# Create labels for the question and image
question_label = tk.Label(window, text="", wraplength=400)
question_label.pack(pady=10)

image_label = tk.Label(window)
image_label.pack()

# Create a frame for the answer buttons
answers_frame = tk.Frame(window)
answers_frame.pack()

# Create the answer buttons
answer_buttons = []
for i in range(4):
    button = tk.Button(answers_frame, text="", width=60, command=lambda idx=i: check_answer(idx))
    answer_buttons.append(button)
    button.pack(pady=5)

# Create labels for the score and remaining time
score_label = tk.Label(window, text="Score: 0")
score_label.pack(pady=10)

time_label = tk.Label(window, text="Remaining time: 100 seconds")
time_label.pack(pady=5)

# Initialize variables for time and score
remaining_time = tk.IntVar()
timer_id = None
start_time = 0
total_time = 0  # Variable for total time

current_question = 0
score = 0
questions = []
first_run = 0

# Function to load a question
def load_question():
    global current_question, remaining_time, timer_id, start_time
    if current_question < len(questions):
        question = questions[current_question]
        question_label.config(text=question["question"])
        if question["image"]:
            try:
                image = Image.open(question["image"])
                image = image.resize((300, 300), Image.BOX)
                image_tk = ImageTk.PhotoImage(image)
                image_label.config(image=image_tk)
                image_label.image = image_tk
            except FileNotFoundError:
                messagebox.showerror("Error", f"Image not found: {question['image']}")
                image_label.config(image="")
        else:
            image_label.config(image="")
        for i, answer in enumerate(question["answers"]):
            answer_buttons[i].config(text=answer)
        remaining_time.set(100)
        time_label.config(text=f"Remaining time: {remaining_time.get()} seconds")
        if timer_id:
            window.after_cancel(timer_id)
        timer_id = window.after(1000, update_time)
        start_time = datetime.now()
    else:
        show_results()

# Function to check the selected answer
def check_answer(answer_index):
    global score, current_question, first_run, timer_id, start_time, total_time
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None
    end_time = datetime.now()
    time_taken = (end_time - start_time).seconds
    total_time += time_taken  # Update total time
    question = questions[current_question]
    with open("quiz_log.txt", "a") as file:
        if first_run == 0:
            first_run = 1
            dt = datetime.now()
            current_date_time = dt.strftime("%d-%m-%Y %H:%M:%S")
            file.write(f"Quiz of {current_date_time}\n")
        file.write(f"Question: {question['question']}\n")
        file.write(f"Answers: {question['answers']}")
        file.write(f"    User answer: " + question["answers"][answer_index] + "\n")
        file.write(f"Correct answer:" + question["correct_answer"] + "\n")
        file.write(f"Time taken: {time_taken} seconds\n")
        file.write("-" * 20 + "\n")
    if question["answers"][answer_index] == question["correct_answer"]:
        score += 1
        score_label.config(text=f"Score: {score}")
        messagebox.showinfo("Correct", "Correct answer!")
    else:
        messagebox.showerror("Wrong", "Wrong answer.")
    current_question += 1
    load_question()

# Function to show the final results
def show_results():
    messagebox.showinfo("Results", f"You scored {score} points out of {len(questions)}.\nTotal time taken: {total_time} seconds.") #print total time
    with open("quiz_log.txt", "a") as file:
        file.write(f"Scora : Final  {score} score on {len(questions)}.\nTotale time : {total_time} seconds.") #Stampa del tempo totale

    window.destroy()

# Function to update the remaining time
def update_time():
    global remaining_time, current_question, timer_id
    if remaining_time.get() > 0 and current_question < len(questions):
        remaining_time.set(remaining_time.get() - 1)
        time_label.config(text=f"Remaining time: {remaining_time.get()} seconds")
        timer_id = window.after(1000, update_time)
    elif remaining_time.get() == 0:
        messagebox.showerror("Time expired", "Time expired to answer.")
        current_question += 1
        load_question()
        timer_id = None

# Load questions from JSON file
try:
    with open("questions1.json", "r") as f:
        questions = json.load(f)
    random.shuffle(questions)
    load_question()
except FileNotFoundError:
    messagebox.showerror("Error", "Questions.json file not found.")
except json.JSONDecodeError:
    messagebox.showerror("Error", "Questions.json file corrupted.")

window.mainloop()
