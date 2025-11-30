import argparse
import csv
import os
import sys

from tabulate import tabulate


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+')
    parser.add_argument('--report', type=str)

    try:
        args = parser.parse_args()
    except SystemExit:
        print('Введены некорректные аргументы.')
        sys.exit(1)

    if not args.files or not args.report:
        print('Не указано значение для аргумента --files или --report.')
        sys.exit(0)

    for file in args.files:
        isfile = os.path.isfile(file)
        if not isfile:
            print('Файлы не были найдены.')
            sys.exit(0)

    return args.files, args.report


def performance_report(files):
    position_count = {}
    for file in files:
        with open(file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader) # Пропускаем первую строку с заголовками
            for row in csv_reader:
                if row[1] not in position_count.keys():
                    position_count[row[1]] = [float(row[3]), 1]
                else:
                    position_count[row[1]][0] += float(row[3]) # Сумма performance
                    position_count[row[1]][1] += 1 # Количество записей

    performance_avg = []
    for key, value in position_count.items():
        performance_avg.append((key, round(value[0]/value[1], 2)))

    return performance_avg


def get_row_number_for_report(data):
    for i, row in enumerate(data):
        data[i] = (i+1,) + row

    return data


def get_report(files, report_name):
    report_data, headers = [], []
    # Отчет performance
    if report_name == 'performance':
        report_data = performance_report(files)
        headers = ['', 'position', 'performance']

    report_data_with_num = get_row_number_for_report(report_data)
    print(tabulate(report_data_with_num, headers=headers))


if __name__ == '__main__':
    files, report = get_args()
    get_report(files, report)
