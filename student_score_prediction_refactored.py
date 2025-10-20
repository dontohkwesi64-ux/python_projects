# student_score_prediction_refactored.py
from datetime import datetime
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Step 1: Collect input
names = input("Enter student names separated by commas: ").split(",")
hours = list(map(float, input(f"Enter hours studied for {len(names)} students separated by commas: ").split(",")))

# Step 2: Train simple linear regression model
X = [[h] for h in hours]  # features
y = hours  # using hours as proxy for score for demonstration
model = LinearRegression()
model.fit(X, y)

# Step 3: Predict scores
predicted = [model.predict([[h]])[0] for h in hours]  # fixed deprecation warning

# Step 4: Define grading function
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

# Step 5: Sort by predicted score
combined = list(zip(names, predicted))
combined.sort(key=lambda x: x[1], reverse=True)

# Step 6: Display rankings
output = []
output.append("\nStudent Rankings:")
for i, (name, score) in enumerate(combined, start=1):
    grade, remark = get_grade(score)
    line = f"{i}. {name.strip()} — {score:.2f} ({grade}, {remark})"
    print(line)
    output.append(line)

# Step 7: Compute stats
average_score = sum(predicted) / len(predicted)
highest_score = max(combined, key=lambda x: x[1])
lowest_score = min(combined, key=lambda x: x[1])

summary = f"""
Average predicted score: {average_score:.2f}
Highest predicted scorer: {highest_score[0].strip()} with {highest_score[1]:.2f}
Lowest predicted scorer: {lowest_score[0].strip()} with {lowest_score[1]:.2f}
"""
print(summary)
output.append(summary)

# Step 8: Save results to file
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("predicted_student_results.txt", "a", encoding="utf-8") as f:
    f.write(f"\n{'='*60}\nResults recorded on: {timestamp}\n")
    f.write("\n".join(output))
    f.write("\n")

print(f"Results successfully appended to predicted_student_results.txt")

# Step 9: Plot predicted scores
plt.figure(figsize=(10,6))
plt.bar([n.strip() for n in names], predicted, color='skyblue')
plt.xlabel("Students")
plt.ylabel("Predicted Scores")
plt.title("Predicted Student Scores based on Hours Studied")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
