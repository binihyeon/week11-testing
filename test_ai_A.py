"""AI A: 코드 전체를 입력으로 받아 작성한 테스트. 원본 결과 보존."""
from pathlib import Path
import pytest
from load_scores import load_scores


def make_file(tmp_path, content):
    p = tmp_path / 'data.csv'
    p.write_text(content, encoding='utf-8')
    return p


def test_normal_records(tmp_path):
    p = make_file(tmp_path, 'name,score\nA,30\nB,90\n')
    assert load_scores(p) == ([('A', 30), ('B', 90)], [])


def test_empty_and_header_only(tmp_path):
    p = make_file(tmp_path, 'name,score\n')
    assert load_scores(p) == ([], [])


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / 'missing.csv')


@pytest.mark.parametrize('value,ok', [(-1, False), (0, True), (100, True), (101, False)])
def test_score_bounds(tmp_path, value, ok):
    p = make_file(tmp_path, f'name,score\nA,{value}\n')
    kept, skipped = load_scores(p)
    assert (len(kept) == 1) is ok
    assert (len(skipped) == 0) is ok


def test_invalid_fields(tmp_path):
    p = make_file(tmp_path, 'name,score\n,70\nA,\nA,abc\nA,70,extra\n')
    kept, skipped = load_scores(p)
    assert kept == []
    assert [row[2] for row in skipped] == [
        '이름이 비어 있음', '점수가 비어 있음',
        '점수가 정수가 아님', '열 개수가 2가 아님'
    ]


def test_blank_lines_and_duplicate_names(tmp_path):
    p = make_file(tmp_path, 'name,score\nA,60\n\nA,90\n')
    assert load_scores(p) == ([('A', 60), ('A', 90)], [])
