"""AI B: 함수 구현은 제공받지 않고 명세 여섯 칸만을 기준으로 작성한 테스트."""
import pytest
from load_scores import load_scores


def csv_case(tmp_path, lines):
    file = tmp_path / 'scores_case.csv'
    file.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return file


def test_valid_input_returns_original_order(tmp_path):
    file = csv_case(tmp_path, ['name,score', '민지,45', '준호,82'])
    assert load_scores(file) == ([('민지', 45), ('준호', 82)], [])


def test_blank_line_not_logged(tmp_path):
    file = csv_case(tmp_path, ['name,score', '민지,45', '', '준호,82'])
    assert load_scores(file) == ([('민지', 45), ('준호', 82)], [])


def test_quoted_comma_in_name(tmp_path):
    file = csv_case(tmp_path, ['name,score', '"김,민지",99'])
    assert load_scores(file) == ([('김,민지', 99)], [])


def test_missing_path_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / 'none.csv')


def test_only_header_empty_result(tmp_path):
    file = csv_case(tmp_path, ['name,score'])
    assert load_scores(file) == ([], [])


@pytest.mark.parametrize('score,accepted', [(0, True), (100, True), (101, False), (-1, False)])
def test_boundary_inclusive_zero_and_hundred(tmp_path, score, accepted):
    file = csv_case(tmp_path, ['name,score', f'테스트,{score}'])
    kept, skipped = load_scores(file)
    assert (len(kept) == 1) == accepted
    assert len(skipped) == (0 if accepted else 1)


def test_invalid_name_and_score_logged(tmp_path):
    file = csv_case(tmp_path, ['name,score', ',70', '가,', '나,글자', '다,40,extra'])
    kept, skipped = load_scores(file)
    assert kept == []
    assert len(skipped) == 4
    assert [item[0] for item in skipped] == [2, 3, 4, 5]


def test_duplicate_name_must_be_preserved(tmp_path):
    file = csv_case(tmp_path, ['name,score', '가,40', '가,90'])
    assert load_scores(file) == ([('가', 40), ('가', 90)], [])
