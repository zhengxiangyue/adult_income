from basic import get_x_and_y
from sklearn import svm
import random
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from numpy.random import choice

if __name__ == '__main__':

    def stats_2_features(data, label, _i=7, _j=6):
        smaller_stats = [[0 for i in range(_j)] for j in range(_i)]
        larger_stats = [[0 for i in range(_j)] for j in range(_i)]
        for index, item in enumerate(data):
            if label[index] == 0:
                smaller_stats[item[0]][item[1]] += 1
            else:
                larger_stats[item[0]][item[1]] += 1
        print smaller_stats
        js_render_larger_list = []
        js_render_smaller_list = []
        for i in range(0, _i):
            for j in range(0, _j):
                js_render_larger_list.append([i, j, larger_stats[i][j]])
                js_render_smaller_list.append([i, j, smaller_stats[i][j]])
        print js_render_larger_list
        print js_render_smaller_list


    def k_fold_validation(k, data, label, method='svm.SVC(kernel=\'rbf\', C=1)'):
        split_number = k
        kf = KFold(n_splits=split_number)
        kf.get_n_splits(data)
        print "k fold validation start..."
        correctness = 0.0
        test_fold_index = 0

        for train_index, test_index in kf.split(data):
            data_train, label_train = [data[index] for index in train_index], [label[index] for index in train_index]
            data_test, label_test = [data[index] for index in test_index], [label[index] for index in test_index]
            clf = eval(method)
            clf.fit(data_train, label_train)

            # from sklearn.tree import export_graphviz
            # import os
            # tree_in_forest = clf.estimators_[5]
            # export_graphviz(tree_in_forest,
            #                 feature_names=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            #                 filled=True,
            #                 rounded=True, out_file='tree.dot')

            result = clf.predict(data_test)

            from sklearn.metrics import average_precision_score
            average_precision = average_precision_score(label_test, result)

            print average_precision
            correct = 0
            for index in range(0, len(result)):
                correct += (label_test[index] == result[index])
            print("TEST FOLD %s: %s" % (test_fold_index, float(correct) / float(len(result))))
            test_fold_index += 1
            correctness += float(correct) / float(len(result))
        correctness /= split_number
        print correctness


    def lir():
        data, label = get_x_and_y(True)
        num_of_zero = 0
        for each in label:
            num_of_zero += (1 if each == 0 else 0)
        print num_of_zero, len(label)


    def pick_feature_to_predict(index_list):
        data, label = get_x_and_y(True)
        data = [[each[index] for index in index_list] for each in data]
        max_features = len(index_list)
        k_fold_validation(10, data, label)


    pick_feature_to_predict([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    # _data, _label = get_x_and_y(True)
    # _data = [[each[_index] for _index in [5, 7]] for each in _data]
    # stats_2_features(_data, _label)
    # data type:
    # 1. discrete data sort by ratio (textual)
    # 2. discrete data sort by key (numerical)
    # 3. contious data sort by key, plot scater

    # 1 work class
    # 3 education
    # 5 martial status
    # 6 occupation
    # 7 relationship
    # 8 race
    # 9 sex
    # 13 native country

    # 0 age
    # 4 education number
    # 12 hours.per.week

    # 2 fnlwgt
    # 11 capatal loss
