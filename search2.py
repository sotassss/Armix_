# 0521作成
# 「単価」「個数

import json
import os
import function02
import function03
import numpy as np


input_folder = "02_gray_ocr/"

# input_folder内のJSONファイルのみを処理する
for file_name in os.listdir(input_folder):
    width = 160
    if file_name.endswith(".json"):
        file_path = os.path.join(input_folder, file_name)
        with open(file_path) as f:
            data = json.load(f)

        # 各リストを得る
        (
            text_list,
            x_mean_list,
            y_mean_list,
            x_max_list,
            y_max_list,
            x_min_list,
            y_min_list,
        ) = function02.process_data(data)

        print("---------------------------------------------------------")
        print(f"{file_name}")

        x_min = np.min(x_min_list)
        x_max = np.max(x_max_list)
        y_min = function02.find_word_y_up(
            "数量", "金額", "診療明細", "明細", text_list, y_min_list
        )
        y_max = function02.find_word_y_up(
            "小計", "計", "外税", "今回", text_list, y_min_list
        )

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
            count_number,
        ) = function03.find_number(
            text_list, x_mean_list, y_mean_list, y_max_list, y_min_list, y_min, y_max
        )

        width_1, width_2, width_3 = function03.calculate_width(
            group1_y_width, group2_y_width, group3_y_width
        )

        # 水平方向を探索・存在しない場合は"no"とする
        long = function02.list_longest(group1, group2, group3)
        if long == 1:
            result_1, result_2, result_3 = function02.make_list_1(
                group1, group2, group3, group1_y, group2_y, group3_y, width_1
            )
        elif long == 2:
            result_1, result_2, result_3 = function02.make_list_2(
                group1, group2, group3, group1_y, group2_y, group3_y, width_2
            )
        elif long == 3:
            result_1, result_2, result_3 = function02.make_list_3(
                group1, group2, group3, group1_y, group2_y, group3_y, width_3
            )

        # 数字部分を抜き出す（"no"はそのまま)
        result_1, result_2, result_3 = function03.extract_digit(
            result_1, result_2, result_3
        )

        # "no"となった部分を計算により求める
        ans_1, ans_2, ans_3 = function02.change_member_no(result_1, result_2, result_3)
        print(f"個数{ans_1}")
        print(f"単価{ans_2}")
        print(f"金額{ans_3}")

        # 正答率の確認
        percent = function02.check(ans_1, ans_2, ans_3)
        print(f"正答率:{percent}%")
