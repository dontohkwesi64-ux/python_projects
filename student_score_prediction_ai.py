# student_score_prediction_ai.py
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os
import sys
import random

MODEL_FILE = "student_score_model.pkl"
DATA_FILE = "historical_scores.csv"

# Step 1: Grading function
def grade(score):
    if score >= 90:
        return "A", "Excellent"
    elif score >= 80:
        return "B", "Very Good"
    elif score >= 70:
        return "C", "Good"
    elif score >= 60:
        return "D", "Needs Improvement"
    else:
        return "F", "Fail"

# Step 2: Collect student data
def collect_student_data():
    names = input("Enter student names separated by commas: ").split(",")
    hours = list(map(float, input(f"Enter hours studied for {len(names)} students separated by commas: ").split(",")))
    return names, hours

# Step 3: Auto-generate historical data
def create_historical_data_auto(num_students=20):
    historical_names = [f"Student{i+1}" for i in range(num_students)]
    historical_hours = [random.randint(10, 20) for _ in range(num_students)]
    historical_scores = [h * random.uniform(4.5, 5.0) for h in historical_hours]  # approximate linear relationship
    df = pd.DataFrame({
        "name": historical_names,
        "hours": historical_hours,
        "score": historical_scores
    })
    try:
        df.to_csv(DATA_FILE, index=False)
        print(f"\nAuto-generated historical data saved to {DATA_FILE}")
    except PermissionError:
        print(f"\nPermission denied. Auto-generated historical data not saved to {DATA_FILE}")
    return df

# Step 4: Train or load model
def get_trained_model():
    if os.path.exists(MODEL_FILE):
        try:
            model = joblib.load(MODEL_FILE)
            return model
        except PermissionError:
            print(f"Permission denied when trying to read {MODEL_FILE}. Model will be trained anew.")

    # Try reading historical CSV
    try:
        data = pd.read_csv(DATA_FILE)
    except (FileNotFoundError, PermissionError):
        print(f"Cannot read {DATA_FILE}. Auto-generating historical data...")
        data = create_historical_data_auto()

    X = data[["hours"]]
    y = data["score"]
    model = LinearRegression()
    model.fit(X, y)

    try:
        joblib.dump(model, MODEL_FILE)
    except PermissionError:
        print(f"Permission denied when trying to save {MODEL_FILE}. Model not saved.")
    return model

# Step 5: Predict scores
def predict_scores(model, hours):
    X_new = [[h] for h in hours]
    predicted = [float(model.predict([x])[0]) for x in X_new]
    return predicted

# Step 6: Display results
def display_results(names, predicted_scores):
    output = []
    print("\nPredicted Student Scores:")
    for i, (name, score) in enumerate(zip(names, predicted_scores), start=1):
        g, remark = grade(score)
        line = f"{i}. {name.strip()} — {score:.2f} ({g}, {remark})"
        print(line)
        output.append(line)

    avg_score = sum(predicted_scores) / len(predicted_scores)
    highest_score = max(predicted_scores)
    lowest_score = min(predicted_scores)
    summary = (
        f"\nAverage predicted score: {avg_score:.2f}\n"
        f"Highest predicted scorer: {names[predicted_scores.index(highest_score)]} with {highest_score:.2f}\n"
        f"Lowest predicted scorer: {names[predicted_scores.index(lowest_score)]} with {lowest_score:.2f}"
    )
    print(summary)
    output.append(summary)
    return output

# Step 7: Save results
def save_results_to_file(output, filename="predicted_student_results.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*60}\nResults recorded on: {timestamp}\n")
            f.write("\n".join(output))
            f.write("\n")
        print(f"\nResults successfully appended to {filename}")
    except PermissionError:
        print(f"Permission denied when trying to save {filename}. Results not saved.")

# Main program
def main():
    names, hours = collect_student_data()
    model = get_trained_model()
    predicted_scores = predict_scores(model, hours)
    output = display_results(names, predicted_scores)
    save_results_to_file(output)

if __name__ == "__main__":
    main()
