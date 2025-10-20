# student_score_prediction_upgraded.py
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Step 1: Collect input
names = input("Enter student names separated by commas: ").split(",")
hours = list(map(float, input(f"Enter hours studied for {len(names)} students separated by commas: ").split(",")))

# Convert to numpy array for sklearn
X = np.array(hours).reshape(-1, 1)

# Step 2: Train a simple Linear Regression
# Here we use hours as X and make a toy relationship y = 10*X + 10 + random noise
y = np.array([10*h + 10 for h in hours])  # simulate actual scores
model = LinearRegression()
model.fit(X, y)

# Step 3: Predict scores
predicted_scores = model.predict(X)
# Clip predicted scores to a max of 100
predicted_scores = np.clip(predicted_scores, 0, 100)

# Step 4: Assign grades
def get_grade(score):
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

# Step 5: Combine names and scores
combined = list(zip(names, predicted_scores))
combined.sort(key=lambda x: x[1], reverse=True)

# Step 6: Display rankings and build output
output = []
output.append("\nStudent Predicted Rankings:")
for i, (name, score) in enumerate(combined, start=1):
    grade, remark = get_grade(score)
    line = f"{i}. {name.strip()} — {score:.2f} ({grade}, {remark})"
    print(line)
    output.append(line)

# Step 7: Compute stats
average_score = np.mean(predicted_scores)
highest_score = max(combined, key=lambda x: x[1])
lowest_score = min(combined, key=lambda x: x[1])

summary = f"""
Average predicted score: {average_score:.2f}
Highest predicted scorer: {highest_score[0].strip()} with {highest_score[1]:.2f}
Lowest predicted scorer: {lowest_score[0].strip()} with {lowest_score[1]:.2f}
"""
print(summary)
output.append(summary)

# Step 8: Append results to file
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("predicted_student_results.txt", "a", encoding="utf-8") as f:
    f.write(f"\n{'='*60}\nResults recorded on: {timestamp}\n")
    f.write("\n".join(output))
    f.write("\n")

print("Results successfully appended to predicted_student_results.txt")

# Step 9: Plot graph
plt.figure(figsize=(10,6))
plt.scatter(names, predicted_scores, color='blue')
for i, (name, score) in enumerate(combined):
    plt.text(i, score+0.5, f"{score:.1f}", ha='center')
plt.title("Predicted Student Scores Based on Hours Studied")
plt.xlabel("Students")
plt.ylabel("Predicted Score")
plt.xticks(rotation=45)
plt.ylim(0, 105)
plt.grid(True)
plt.tight_layout()
plt.show()
