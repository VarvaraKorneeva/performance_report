import sys

import pytest

from report import performance_report, get_args, get_report, get_row_number_for_report


def test_performance_report_one_file():
    report = performance_report(['data/employees1.csv'])
    assert report == [('Backend Developer', 4.85),
                      ('DevOps Engineer', 4.7),
                      ('Data Engineer', 4.7),
                      ('Data Scientist', 4.7),
                      ('Mobile Developer', 4.6),
                      ('Frontend Developer', 4.6),
                      ('QA Engineer', 4.5)]


def test_performance_report_few_files():
    report = performance_report(['data/employees1.csv', 'data/employees2.csv'])
    assert report == [('Backend Developer', 4.83),
                      ('DevOps Engineer', 4.8),
                      ('Data Engineer', 4.7),
                      ('Fullstack Developer', 4.7),
                      ('Frontend Developer', 4.65),
                      ('Data Scientist', 4.65),
                      ('Mobile Developer', 4.6),
                      ('QA Engineer', 4.5)]


@pytest.fixture
def mock_argv(request):
    curr_argv = sys.argv
    sys.argv = request.param
    yield
    sys.argv = curr_argv


@pytest.mark.parametrize('mock_argv',
                         [['report.py', '--files', 'data/employees1.csv', 'data/employees2.csv',
                           '--report', 'performance']],
                         indirect=True)
def test_read_args_right_args(mock_argv):
    files, report_name = get_args()
    assert files == ['data/employees1.csv', 'data/employees2.csv'] and report_name == 'performance'


@pytest.mark.parametrize('mock_argv',
                         [['report.py', '--files', 'data/not_exists_file.csv', '--report', 'performance']],
                         indirect=True)
def test_read_args_wrong_file(mock_argv, capsys):
    with pytest.raises(SystemExit) as exception:
        _, _ = get_args()
    captured = capsys.readouterr()
    assert captured.out == 'Файлы не были найдены.\n'
    assert exception.value.code == 0


@pytest.mark.parametrize('mock_argv',
                         [['report.py']],
                         indirect=True)
def test_read_args_without_args(mock_argv, capsys):
    with pytest.raises(SystemExit) as exception:
        _, _ = get_args()
    captured = capsys.readouterr()
    assert captured.out == 'Не указано значение для аргумента --files или --report.\n'
    assert exception.value.code == 0


@pytest.mark.parametrize('mock_argv',
                         [['report.py', '--files', 'daata/employees1.csv']],
                         indirect=True)
def test_read_args_only_files(mock_argv, capsys):
    with pytest.raises(SystemExit) as exception:
        _, _ = get_args()
    captured = capsys.readouterr()
    assert captured.out == 'Не указано значение для аргумента --files или --report.\n'
    assert exception.value.code == 0


@pytest.mark.parametrize('mock_argv',
                         [['report.py', '--report', 'performance']],
                         indirect=True)
def test_read_args_only_report(mock_argv, capsys):
    with pytest.raises(SystemExit) as exception:
        _, _ = get_args()
    captured = capsys.readouterr()
    assert captured.out == 'Не указано значение для аргумента --files или --report.\n'
    assert exception.value.code == 0


@pytest.mark.parametrize('mock_argv',
                         [['report.py', '--unknown', 'arg']],
                         indirect=True)
def test_read_args_unknown_arg(mock_argv, capsys):
    with pytest.raises(SystemExit) as exception:
        _, _ = get_args()
    captured = capsys.readouterr()
    assert captured.out == 'Введены некорректные аргументы.\n'
    assert exception.value.code == 1


def test_output_report(capsys):
    get_report(['data/employees1.csv'], 'performance')
    captured = capsys.readouterr()
    assert captured.out == '    position              performance\n' \
                           '--  ------------------  -------------\n' \
                           ' 1  Backend Developer            4.85\n' \
                           ' 2  DevOps Engineer              4.7\n' \
                           ' 3  Data Engineer                4.7\n' \
                           ' 4  Data Scientist               4.7\n' \
                           ' 5  Mobile Developer             4.6\n' \
                           ' 6  Frontend Developer           4.6\n' \
                           ' 7  QA Engineer                  4.5\n'


def test_get_row_number_for_report():
    data_with_num = get_row_number_for_report([('Mobile Developer', 4.6), ('Backend Developer', 4.85)])
    assert data_with_num == [(1, 'Mobile Developer', 4.6), (2, 'Backend Developer', 4.85)]
