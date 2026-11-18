# 성적 CSV 검사기 (load_scores)

## ① 무엇을 하나요 (What)
성적 CSV를 읽어 유효한 `(이름, 점수)` 목록과 제외한 줄의 이유를 반환합니다.

## ② 왜 만들었나요 (Why)
실제 CSV에는 빈 이름, 잘못된 점수, 열 개수 오류와 빈 줄이 섞일 수 있습니다.
한 줄의 오류 때문에 전체 작업을 중단하거나 잘못된 점수를 통과시키지 않도록, 유효한 데이터와 제외 기록을 분리하려고 만들었습니다.
동명이인은 구별할 수 없으므로 이름이 중복되어도 데이터를 삭제하지 않습니다.

## ③ 어떻게 쓰나요 (How)
Python 3.10 이상이 필요합니다. 파일을 받은 뒤 **저장소 폴더에서** 다음을 실행합니다.

```bash
python -m pip install pytest pytest-cov
python load_scores.py scores.csv
python load_scores.py weird.csv
```

`load_scores(path)`는 `(kept, skipped)`를 반환합니다. `kept`는 `(이름, 정수 점수)` 목록이고, `skipped`는 `(줄 번호, 원본 줄, 이유)` 목록입니다. 점수는 0~100 범위이며, 파일이 없으면 `FileNotFoundError`가 발생합니다.

## ④ 어떻게 테스트하나요
```bash
python -m pytest test_load_scores.py -q
python -m pytest test_ai_A.py -q
python -m pytest test_ai_B.py -q
python -m pytest test_load_scores.py --cov=load_scores --cov-report=term-missing -q
```

검증한 출력(2026-11-18, Python 3.13):
```text
10 passed
9 passed
11 passed
load_scores.py   45 Stmts   9 Miss   80% Cover   Missing 77-86
```

함정 실험은 의도적으로 실패하는 코드가 들어 있어 별도로 실행해야 합니다.
```bash
python -m pytest test_ai_bug.py -q
# 2 failed, 1 passed: 구현 버그가 검출됨
```

## ⑤ 파일 구성
| 파일 | 하는 일 |
| --- | --- |
| `load_scores.py` | 배포받은 CSV 파서 (수정하지 않음) |
| `scores.csv`, `empty.csv`, `weird.csv` | 제공된 검증 입력 |
| `test_load_scores.py` | 명세 기반 8개 케이스 + 구현 확인 뒤 추가 2개 테스트 |
| `test_ai_A.py` | AI A: 코드 전체를 보고 작성한 테스트 (수정 없이 보존) |
| `test_ai_B.py` | AI B: 명세만 보고 작성한 테스트 (수정 없이 보존) |
| `bug3_logic.py`, `test_ai_bug.py` | 최대값 탐색의 기존 버그와 이를 찾는 테스트 |
| `prompts.txt` | 수업 배포 A/B/함정 프롬프트 |
| `LICENSE` | MIT License |
| `worksheets/` | 제출용 워크시트 6장 (별도 압축본에 포함) |

## ⑥ 만든 사람 · AI를 어디에 썼는지
- 만든 사람: **[학번 / 이름 입력]**
- AI를 쓴 곳: 테스트 초안 A/B 및 테스트 코드 구성, README 초안, 워크시트 정리
- 내가 직접 판단한 것: **[본인이 실제로 수행한 명세 검토·테스트 결과 검토 내용을 작성]**
- 커밋 표기: `Assisted-by: ChatGPT (OpenAI)`

## 라이선스
MIT License (`LICENSE` 참조). 배포 전 저작권자 이름을 확인해 주세요.
