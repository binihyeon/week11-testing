"""명세에서 먼저 고른 여덟 입력을 검증한다 (정상 3, 예외 2, 경계 3)."""
import pytest
from load_scores import load_scores


def write_csv(tmp_path, text):
    path = tmp_path / "case.csv"
    path.write_text(text, encoding="utf-8")
    return path


def test_normal_file_keeps_five_and_logs_five():
    kept, skipped = load_scores("scores.csv")
    assert kept == [("김하나", 88), ("최,네번", 77), ("김하나", 91), ("윤보람", 64), ("서한별", 95)]
    assert len(skipped) == 5


def test_blank_line_is_ignored_without_skip_record(tmp_path):
    path = write_csv(tmp_path, "name,score\n가영,80\n\n나영,90\n")
    assert load_scores(path) == ([("가영", 80), ("나영", 90)], [])


def test_comma_in_quoted_name_is_one_column(tmp_path):
    path = write_csv(tmp_path, 'name,score\n"김,민수",70\n')
    assert load_scores(path) == ([("김,민수", 70)], [])


def test_missing_file_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "not_here.csv")


def test_header_only_returns_two_empty_lists():
    assert load_scores("empty.csv") == ([], [])


@pytest.mark.parametrize("score,valid", [(0, True), (100, True), (101, False)])
def test_boundary_scores_zero_hundred_one_hundred_one(tmp_path, score, valid):
    path = write_csv(tmp_path, f"name,score\n경계,{score}\n")
    kept, skipped = load_scores(path)
    assert kept == ([("경계", score)] if valid else [])
    assert skipped == ([] if valid else [(2, f"경계,{score}", "점수가 0~100 밖")])


# 코드를 확인한 뒤 추가한 분기 검증. 위 여덟 설계 케이스와 구별한다.
def test_open_box_invalid_name_and_noninteger(tmp_path):
    path = write_csv(tmp_path, "name,score\n,90\n철수,abc\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert [x[2] for x in skipped] == ["이름이 비어 있음", "점수가 정수가 아님"]


def test_open_box_whitespace_and_duplicate_names(tmp_path):
    path = write_csv(tmp_path, "name,score\n 철수 , 77 \n철수,88\n")
    assert load_scores(path) == ([("철수", 77), ("철수", 88)], [])
