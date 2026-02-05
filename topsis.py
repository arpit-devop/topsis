import sys
import pandas as pd
import numpy as np


def error(msg):
    print(f"Error: {msg}")
    sys.exit(1)


def main():
    # -----------------------------
    # 1. CHECK NUMBER OF ARGUMENTS
    # -----------------------------
    if len(sys.argv) != 5:
        error("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputFileName>")

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    # -----------------------------
    # 2. READ INPUT FILE
    # -----------------------------
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        error("Input file not found")

    if df.shape[1] < 3:
        error("Input file must contain three or more columns")

    # -----------------------------
    # 3. CHECK NUMERIC COLUMNS
    # -----------------------------
    data = df.iloc[:, 1:]

    if not np.all(data.applymap(np.isreal)):
        error("From 2nd to last columns must contain numeric values only")

    # -----------------------------
    # 4. CHECK WEIGHTS & IMPACTS
    # -----------------------------
    weights = weights.split(",")
    impacts = impacts.split(",")

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        error("Number of weights, impacts and columns must be the same")

    try:
        weights = np.array(weights, dtype=float)
    except ValueError:
        error("Weights must be numeric")

    for imp in impacts:
        if imp not in ["+", "-"]:
            error("Impacts must be either + or -")

    # -----------------------------
    # 5. NORMALIZATION
    # -----------------------------
    norm_data = data / np.sqrt((data ** 2).sum())

    # -----------------------------
    # 6. WEIGHTED NORMALIZATION
    # -----------------------------
    weighted_data = norm_data * weights

    # -----------------------------
    # 7. IDEAL BEST & WORST
    # -----------------------------
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == "+":
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # -----------------------------
    # 8. DISTANCE MEASURES
    # -----------------------------
    d_pos = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # -----------------------------
    # 9. TOPSIS SCORE & RANK
    # -----------------------------
    score = d_neg / (d_pos + d_neg)
    df["Topsis Score"] = score
    df["Rank"] = score.rank(ascending=False).astype(int)

    # -----------------------------
    # 10. SAVE OUTPUT
    # -----------------------------
    df.to_csv(output_file, index=False)
    print("TOPSIS analysis completed successfully.")


if __name__ == "__main__":
    main()
