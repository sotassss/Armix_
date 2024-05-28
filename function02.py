import numpy as np
import re


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


# 3項目のうち2個が識別できる場合、残り一つの項目を生成する
def generate_member(list_1, list_2, list_3):
    list_1 = list_1 if list_1 is not None else []
    list_2 = list_2 if list_2 is not None else []
    list_3 = list_3 if list_3 is not None else []
    max_len = max(len(list_1), len(list_2), len(list_3))
    min_len = min(len(list_1), len(list_2), len(list_3))
    list_1_new, list_2_new, list_3_new = [], [], []
    if min_len == 0:
        return [], [], []  # 長さが0の場合、空のリストを返す
    for i in range(max_len):

        if i >= len(list_1):
            if isinstance(list_2[i], int) and isinstance(list_3[i], int):
                list_1_mem = int(list_3[i] / list_2[i])
                list_1_new.append(list_1_mem)
                list_2_new.append(list_2[i])
                list_3_new.append(list_3[i])

        elif i >= len(list_2):
            if isinstance(list_1[i], int) and isinstance(list_3[i], int):
                list_2_mem = int(list_3[i] / list_1[i])
                list_1_new.append(list_1[i])
                list_2_new.append(list_2_mem)
                list_3_new.append(list_3[i])

        elif i >= len(list_3):
            if isinstance(list_1[i], int) and isinstance(list_2[i], int):
                list_3_mem = int(list_1[i] * list_2[i])
                list_1_new.append(list_1[i])
                list_2_new.append(list_2[i])
                list_3_new.append(list_3_mem)

        else:
            list_1_new.append(list_1[i])
            list_2_new.append(list_2[i])
            list_3_new.append(list_3[i])

    return list_1_new, list_2_new, list_3_new


def calculate_y(y_1, y_2, y_3):
    if y_1 is None:
        if y_2 is not None and y_3 is not None:
            y_1 = (y_2 + y_3) / 2
        elif y_2 is not None:
            y_1 = y_2
        elif y_3 is not None:
            y_1 = y_3
        else:
            # どの値も None の場合の処理
            y_1, y_2, y_3 = None, None, None

    if y_2 is None:
        if y_1 is not None and y_3 is not None:
            y_2 = (y_1 + y_3) / 2
        elif y_1 is not None:
            y_2 = y_1
        elif y_3 is not None:
            y_2 = y_3
        else:
            # どの値も None の場合の処理
            y_1, y_2, y_3 = None, None, None

    if y_3 is None:
        if y_1 is not None and y_2 is not None:
            y_3 = (y_1 + y_2) / 2
        elif y_1 is not None:
            y_3 = y_1
        elif y_2 is not None:
            y_3 = y_2
        else:
            # どの値も None の場合の処理
            y_1, y_2, y_3 = None, None, None
    return y_1, y_2, y_3


def calculate_x(x_1, x_2, x_3, width):
    if x_1 is None:
        if x_2 is not None and x_3 is not None:
            width = x_3 - x_2
            x_1 = x_2 - width
        elif x_2 is not None:
            x_1 = x_2 - width
            x_3 = x_2 + width
        elif x_3 is not None:
            x_1 = x_3 - 2 * width
            x_2 = x_3 - width
        else:
            # どの値も None の場合の処理
            return None, None, None, width

    if x_2 is None:
        if x_1 is not None and x_3 is not None:
            width = (x_3 - x_1) / 2
            x_2 = x_1 + width
        elif x_1 is not None:
            x_2 = x_1 + width
            x_3 = x_1 + 2 * width
        elif x_3 is not None:
            x_1 = x_3 - 2 * width
            x_2 = x_3 - width
        else:
            # どの値も None の場合の処理
            return None, None, None, width

    if x_3 is None:
        if x_1 is not None and x_2 is not None:
            width = x_2 - x_1
        elif x_1 is not None:
            x_2 = x_1 + width
            x_3 = x_1 + 2 * width
        elif x_2 is not None:
            x_1 = x_2 - width
            x_3 = x_2 + width
        else:
            # どの値も None の場合の処理
            return None, None, None, width

    width = ((x_2 - x_1) + (x_3 - x_2) + (x_3 - x_1)) / 4.0
    return x_1, x_2, x_3, width


