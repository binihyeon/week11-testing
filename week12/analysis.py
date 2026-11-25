import pandas as pd

def 정제(df):
    """명세에 따라 성적 데이터를 정제하고 단계별 행 수를 출력한다."""
    df = df.copy()
    print("시작:", len(df))
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거:", len(df))
    df = df.drop_duplicates()
    print("중복 제거:", len(df))
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거:", len(df))
    return df

def 반별평균(df):
    return df.groupby("반")["점수"].mean()

if __name__ == "__main__":
    df = 정제(pd.read_csv("scores_2026.csv"))
    print("\n수학 필터:")
    print(df[df["과목"] == "수학"])
    print("\n1반 90점 이상:")
    print(df[(df["반"] == "1반") & (df["점수"] >= 90)])
    print("\n반별 평균:")
    print(df.groupby("반")["점수"].mean())
    print("\n과목 × 반 평균:")
    print(df.groupby(["과목", "반"])["점수"].mean())
    print("\n반별 통계:")
    print(df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2))
    print("\n전체 점수 합:", df["점수"].sum())
    print("반별 점수 합:")
    print(df.groupby("반")["점수"].sum())
