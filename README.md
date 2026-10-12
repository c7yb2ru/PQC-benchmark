# PQC-benchmark

양자내성암호 알고리즘의 실행 시간, 키 및 암호문 크기, 서명 크기를 측정하고 실험 조건에 따른 성능 차이를 분석하는 프로젝트.
Python 기반 ML-KEM 및 ML-DSA 벤치마크를 통해 키 생성·캡슐화·디캡슐화·전자서명·검증 성능과 키 및 데이터 크기를 비교 분석.
---
ML-KEM

공유 비밀값을 안전하게 설정하기 위한 키 캡슐화 메커니즘. 키 생성, 캡슐화, 디캡슐화 시간을 측정한다.

ML-DSA

메시지의 출처와 무결성을 검증하기 위한 전자서명 알고리즘. 키 생성, 서명, 검증 시간을 측정한다.

실험 및 분석

반복 실행, 평균·중앙값 계산, 크기 비교 그래프, 결과 CSV 저장.

---
# Experimental Environment

Python 3.14.5

cryptography 48.0.0

OS: Microsoft Windows 11 Pro

CPU: AMD Ryzen 5 5600X 6-Core Processor
