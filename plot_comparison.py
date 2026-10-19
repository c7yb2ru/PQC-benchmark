
import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. CSV 파일 읽기
# ==========================================

KEM_CSV = r"benchmark_results.csv"
DSA_CSV = r"mldsa_benchmark_results.csv"

OUTPUT_DIR = "graphs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

kem = pd.read_csv(KEM_CSV)
dsa = pd.read_csv(DSA_CSV)

# 한글이 포함된 그래프 제목이 필요하면
# Windows 환경에서 아래 설정을 사용할 수 있음.
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


def save_bar_chart(
    labels,
    series,
    title,
    ylabel,
    filename,
    rotation=0,
):
    """여러 데이터 계열을 비교하는 막대 그래프 생성"""

    fig, ax = plt.subplots(figsize=(10, 6))

    x = list(range(len(labels)))
    n_series = len(series)
    width = 0.8 / n_series

    for i, (legend, values) in enumerate(series.items()):
        positions = [
            pos - 0.4 + width / 2 + i * width
            for pos in x
        ]

        bars = ax.bar(
            positions,
            values,
            width=width,
            label=legend,
        )

        ax.bar_label(
            bars,
            fmt="%.4f",
            padding=3,
            fontsize=8,
        )

    ax.set_title(title, fontsize=14)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=rotation)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(
        os.path.join(OUTPUT_DIR, filename),
        dpi=200,
        bbox_inches="tight",
    )
    plt.close(fig)

    print(f"그래프 저장: {filename}")


# ==========================================
# 2. 키 생성 시간 비교
# ==========================================

all_algorithms = pd.concat(
    [
        kem[["algorithm", "keygen_mean_ms"]],
        dsa[["algorithm", "keygen_mean_ms"]],
    ],
    ignore_index=True,
)

save_bar_chart(
    labels=all_algorithms["algorithm"].tolist(),
    series={
        "Key Generation": all_algorithms[
            "keygen_mean_ms"
        ].tolist()
    },
    title="ML-KEM vs ML-DSA: Key Generation",
    ylabel="Mean execution time (ms)",
    filename="01_key_generation.png",
    rotation=15,
)


# ==========================================
# 3. ML-KEM 캡슐화 및 디캡슐화
# ==========================================

save_bar_chart(
    labels=kem["algorithm"].tolist(),
    series={
        "Encapsulation": kem[
            "encapsulation_mean_ms"
        ].tolist(),
        "Decapsulation": kem[
            "decapsulation_mean_ms"
        ].tolist(),
    },
    title="ML-KEM: Encapsulation vs Decapsulation",
    ylabel="Mean execution time (ms)",
    filename="02_mlkem_operations.png",
)


# ==========================================
# 4. ML-DSA 서명 및 검증
# ==========================================

save_bar_chart(
    labels=dsa["algorithm"].tolist(),
    series={
        "Signing": dsa[
            "signing_mean_ms"
        ].tolist(),
        "Verification": dsa[
            "verification_mean_ms"
        ].tolist(),
    },
    title="ML-DSA: Signing vs Verification",
    ylabel="Mean execution time (ms)",
    filename="03_mldsa_operations.png",
)


# ==========================================
# 5. 공개키 크기 비교
# ==========================================

all_public_keys = pd.concat(
    [
        kem[["algorithm", "public_key_bytes"]],
        dsa[["algorithm", "public_key_bytes"]],
    ],
    ignore_index=True,
)

save_bar_chart(
    labels=all_public_keys["algorithm"].tolist(),
    series={
        "Public Key": all_public_keys[
            "public_key_bytes"
        ].tolist()
    },
    title="ML-KEM vs ML-DSA: Public Key Size",
    ylabel="Size (bytes)",
    filename="04_public_key_size.png",
    rotation=15,
)


# ==========================================
# 6. 암호문 및 서명 크기 비교
# ==========================================

payload_labels = (
    kem["algorithm"].tolist()
    + dsa["algorithm"].tolist()
)

payload_sizes = (
    kem["ciphertext_bytes"].tolist()
    + dsa["signature_bytes"].tolist()
)

payload_types = (
    ["Ciphertext"] * len(kem)
    + ["Signature"] * len(dsa)
)

# 종류별로 분리해서 표시
fig, ax = plt.subplots(figsize=(10, 6))

x = list(range(len(payload_labels)))

for i, (label, size, kind) in enumerate(
    zip(payload_labels, payload_sizes, payload_types)
):
    ax.bar(i, size, label=kind if kind not in [
        t.get_label() for t in ax.containers
    ] else None)

    ax.text(
        i,
        size,
        str(size),
        ha="center",
        va="bottom",
        fontsize=9,
    )

ax.set_title("ML-KEM Ciphertext vs ML-DSA Signature Size")
ax.set_ylabel("Size (bytes)")
ax.set_xticks(x)
ax.set_xticklabels(payload_labels, rotation=15)

from matplotlib.patches import Patch

ax.legend(handles=[
    Patch(label="Ciphertext"),
    Patch(label="Signature"),
])

ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig(
    os.path.join(OUTPUT_DIR, "05_ciphertext_signature_size.png"),
    dpi=200,
    bbox_inches="tight",
)
plt.close(fig)

print("그래프 저장: 05_ciphertext_signature_size.png")

print("\n모든 그래프 생성 완료!")
print(f"저장 위치: {os.path.abspath(OUTPUT_DIR)}")
