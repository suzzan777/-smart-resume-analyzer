import json
import os


def load_evaluation_pairs(file_path="data/evaluation_pairs.json"):
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def label_from_score(score):
    if score >= 70:
        return "high"
    elif score >= 40:
        return "medium"
    return "low"


def compute_classification_metrics(pairs):
    """
    Simple evaluation:
    - 'high' is treated as positive
    - 'medium' and 'low' are treated as non-high
    """
    tp = fp = fn = tn = 0

    detailed_results = []

    for pair in pairs:
        expected = pair.get("expected_label", "low").lower()
        predicted_score = pair.get("predicted_score", 0)
        predicted = label_from_score(predicted_score)

        expected_positive = expected == "high"
        predicted_positive = predicted == "high"

        if predicted_positive and expected_positive:
            tp += 1
        elif predicted_positive and not expected_positive:
            fp += 1
        elif not predicted_positive and expected_positive:
            fn += 1
        else:
            tn += 1

        detailed_results.append({
            "resume_name": pair.get("resume_name", "Unknown"),
            "expected_label": expected,
            "predicted_score": predicted_score,
            "predicted_label": predicted
        })

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / len(pairs) if pairs else 0

    return {
        "total_pairs": len(pairs),
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "true_negative": tn,
        "precision": round(precision * 100, 2),
        "recall": round(recall * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "accuracy": round(accuracy * 100, 2),
        "details": detailed_results
    }


def qualitative_summary(metrics):
    comments = []

    if metrics["precision"] >= 70:
        comments.append("The system shows good precision when identifying strong candidate matches.")
    else:
        comments.append("The system may be over-predicting strong matches and needs better filtering.")

    if metrics["recall"] >= 70:
        comments.append("The system is recovering a good proportion of genuinely strong matches.")
    else:
        comments.append("The system may be missing some relevant candidates and needs better extraction or scoring.")

    if metrics["f1_score"] >= 70:
        comments.append("Overall balance between precision and recall is strong.")
    elif metrics["f1_score"] >= 50:
        comments.append("Overall balance is moderate, but there is still room for improvement.")
    else:
        comments.append("The balance between precision and recall is weak and requires refinement.")

    comments.append("Results should be interpreted as decision-support outputs rather than automated hiring decisions.")
    return comments