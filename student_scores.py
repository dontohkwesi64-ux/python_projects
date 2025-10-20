students = input("Enter student names separated by commas: ").split(",")
scores = list(map(int, input("Enter corresponding scores separated by commas: ").split(",")))

def add_scores(students, scores):
    return [f"{student} scored {score}" for student, score in zip(students, scores)]

def average(scores):
    return sum(scores) / len(scores)

def highest_scorer(students, scores):
    max_score = max(scores)
    index = scores.index(max_score)
    return students[index], max_score

def lowest_scorer(students, scores):
    min_score = min(scores)
    index = scores.index(min_score)
    return students[index], min_score

results = add_scores(students, scores)
print("\nStudent Results:")
for line in results:
    print(line)

print(f"\nAverage score: {average(scores):.2f}")

student, score = highest_scorer(students, scores)
print(f"Highest scorer: {student} with {score}")

student, score = lowest_scorer(students, scores)
print(f"Lowest scorer: {student} with {score}")
