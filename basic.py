# config: utf-8
import csv
from random import shuffle

def get_raw_data_package(file_path, ignore_missing=True):
    data_package = []
    with open(file_path) as csv_file:
        csv_data = csv.reader(csv_file)
        for index, each_column_list in enumerate(csv_data):
            if index == 0:
                continue
            if ignore_missing and any(item == '?' for item in each_column_list):
                continue
            for i, item in enumerate(each_column_list):
                try:
                    each_column_list[i] = int(item)
                except:
                    pass
            data_package.append(each_column_list)
    return data_package


def generate_js_render_data(raw_data, column_index):
    """
    :param raw_data:
    :param column_index:
    :return: [[{sorted feature values}], [number larger than 50K], [number smaller than 50K], [HIR]]
    """
    data = {}
    for index, each_column_list in enumerate(raw_data):
        if column_index == 2:
            each_column_list[column_index] = int(each_column_list[column_index]) / 1000
        if column_index == 11:
            each_column_list[column_index] = int(each_column_list[column_index]) / 10
        if each_column_list[column_index] not in data:
            data.update({
                each_column_list[column_index]: {
                    'larger': 0,
                    'smaller': 0
                }
            })
        data[each_column_list[column_index]]['larger' if each_column_list[14] == '>50K' else 'smaller'] += 1
    if column_index in [1, 3, 5, 6, 7, 8, 9, 13]:
        # for non-continus value, sort by the ratio
        data = sorted(data.items(), key=lambda item:float(item[1]['larger']) / float(item[1]['smaller']))
    else:
        data = sorted(data.items(), key=lambda item:float(item[0]))

    result = [[], [], [], []]

    for index, item in enumerate(data):
        if item[1]['smaller'] == 0:
            continue
        try:
            result[0].append(int(item[0]))
        except:
            result[0].append(item[0])

        result[1].append(item[1]['larger'])
        result[2].append(item[1]['smaller'])
        result[3].append(float("%.3f" % (float(item[1]['larger']) / (float(item[1]['larger']) + float(item[1]['smaller'])))))
    return result


def get_quantized_data():
    raw_data = get_raw_data_package('adult.csv')
    sorted_feature_list = [generate_js_render_data(raw_data, i)[0] for i in range(14)]
    quantize_row_index_list = [1, 3, 5, 6, 7, 8, 9, 13]
    for column_index in range(len(raw_data)):
        for row_index in quantize_row_index_list:
            raw_data[column_index][row_index] = int(sorted_feature_list[row_index].index(raw_data[column_index][row_index]))

    for i, each in enumerate(raw_data):
        raw_data[i][-1] = (0 if each[-1] == '<=50K' else 1)

    return raw_data


def get_x_and_y(randomize=False):
    """
    get data and label
    :param randomize:
    :return:
    """
    data = get_quantized_data()
    if randomize:
        shuffle(data)
    return [each[:-1] for each in data], [each[-1] for each in data]


if __name__ == '__main__':
    x, y = get_x_and_y()
    print len(x[0])
