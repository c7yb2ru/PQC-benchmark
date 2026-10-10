
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pqc-benchmark-lab\\benchmark_results.csv")

operations = {
    "keygen_mean_ms": "Key Generation",
    "encapsulation_mean_ms": "Encapsulation",
    "decapsulation_mean_ms": "Decapsulation",
}

for column, title in operations.items():
    plt.figure()
    plt.bar(df["algorithm"], df[column])
    plt.title(f"ML-KEM {title} Benchmark")
    plt.ylabel("Mean execution time (ms)")
    plt.xlabel("Algorithm")
    plt.tight_layout()
    plt.savefig(f"{column}.png", dpi=200)
    plt.close()

print("그래프 3개 저장 완료")
