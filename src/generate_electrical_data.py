from pathlib import Path
import math
import random

import pandas as pd


# SYNTHETIC ACADEMIC DATA ONLY.
# These readings are not measurements from real electrical equipment.

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "electrical_data.csv"

SAMPLES_PER_CLASS = 500
rng = random.Random(42)

LABELS = [
    "NORMAL",
    "OVERLOAD",
    "VOLTAGE_DIP",
    "FREQUENCY_DEVIATION",
    "TRANSFORMER_OVERHEATING",
]


def generate_dataset():
    rows = []

    for label in LABELS:
        for _ in range(SAMPLES_PER_CLASS):

            # Match the normal ranges in the current app.py simulator.
            voltage = rng.uniform(10.9, 11.1)
            current = rng.uniform(260, 310)
            frequency = rng.uniform(49.95, 50.05)
            load = rng.uniform(65, 85)
            temperature = rng.uniform(55, 68)

            if label == "OVERLOAD":
                current = rng.uniform(430, 480)
                load = rng.uniform(115, 130)
                temperature = rng.uniform(90, 105)

            elif label == "VOLTAGE_DIP":
                voltage = rng.uniform(8.5, 9.5)

            elif label == "FREQUENCY_DEVIATION":
                frequency = rng.uniform(47.5, 48.5)

            elif label == "TRANSFORMER_OVERHEATING":
                # Separate overheating example without an overload.
                temperature = rng.uniform(90, 105)

            # Match app.py's simplified power calculation.
            # Active power here assumes a power factor of 1.
            power = voltage * current * math.sqrt(3) / 1000

            rows.append({
                "voltage_kv": round(voltage, 2),
                "current_a": round(current, 2),
                "frequency_hz": round(frequency, 2),
                "power_mw": round(power, 2),
                "load_percent": round(load, 2),
                "transformer_temp_c": round(temperature, 2),
                "label": label,
            })

    dataset = pd.DataFrame(rows)

    # Shuffle the examples so that classes are mixed.
    return dataset.sample(frac=1, random_state=42).reset_index(drop=True)


def main():
    if DATASET_PATH.exists():
        print("STOP: electrical_data.csv already exists.")
        print("No existing file was changed.")
        return

    dataset = generate_dataset()

    # Mode "x" prevents overwriting an existing dataset.
    with DATASET_PATH.open("x", encoding="utf-8", newline="") as file:
        dataset.to_csv(file, index=False)

    print("\nGRIDSHIELD AI - SYNTHETIC ELECTRICAL DATASET")
    print("Dataset created successfully!")
    print(f"Total rows: {len(dataset)}")
    print("\nExamples per class:")
    print(dataset["label"].value_counts().to_string())
    print(f"\nSaved at: {DATASET_PATH}")
    print("\nAcademic simulation only. Not real-world validation.")


if __name__ == "__main__":
    main()
