# config: utf-8

import csv
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.metrics.pairwise import chi2_kernel
from sklearn.model_selection import train_test_split
from sklearn import tree
import graphviz
from random import shuffle

education_map = {
    'Preschool': 0,
    '1st-4th': 1,
    '5th-6th': 2,
    '11th': 3,
    '9th': 4,
    '7th-8th': 5,
    '10th': 6,
    '12th': 7,
    'HS-grad': 8,
    'Some-college': 9,
    'Assoc-acdm': 10,
    'Assoc-voc': 11,
    'Bachelors': 12,
    'Masters': 13,
    'Prof-school': 14,
    'Doctorate': 15
}
occupation_map = {
    'Priv-house-serv': 0,
    'Other-service': 1,
    'Handlers-cleaners': 2,
    'Armed-Forces': 3,
    'Farming-fishing': 4,
    'Machine-op-inspct': 5,
    'Adm-clerical': 6,
    'Transport-moving': 7,
    'Craft-repair': 8,
    'Sales': 9,
    'Tech-support': 10,
    'Protective-serv': 11,
    'Prof-specialty': 12,
    'Exec-managerial': 13
}

index_map = [
    ['Never-worked', 'Without-pay', '?', 'Private', 'State-gov', 'Self-emp-not-inc', 'Local-gov', 'Federal-gov',
     'Self-emp-inc'],
    ['Preschool', '1st-4th', '5th-6th', '11th', '9th', '7th-8th', '10th', '12th', 'HS-grad', 'Some-college',
     'Assoc-acdm', 'Assoc-voc', 'Bachelors', 'Masters', 'Prof-school', 'Doctorate'],
    ['Never-married', 'Separated', 'Married-spouse-absent', 'Widowed', 'Divorced', 'Married-AF-spouse',
     'Married-civ-spouse'],
    ['Priv-house-serv', 'Other-service', 'Handlers-cleaners', '?', 'Armed-Forces', 'Farming-fishing',
     'Machine-op-inspct', 'Adm-clerical', 'Transport-moving', 'Craft-repair', 'Sales', 'Tech-support',
     'Protective-serv', 'Prof-specialty', 'Exec-managerial'],
    ['Own-child', 'Other-relative', 'Unmarried', 'Not-in-family', 'Husband', 'Wife'],
    ['Other', 'Amer-Indian-Eskimo', 'Black', 'White', 'Asian-Pac-Islander'],
    ['Female', 'Male'],
    ['Outlying-US(Guam-USVI-etc)', 'Holand-Netherlands', 'Dominican-Republic', 'Columbia', 'Guatemala', 'Mexico',
     'Nicaragua', 'Peru', 'Vietnam', 'Honduras', 'El-Salvador', 'Haiti', 'Puerto-Rico', 'Trinadad&Tobago', 'Portugal',
     'Laos', 'Jamaica', 'Ecuador', 'Thailand', 'South', 'Poland', 'Ireland', 'Hungary', 'United-States', 'Scotland',
     '?', 'Cuba', 'China', 'Greece', 'Hong', 'Philippines', 'Germany', 'Canada', 'England', 'Italy', 'Cambodia',
     'Yugoslavia', 'Japan', 'Taiwan', 'India', 'France', 'Iran'],

]


def feature_numeric(item, item_list):
    try:
        val = int(item)
        return val
    except ValueError:
        pass

    return item_list.index(item)


if __name__ == '__main__':
    data_list = []

    larger_than_50_points = {}
    smaller_than_50_points = {}

    data_package = []

    data_set = []
    label_set = []

    with open('adult.csv') as csvfile:
        csv_data = csv.reader(csvfile)

        for index, each_column_list in enumerate(csv_data):
            if index == 0:
                index_map = [list() for x in range(len(each_column_list))]
                continue
            if any(item == '?' for item in each_column_list):
                continue
            data_package.append([education_map[each_column_list[3]], occupation_map[each_column_list[6]], -1 if each_column_list[14] == '<=50K' else 1])

    shuffle(data_package)
    data_set = [[each[0], each[1]] for each in data_package]
    label_set = [each[2] for each in data_package]

    # x_train, x_test, y_train, y_test = train_test_split(data_set, label_set, test_size=0.9, random_state=0)
    # print len(x_train), len(x_test)
    #
    split_number = 10
    kf = KFold(n_splits=split_number)
    kf.get_n_splits(data_set)
    #
    correctness = 0.0

    for train_index, test_index in kf.split(data_set):
        print("TRAIN:", train_index, "TEST:", test_index)

        data_train = [data_set[index] for index in train_index]
        label_train = [label_set[index] for index in train_index]

        data_test = [data_set[index] for index in test_index]
        label_test = [label_set[index] for index in test_index]

        kerneled_data_train = chi2_kernel(data_train, gamma=.5)

        clf = svm.SVC(gamma='scale')
        # clf = svm.NuSVC()
        # clf = tree.DecisionTreeClassifier()
        clf.fit(kerneled_data_train, label_train)

        result = clf.predict(chi2_kernel(data_test, gamma=.5))
        #
        correct = 0
        for index in range(0, len(result)):
            correct += (label_test[index] == result[index])
        print float(correct) / float(len(result))
        correctness += float(correct) / float(len(result))

    correctness /= split_number
    print correctness

    # train_data = [[each[0], each[1]] for each in train_set]
    # train_label = [each[2] for each in train_set]
    #

    #
    #

# for each in test_set:
#     print(clf.predict([each[0], each[1]]) + ", " + each[2])
