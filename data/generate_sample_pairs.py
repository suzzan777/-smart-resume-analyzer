import json
import random

labels = ["high", "medium", "low"]

sample_pairs = []

for i in range(1, 21):
    expected = random.choice(labels)

    if expected == "high":
        score = random.randint(65, 95)
    elif expected == "medium":
        score = random.randint(35, 69)
    else:
        score = random.randint(5, 45)

    sample_pairs.append({
        "resume_name": f"candidate_{i}.pdf",
        "expected_label": expected,
        "predicted_score": score
    })

with open("data/evaluation_pairs.json", "w", encoding="utf-8") as f:
    json.dump(sample_pairs, f, indent=2)

print("Sample evaluation_pairs.json generated successfully.")