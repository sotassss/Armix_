# 03_no用に用意した関数
import numpy as np
import re
import function02


# 小計の上部分で数字が密集している部分を探索
def find_digit(text_list, x_mean_list, y_mean_list, x_min, x_max, y_max):
    results = []
    x_list = []
    width = 10
    num_intervals = (x_max - x_min) // width

    for i in range(num_intervals):
        results_maybe = []
        count = 0
        x_sum = 0
        x_width_min = x_min + i * width
        x_width_max = x_min + (i + 2) * width

        for text, x_mean, y_mean in zip(text_list, x_mean_list, y_mean_list):
            if (
                (x_width_min <= x_mean <= x_width_max)
                and (y_mean <= y_max)
                and any(char.isdigit() for char in text)
            ):
                results_maybe.append((text, x_mean, y_mean))  # タプルとして追加する
                x_sum += x_mean
                count += 1

        if count > 5:
            results.append(results_maybe)
            x_mean = x_sum / count
            x_list.append(x_mean)
    return results, x_list


# テキストリストから、すべて数字または数字+漢字1文字の文字列を抜き出す→y座標が異常な要素を削除→3グループに分ける
def find_number(
    text_list, x_mean_list, y_mean_list, y_max_list, y_min_list, y_min, y_max
):
    result, result_x, result_y, result_y_width = [], [], [], []
    count = 0
    for text, x_mean, y_mean, y_large, y_small in zip(
        text_list, x_mean_list, y_mean_list, y_max_list, y_min_list
    ):
        if (y_min < y_mean) and (y_mean < y_max):
            if re.fullmatch(r"\d+", text):  # 全て数字の場合
                result.append(text)
                result_x.append(x_mean)
                result_y.append(y_mean)
                result_y_width.append(y_large - y_small)
                count += 1
            # elif re.fullmatch(r"\d+[一-龥]", text):  # 数字＋漢字一文字の場合
            elif re.fullmatch(r"\d+\w{1,4}", text):  # 数字＋文字(4字以内)
                result.append(text)
                result_x.append(x_mean)
                result_y.append(y_mean)
                result_y_width.append(y_large - y_small)
                count += 1

    # result_yの異常値を削除
    if len(result_y) > 2:
        y_diffs = np.abs(np.diff(result_y))
        mean_diff = np.mean(y_diffs)
        std_diff = np.std(y_diffs)
        threshold = mean_diff + 2 * std_diff

        filtered_result, filtered_x, filtered_y, filtered_width = [], [], [], []
        for i in range(len(result_y)):
            if i == (len(result_y) - 1):
                prev_diff = abs(result_y[i] - result_y[i - 1])
                if prev_diff < threshold:
                    filtered_result.append(result[i])
                    filtered_x.append(result_x[i])
                    filtered_y.append(result_y[i])
                    filtered_width.append(result_y_width[i])
            else:
                next_diff = abs(result_y[i] - result_y[i + 1])
                if next_diff <= threshold:
                    filtered_result.append(result[i])
                    filtered_x.append(result_x[i])
                    filtered_y.append(result_y[i])
                    filtered_width.append(result_y_width[i])

        result, result_x, result_y, result_y_width = (
            filtered_result,
            filtered_x,
            filtered_y,
            filtered_width,
        )

    # result_xの異常値を削除
    if len(result_x) > 2:
        mean_x = np.mean(result_x)
        std_x = np.std(result_x)
        threshold_x = 2 * std_x
        filtered_result, filtered_x, filtered_y = [], [], []

        # 外れ値を除外
        for i in range(len(result_x)):
            if abs(result_x[i] - mean_x) <= threshold_x:
                filtered_result.append(result[i])
                filtered_x.append(result_x[i])
                filtered_y.append(result_y[i])

        result, result_x, result_y = filtered_result, filtered_x, filtered_y

    # x_meanの範囲を決定して3グループに分類
    if result_x:
        min_x, max_x = min(result_x), max(result_x)
        range1 = min_x + (max_x - min_x) / 3
        range2 = min_x + 2 * (max_x - min_x) / 3

        (
            group1,
            group2,
            group3,
            group1_y,
            group2_y,
            group3_y,
            group1_y_width,
            group2_y_width,
            group3_y_width,
        ) = ([], [], [], [], [], [], [], [], [])
        for text, x_mean, y_mean, y_width in zip(
            result, result_x, result_y, result_y_width
        ):
            if x_mean <= range1:
                group1.append(text)
                group1_y.append(y_mean)
                group1_y_width.append(y_width)
            elif x_mean <= range2:
                group2.append(text)
                group2_y.append(y_mean)
                group2_y_width.append(y_width)
            else:
                group3.append(text)
                group3_y.append(y_mean)
                group3_y_width.append(y_width)
    else:
        (
            group1,
            group2,
            group3,
            group1_y,
            group2_y,
            group3_y,
            group1_y_width,
            group2_y_width,
            group3_y_width,
        ) = ([], [], [], [], [], [], [], [], [])

    return (
        group1,
        group2,
        group3,
        group1_y,
        group2_y,
        group3_y,
        group1_y_width,
        group2_y_width,
        group3_y_width,
        count,
    )


def calculate_width(group1_y, group2_y, group3_y):
    if len(group1_y) > 1:
        width_1 = np.mean(group1_y)
    if len(group2_y) > 1:
        width_2 = np.mean(group2_y)
    if len(group3_y) > 1:
        width_3 = np.mean(group3_y)

    return width_1, width_2, width_3


# リストから数字部分のみを取りだす関数
import re


def extract_digit(list1, list2, list3):
    list1_new = []
    for item in list1:
        if item == "no":
            list1_new.append(item)
        digits = "".join(re.findall(r"\d+", item))
        if digits:
            list1_new.append(int(digits))

    list2_new = []
    for item in list2:
        if item == "no":
            list2_new.append(item)
        digits = "".join(re.findall(r"\d+", item))
        if digits:
            list2_new.append(int(digits))

    list3_new = []
    for item in list3:
        if item == "no":
            list3_new.append(item)
        digits = "".join(re.findall(r"\d+", item))
        if digits:
            list3_new.append(int(digits))

    return list1_new, list2_new, list3_new
