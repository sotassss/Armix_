# 補助関数一覧

import numpy as np
import re


# 平均の計算
def calculate_mean(bounding_box):
    x_mean = (bounding_box[0] + bounding_box[2] + bounding_box[4] + bounding_box[6]) / 4
    y_mean = (bounding_box[1] + bounding_box[3] + bounding_box[5] + bounding_box[7]) / 4
    return x_mean, y_mean


# 最大値の計算
def calculate_max(bounding_box):
    x_max = max(bounding_box[0], bounding_box[2], bounding_box[4], bounding_box[6])
    y_max = max(bounding_box[1], bounding_box[3], bounding_box[5], bounding_box[7])
    return x_max, y_max


# 最小値の計算
def calculate_min(bounding_box):
    x_min = min(bounding_box[0], bounding_box[2], bounding_box[4], bounding_box[6])
    y_min = min(bounding_box[1], bounding_box[3], bounding_box[5], bounding_box[7])
    return x_min, y_min


# 外れ値(x)の除去(四分位数を用いる)
def extract_outlier_iqr_x(list, list_x, list_y, width):
    filtered_list, filtered_list_x, filtered_list_y, filtered_width = [], [], [], []
    if len(list_x) > 0:
        Q1 = np.percentile(list_x, 25)
        Q2 = np.percentile(list_x, 50)
        Q3 = np.percentile(list_x, 75)
        IQR = ((Q3 - Q1) + (Q2 - Q1) + (Q3 - Q2)) / 2
        # 外れ値の基準
        lower_bound = Q1 - 1.0 * IQR
        upper_bound = Q3 + 1.0 * IQR
        for i in range(len(list_x)):
            if (lower_bound < list_x[i]) and (list_x[i] < upper_bound):
                filtered_list.append(list[i])
                filtered_list_x.append(list_x[i])
                filtered_list_y.append(list_y[i])
                filtered_width.append(width[i])
    return (filtered_list, filtered_list_x, filtered_list_y, filtered_width)


# 外れ値(y)の除去(四分位数を用いる)
def extract_outlier_iqr_y(list, list_x, list_y, width):
    filtered_list, filtered_list_x, filtered_list_y, filtered_width = [], [], [], []
    if len(list_y) > 0:
        Q1 = np.percentile(list_y, 25)
        Q2 = np.percentile(list_y, 50)
        Q3 = np.percentile(list_y, 75)
        IQR = ((Q3 - Q1) + (Q2 - Q1) + (Q3 - Q2)) / 2
        # 外れ値の基準
        lower_bound = Q1 - 3.0 * IQR
        upper_bound = Q3 + 3.0 * IQR
        for i in range(len(list_y)):
            if (lower_bound < list_y[i]) and (list_y[i] < upper_bound):
                filtered_list.append(list[i])
                filtered_list_x.append(list_x[i])
                filtered_list_y.append(list_y[i])
                filtered_width.append(width[i])
    return filtered_list, filtered_list_x, filtered_list_y, filtered_width


# 外れ値(y)の除去(差を用いる)
def extract_outlier_diff_y(list, list_x, list_y, width):
    filtered_list, filtered_list_x, filtered_list_y, filtered_width = [], [], [], []
    if len(list_y) > 2:
        y_diffs = np.abs(np.diff(list_y))
        mean_diff = np.mean(y_diffs)
        std_diff = np.std(y_diffs)
        threshold = mean_diff + 2 * std_diff

        for i in range(len(list_y)):
            if i == (len(list_y) - 1):
                prev_diff = abs(list_y[i] - list_y[i - 1])
                if prev_diff < threshold:
                    filtered_list.append(list[i])
                    filtered_list_x.append(list_x[i])
                    filtered_list_y.append(list_y[i])
                    filtered_width.append(width[i])
            else:
                next_diff = abs(list_y[i] - list_y[i + 1])
                if next_diff <= threshold:
                    filtered_list.append(list[i])
                    filtered_list_x.append(list_x[i])
                    filtered_list_y.append(list_y[i])
                    filtered_width.append(width[i])

    return filtered_list, filtered_list_x, filtered_list_y, filtered_width