def find_word(word_1, text_list, x_list, y_list):
    for i, text in enumerate(text_list):
        if word_1 == text:  # 完全一致を確認
            return x_list[i], y_list[i]
    return None, None


# 各項目のメンバを整数型の数字として加える関数
def add_member(
    center_x,
    center_y,
    text_list,
    y_max_list,
    y_min_list,
    x_mean_list,
    y_mean_list,
    x_range,
    y_range,
):
    ans_list = []
    ans_list_y = []
    width_list = []
    if center_x is None or center_y is None:
        return None
    else:
        x_min = center_x - x_range
        x_max = center_x + x_range
        y_max = center_y + y_range
        for i, text in enumerate(text_list):
            if (
                x_min < x_mean_list[i]
                and x_mean_list[i] < x_max
                and y_mean_list[i] < y_max
                and center_y < y_mean_list[i]
                and (any(char.isdigit() for char in text))
            ):
                # 数字の部分のみを抽出して追加
                number_part = "".join(char for char in text if char.isdigit())
                if number_part:
                    ans_list.append(int(number_part))
                    ans_list_y.append(y_mean_list[i])
                    width_list.append(y_max_list[i] - y_min_list[i])
                # ans_list.append(int(text))
        width = np.mean(width_list)
        return ans_list, ans_list_y, width


def calculate_mean(bounding_box):
    x_mean = (bounding_box[0] + bounding_box[2] + bounding_box[4] + bounding_box[6]) / 4
    y_mean = (bounding_box[1] + bounding_box[3] + bounding_box[5] + bounding_box[7]) / 4
    return x_mean, y_mean


def calculate_max(bounding_box):
    x_max = max(bounding_box[0], bounding_box[2], bounding_box[4], bounding_box[6])
    y_max = max(bounding_box[1], bounding_box[3], bounding_box[5], bounding_box[7])
    return x_max, y_max


def calculate_min(bounding_box):
    x_min = min(bounding_box[0], bounding_box[2], bounding_box[4], bounding_box[6])
    y_min = min(bounding_box[1], bounding_box[3], bounding_box[5], bounding_box[7])
    return x_min, y_min


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
        bounding_box = item["boundingBox"]

        x_mean, y_mean = calculate_mean(bounding_box)
        x_max, y_max = calculate_max(bounding_box)
        x_min, y_min = calculate_min(bounding_box)

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


# 小計の上部分の座標を取得
def find_word_y_up(word_1, word_2, word_3, word_4, text_list, y_list):
    for i, text in enumerate(text_list):
        if word_1 == text:  # 完全一致を確認
            ans = y_list[i]
            return ans
        elif word_2 == text:
            ans = y_list[i]
            return ans
        elif word_3 in text:
            ans = y_list[i]
            return ans
        elif word_4 in text:
            ans = y_list[i]
            return ans
    return None


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


# resultで"no"となった要素を計算式により求める
def change_member_no(list_1, list_2, list_3):
    result_1, result_2, result_3 = [], [], []
    for money, count, total in zip(list_1, list_2, list_3):
        if money == "no" and count != "no" and total != "no":
            try:
                money = int(int(total) / int(count))
            except ZeroDivisionError:
                money = "no"
            result_1.append(int(money))
            result_2.append(int(count))
            result_3.append(int(total))
        elif money != "no" and count == "no" and total != "no":
            try:
                count = int(int(total) / int(money))
            except ZeroDivisionError:
                count = "no"
            result_1.append(int(money))
            result_2.append(int(count))
            result_3.append(int(total))
        elif money != "no" and count != "no" and total == "no":
            total = int(int(money) * int(count))
            result_1.append(int(money))
            result_2.append(int(count))
            result_3.append(int(total))
        else:
            result_1.append(money)
            result_2.append(count)
            result_3.append(total)
    return result_1, result_2, result_3
