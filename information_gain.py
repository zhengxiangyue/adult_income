from basic import get_x_and_y
from sklearn.feature_selection import mutual_info_classif

x, y = get_x_and_y()
print mutual_info_classif(x, y)