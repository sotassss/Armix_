# 関数一覧

import re
import numpy as np
import function_sub_fin
from function_class import Extract_outlier_iqr_x


# jsonファイルから情報を抜き出す
def process_data(data):
    text_list = []
    x_mean_list = []
    y_mean_list = []
    x_max_list = []
    y_max_list = []
    x_min_list = []
    y_min_list = []

    for item in data:
        text = item["text"]
        text = re.sub(r"\s", "", text)  # テキストから空白を削除
        text = re.sub(r"[\s\u00A5\uFFE5]", "", text)  # テキストから￥マーク削除
        text = re.sub(r"[\sｕｖ]", "", text)  # テキストからu,vを削除
        text = re.sub(r"[YＹ]", "", text)  # テキストからYを削除
        text = re.sub(r"O", "0", text)  # テキストのOを0に変換
        bounding_box = item["boundingBox"]

        x_mean, y_mean = function_sub_fin.calculate_mean(bounding_box)
        x_max, y_max = function_sub_fin.calculate_max(bounding_box)
        x_min, y_min = function_sub_fin.calculate_min(bounding_box)

        text_list.append(text)
        x_mean_list.append(x_mean)
        y_mean_list.append(y_mean)
        x_max_list.append(x_max)
        y_max_list.append(y_max)
        x_min_list.append(x_min)
        y_min_list.append(y_min)

        # 数字から . , を削除
        text_list = [
            re.sub(r"[,. ]", "", text) if re.search(r"\d", text) else text
            for text in text_list
        ]

    return [
        text_list,
        x_mean_list,
        y_mean_list,
        x_max_list,
        y_max_list,
        x_min_list,
        y_min_list,
    ]


# 小計の上部分の座標を取得・y_search_minより下の範囲を探索
def find_word_y(words_a, words_b, text_list, y_list, y_search_min, y_now):
    for i, text in enumerate(text_list):
        if y_search_min < y_list[i]:
            for word in words_a:
                if word == text:
                    return y_list[i]
            for word in words_b:
                if word in text:
                    return y_list[i]
    return y_now


def find_number(
    text_list, x_mean_list, y_mean_list, y_max_list, y_min_list, y_min, y_max
):
    result, result_x, result_y, result_y_width = [], [], [], []
    for text, x_mean, y_mean, y_large, y_small in zip(
        text_list, x_mean_list, y_mean_list, y_max_list, y_min_list
    ):
        if (y_min < y_mean) and (y_mean < y_max):
            if re.fullmatch(r"\d+", text):  # 全て数字の場合
                result.append(text)
                result_x.append(x_mean)
                result_y.append(y_mean)
                result_y_width.append(y_large - y_small)

            elif re.fullmatch(r"\d+\w{1,4}", text):  # 数字＋文字(4字以内)
                result.append(text)
                result_x.append(x_mean)
                result_y.append(y_mean)
                result_y_width.append(y_large - y_small)

    # # result_xの異常値を除去
    result, result_x, result_y, result_y_width = function_sub_fin.extract_outlier_iqr_x(
        result, result_x, result_y, result_y_width
    )

    # # クラスを用いた表記(うまくいっていない)
    # outlier_remover = Extract_outlier_iqr_x(result, result_x, result_y, result_y_width)
    # result, result_x, result_y, result_y_width = outlier_remover.extract_outlier_iqr_x()

    # result_yの異常値を削除①
    result, result_x, result_y, result_y_width = function_sub_fin.extract_outlier_iqr_y(
        result, result_x, result_y, result_y_width
    )

    # result_yの異常値を削除②
    result, result_x, result_y, result_y_width = (
        function_sub_fin.extract_outlier_diff_y(
            result, result_x, result_y, result_y_width
        )
    )

    # x_meanの範囲を決定して3グループに分類
    if result_x:
        min_x, max_x = min(result_x), max(result_x)
        range1 = min_x + (max_x - min_x) / 4
        range2 = min_x + 3 * (max_x - min_x) / 4

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
        result,
        group1,
        group2,
        group3,
        group1_y,
        group2_y,
        group3_y,
        group1_y_width,
        group2_y_width,
        group3_y_width,
    )


# 各グループの高さ方向の幅を探索
def calculate_width(group1_y, group2_y, group3_y, width_1, width_2, width_3):
    width_1_new, width_2_new, width_3_new = width_1, width_2, width_3
    if len(group1_y) > 1:
        width_1_new = np.mean(group1_y)
    if len(group2_y) > 1:
        width_2_new = np.mean(group2_y)
    if len(group3_y) > 1:
        width_3_new = np.mean(group3_y)

    return width_1_new, width_2_new, width_3_new


# 最長リストを識別する関数
def list_longest(list_1, list_2, list_3):
    max_len = max(len(list_1), len(list_2), len(list_3))
    if max_len == len(list_1):
        return 1

    elif max_len == len(list_2):
        return 2

    elif max_len == len(list_3):
        return 3


