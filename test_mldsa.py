
import time
import csv
import statistics

from cryptography.hazmat.primitives.asymmetric.mldsa import (
    MLDSA44PrivateKey,
    MLDSA65PrivateKey,
    MLDSA87PrivateKey,
)


MESSAGE = b"PQC Benchmark Lab: ML-DSA digital signature test"
ITERATIONS = 500
WARMUP = 10


def benchmark(name, private_key_class):
    keygen_times = []
    signing_times = []
    verification_times = []

    # 워밍업: 본 실험 결과에서 제외
    for _ in range(WARMUP):
        private_key = private_key_class.generate()
        public_key = private_key.public_key()
        signature = private_key.sign(MESSAGE)
        public_key.verify(signature, MESSAGE)

    # 본 실험
    for _ in range(ITERATIONS):
        # 1. 키 생성 시간
        start = time.perf_counter_ns()
        private_key = private_key_class.generate()
        keygen_times.append(time.perf_counter_ns() - start)

        public_key = private_key.public_key()

        # 2. 전자서명 생성 시간
        start = time.perf_counter_ns()
        signature = private_key.sign(MESSAGE)
        signing_times.append(time.perf_counter_ns() - start)

        # 3. 전자서명 검증 시간
        start = time.perf_counter_ns()
        public_key.verify(signature, MESSAGE)
        verification_times.append(time.perf_counter_ns() - start)

    # 크기 측정용 키와 서명
    private_key = private_key_class.generate()
    public_key = private_key.public_key()
    signature = private_key.sign(MESSAGE)

    def summarize(values):
        values_ms = [v / 1_000_000 for v in values]
        return (
            round(statistics.mean(values_ms), 6),
            round(statistics.median(values_ms), 6),
        )

    result = {
        "algorithm": name,
        "iterations": ITERATIONS,
        "public_key_bytes": len(public_key.public_bytes_raw()),
        "private_seed_bytes": len(private_key.private_bytes_raw()),
        "signature_bytes": len(signature),
        "message_bytes": len(MESSAGE),
    }

    operations = {
        "keygen": keygen_times,
        "signing": signing_times,
        "verification": verification_times,
    }

    for operation, values in operations.items():
        mean_ms, median_ms = summarize(values)
        result[f"{operation}_mean_ms"] = mean_ms
        result[f"{operation}_median_ms"] = median_ms

    return result


def main():
    configurations = [
        ("ML-DSA-44", MLDSA44PrivateKey),
        ("ML-DSA-65", MLDSA65PrivateKey),
        ("ML-DSA-87", MLDSA87PrivateKey),
    ]

    results = []

    for name, key_class in configurations:
        result = benchmark(name, key_class)
        results.append(result)

        print(f"\n[{name}]")
        for key, value in result.items():
            print(f"{key}: {value}")

    with open(
        "mldsa_benchmark_results.csv",
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\n결과 저장 완료: mldsa_benchmark_results.csv")


if __name__ == "__main__":
    main()
