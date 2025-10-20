
# student_ranking.py
from datetime import datetime

# Step 1: Collect input
names = input("Enter student names separated by commas: ").split(",")
scores = list(map(int, input("Enter corresponding scores separated by commas: ").split(",")))

# Step 2: Combine and sort students by score
combined = list(zip(names, scores))
combined.sort(key=lambda x: x[1], reverse=True)

# Step 3: Define grading function
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

# Step 4: Display rankings and build output text
output = []
output.append("\nStudent Rankings:")
for i, (name, score) in enumerate(combined, start=1):
    grade, remark = get_grade(score)
    line = f"{i}. {name.strip()} — {score} ({grade}, {remark})"
    print(line)
    output.append(line)

# Step 5: Compute stats
average_score = sum(scores) / len(scores)
highest_score = max(combined, key=lambda x: x[1])
lowest_score = min(combined, key=lambda x: x[1])

summary = f"""
Average score: {average_score:.2f}
Highest scorer: {highest_score[0].strip()} with {highest_score[1]}
Lowest scorer: {lowest_score[0].strip()} with {lowest_score[1]}
"""
print(summary)
output.append(summary)

# Step 6: Append results to file
with open("student_results.txt", "a", encoding="utf-8") as f:
    f.write("\n" + "="*60 + "\n")
    f.write(f"Results recorded on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write("\n".join(output))
    f.write("\n\n")


print(f"Results successfully appended to student_results.txt")
