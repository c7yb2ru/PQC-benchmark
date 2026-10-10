
import time
import statistics
import csv

from cryptography.hazmat.primitives.asymmetric.mlkem import (
    MLKEM768PrivateKey,
    MLKEM1024PrivateKey,
)


def benchmark(name, private_key_class, iterations=500):
    keygen_times = []
    encapsulation_times = []
    decapsulation_times = []

    # 워밍업: 측정 결과에서 제외
    for _ in range(10):
        private_key = private_key_class.generate()
        public_key = private_key.public_key()
        secret, ciphertext = public_key.encapsulate()
        recovered = private_key.decapsulate(ciphertext)
        assert secret == recovered

    # 본 실험
    for _ in range(iterations):
        start = time.perf_counter_ns()
        private_key = private_key_class.generate()
        keygen_times.append(time.perf_counter_ns() - start)

        public_key = private_key.public_key()

        start = time.perf_counter_ns()
        secret, ciphertext = public_key.encapsulate()
        encapsulation_times.append(time.perf_counter_ns() - start)

        start = time.perf_counter_ns()
        recovered = private_key.decapsulate(ciphertext)
        decapsulation_times.append(time.perf_counter_ns() - start)

        assert secret == recovered

    def summarize(values):
        # 나노초를 밀리초로 변환
        values_ms = [value / 1_000_000 for value in values]
        return (
            round(statistics.mean(values_ms), 6),
            round(statistics.median(values_ms), 6),
        )

    public_key = private_key_class.generate().public_key()
    secret, ciphertext = public_key.encapsulate()

    results = {
        "algorithm": name,
        "iterations": iterations,
        "public_key_bytes": len(public_key.public_bytes_raw()),
        "ciphertext_bytes": len(ciphertext),
        "secret_bytes": len(secret),
    }

    for operation, values in [
        ("keygen", keygen_times),
        ("encapsulation", encapsulation_times),
        ("decapsulation", decapsulation_times),
    ]:
        mean_ms, median_ms = summarize(values)
        results[f"{operation}_mean_ms"] = mean_ms
        results[f"{operation}_median_ms"] = median_ms

    return results


def main():
    configurations = [
        ("ML-KEM-768", MLKEM768PrivateKey),
        ("ML-KEM-1024", MLKEM1024PrivateKey),
    ]

    results = []

    for name, key_class in configurations:
        result = benchmark(name, key_class)
        results.append(result)

        print(f"\n[{name}]")
        for key, value in result.items():
            print(f"{key}: {value}")

    with open("benchmark_results.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\n결과 저장 완료: benchmark_results.csv")


if __name__ == "__main__":
    main()
