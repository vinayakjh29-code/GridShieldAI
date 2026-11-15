import os
import joblib
import pandas as pd


def test_electrical_ai():
    model_path = os.path.join("models", "electrical_model.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run src/train_electrical_model.py first."
        )

    # Load trained Electrical AI model
    loaded = joblib.load(model_path)

    # Handle whether saved directly as model or inside a dictionary
    if isinstance(loaded, dict) and "model" in loaded:
        model = loaded["model"]
    else:
        model = loaded

    # Sample test readings for all 5 electrical conditions
    test_samples = [
        {
            "expected": "NORMAL",
            "voltage_kv": 11.0,
            "current_a": 285.0,
            "frequency_hz": 50.0,
            "power_mw": 5.43,
            "load_percent": 75.0,
            "transformer_temp_c": 62.0,
        },
        {
            "expected": "OVERLOAD",
            "voltage_kv": 10.7,
            "current_a": 455.0,
            "frequency_hz": 49.95,
            "power_mw": 8.43,
            "load_percent": 122.0,
            "transformer_temp_c": 96.0,
        },
        {
            "expected": "VOLTAGE_DIP",
            "voltage_kv": 8.9,
            "current_a": 300.0,
            "frequency_hz": 49.98,
            "power_mw": 4.62,
            "load_percent": 80.0,
            "transformer_temp_c": 65.0,
        },
        {
            "expected": "FREQUENCY_DEVIATION",
            "voltage_kv": 10.95,
            "current_a": 290.0,
            "frequency_hz": 48.0,
            "power_mw": 5.50,
            "load_percent": 76.0,
            "transformer_temp_c": 63.0,
        },
        {
            "expected": "TRANSFORMER_OVERHEATING",
            "voltage_kv": 11.0,
            "current_a": 310.0,
            "frequency_hz": 50.0,
            "power_mw": 5.91,
            "load_percent": 82.0,
            "transformer_temp_c": 95.0,
        },
    ]

    feature_columns = [
        "voltage_kv",
        "current_a",
        "frequency_hz",
        "power_mw",
        "load_percent",
        "transformer_temp_c",
    ]

    df_test = pd.DataFrame(test_samples)
    X_test = df_test[feature_columns]

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None

    print("=" * 65)
    print("GRIDSHIELD AI - ELECTRICAL AI MODEL PREDICTION TEST")
    print("=" * 65)

    for i, row in df_test.iterrows():
        pred = predictions[i]
        conf_str = ""
        if probabilities is not None:
            confidence = max(probabilities[i]) * 100
            conf_str = f" | Confidence: {confidence:.1f}%"

        status = "PASS" if pred == row["expected"] else "CHECK"
        print(
            f"[{status}] Expected: {row['expected']:<24} -> Predicted: {pred:<24}{conf_str}"
        )

    print("=" * 65)


if __name__ == "__main__":
    test_electrical_ai()
    