# リスト1が最大の場合の処理
def make_list_1(list_1, list_2, list_3, list_1_y, list_2_y, list_3_y, width):
    result_1, result_2, result_3 = [], [], []
    num = len(list_1)
    search_width = width / 2
    # リスト1の要素数(最大数)だけ回す
    for i in range(num):
        count_2, count_3 = 0, 0
        result_1.append(list_1[i])
        y1 = list_1_y[i] - search_width
        y2 = list_1_y[i] + search_width
        # リスト2に対する処理
        for j in range(len(list_2)):
            if y1 <= list_2_y[j] <= y2:
                result_2.append(list_2[j])
                count_2 += 1
        if count_2 == 0:
            result_2.append("no")

        # リスト3に対する処理
        for k in range(len(list_3)):
            if y1 <= list_3_y[k] <= y2:
                result_3.append(list_3[k])
                count_3 += 1
        if count_3 == 0:
            result_3.append("no")

    return result_1, result_2, result_3


# リスト2が最大の場合の処理
def make_list_2(list_1, list_2, list_3, list_1_y, list_2_y, list_3_y, width):
    result_1, result_2, result_3 = [], [], []
    num = len(list_2)
    search_width = width / 2
    # リスト2の要素数(最大数)だけ回す
    for i in range(num):
        count_1, count_3 = 0, 0
        result_2.append(list_2[i])
        y1 = list_2_y[i] - search_width
        y2 = list_2_y[i] + search_width
        # リスト1に対する処理
        for j in range(len(list_1)):
            if y1 <= list_1_y[j] <= y2:
                result_1.append(list_1[j])
                count_1 += 1
        if count_1 == 0:
            result_1.append("no")

        # リスト3に対する処理
        for k in range(len(list_3)):
            if y1 <= list_3_y[k] <= y2:
                result_3.append(list_3[k])
                count_3 += 1
        if count_3 == 0:
            result_3.append("no")

    return result_1, result_2, result_3


# リスト3が最大の場合の処理
def make_list_3(list_1, list_2, list_3, list_1_y, list_2_y, list_3_y, width):
    result_1, result_2, result_3 = [], [], []
    num = len(list_3)
    search_width = width / 2
    # リスト3の要素数(最大数)だけ回す
    for i in range(num):
        count_1, count_2 = 0, 0
        result_3.append(list_3[i])
        y1 = list_3_y[i] - search_width
        y2 = list_3_y[i] + search_width
        # リスト1に対する処理
        for j in range(len(list_1)):
            if y1 <= list_1_y[j] <= y2:
                result_1.append(list_1[j])
                count_1 += 1
        if count_1 == 0:
            result_1.append("no")

        # リスト2に対する処理
        for k in range(len(list_2)):
            if y1 <= list_2_y[k] <= y2:
                result_2.append(list_2[k])
                count_2 += 1
        if count_2 == 0:
            result_2.append("no")

    return result_1, result_2, result_3


# リストから数字部分のみを取りだす関数
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


# resultで"no"となった要素を計算式により求める
def change_member_no(list_1, list_2, list_3):
    result_1, result_2, result_3 = [], [], []
    for money, count, total in zip(list_1, list_2, list_3):
        if money == "no" and count != "no" and total != "no":
            try:
                money = int(int(total) / int(count))
            except ZeroDivisionError:
                money = "no"
            result_1.append(money)
            result_2.append(count)
            result_3.append(total)
        elif money != "no" and count == "no" and total != "no":
            try:
                count = int(int(total) / int(money))
            except ZeroDivisionError:
                count = "no"
            result_1.append(money)
            result_2.append(count)
            result_3.append(total)
        elif money != "no" and count != "no" and total == "no":
            total = int(int(money) * int(count))
            result_1.append(money)
            result_2.append(count)
            result_3.append(total)
        else:
            result_1.append(money)
            result_2.append(count)
            result_3.append(total)
    return result_1, result_2, result_3


# 項目・数量・金額の関係が満たされているかを確認・正答率を%で返す
def check(list_1, list_2, list_3):
    # Noneのリストは空リストに変換する
    list_1 = list_1 if list_1 is not None else []
    list_2 = list_2 if list_2 is not None else []
    list_3 = list_3 if list_3 is not None else []
    count = 0
    max_len = max(len(list_1), len(list_2), len(list_3))
    min_len = min(len(list_1), len(list_2), len(list_3))

    if min_len == 0:
        return 0  # 長さが0の場合、計算できないので0を返す

    for i in range(min_len):
        try:
            left = float(list_1[i]) * float(list_2[i])
            right = float(list_3[i])
        except ValueError:
            continue  # 数値に変換できない要素がある場合、スキップする

        if left == right:
            count += 1

    # 正答率を返す
    ans = (count / max_len) * 100
    return ans
