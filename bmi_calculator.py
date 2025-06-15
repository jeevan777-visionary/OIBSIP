
import tkinter as tk
from tkinter import messagebox
import csv
import datetime
import matplotlib.pyplot as plt

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if weight <= 0 or height <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid weight and height.")
        return

    bmi = round(weight / (height ** 2), 2)
    category = get_bmi_category(bmi)

    result_label.config(text=f"BMI: {bmi} ({category})")

    # Save data
    save_bmi_data(weight, height, bmi)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def save_bmi_data(weight, height, bmi):
    with open("bmi_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight, height, bmi])

def view_history():
    try:
        dates = []
        bmis = []
        with open("bmi_data.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                dates.append(row[0])
                bmis.append(float(row[3]))
        if not bmis:
            messagebox.showinfo("History", "No data available.")
            return
        plt.figure(figsize=(10, 5))
        plt.plot(dates, bmis, marker='o')
        plt.xticks(rotation=45)
        plt.title("BMI Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        messagebox.showinfo("History", "No data available.")

# GUI
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x350")

tk.Label(root, text="Enter Weight (kg):", font=("Arial", 12)).pack(pady=5)
weight_entry = tk.Entry(root, font=("Arial", 12))
weight_entry.pack(pady=5)

tk.Label(root, text="Enter Height (m):", font=("Arial", 12)).pack(pady=5)
height_entry = tk.Entry(root, font=("Arial", 12))
height_entry.pack(pady=5)

tk.Button(root, text="Calculate BMI", command=calculate_bmi, font=("Arial", 12)).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
result_label.pack(pady=10)

tk.Button(root, text="View BMI History", command=view_history, font=("Arial", 12)).pack(pady=10)

root.mainloop()
