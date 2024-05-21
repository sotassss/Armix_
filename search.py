# 0521作成

import json
import os
import function
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
        ) = function.process_data(data)

        print("---------------------------------------------------------")
        # 単価の文字列の検出
        x1, y1 = function.find_word("単価", text_list, x_mean_list, y_mean_list)
        x2, y2 = function.find_word("数量", text_list, x_mean_list, y_mean_list)
        x3, y3 = function.find_word("金額", text_list, x_mean_list, y_mean_list)

        # 3項目検出できない場合の対応
        x1, x2, x3, width = function.calculate_x(x1, x2, x3, width)
        y1, y2, y3 = function.calculate_y(y1, y2, y3)

        print(f"{file_name}")
        print(f"単価  ({x1}, {y1})")
        print(f"数量  ({x2}, {y2})")
        print(f"金額  ({x3}, {y3})")

        # 各項目のメンバの探索範囲
        x_wid = width / 2
        y_search_max = function.find_word_y_up("小計", "計", text_list, y_min_list)
        y_wid = y_search_max - np.mean([y1, y2, y3])

        # 各項目のメンバの探索
        list_1, list_1_y, width_1 = function.add_member(
            x1,
            y1,
            text_list,
            y_max_list,
            y_min_list,
            x_mean_list,
            y_mean_list,
            x_wid,
            y_wid,
        )
        list_2, list_2_y, width_2 = function.add_member(
            x2,
            y2,
            text_list,
            y_max_list,
            y_min_list,
            x_mean_list,
            y_mean_list,
            x_wid,
            y_wid,
        )
        list_3, list_3_y, width_3 = function.add_member(
            x3,
            y3,
            text_list,
            y_max_list,
            y_min_list,
            x_mean_list,
            y_mean_list,
            x_wid,
            y_wid,
        )
        # list_1_new, list_2_new, list_3_new = function.generate_member(
        #     list_1, list_2, list_3
        # )

        long = function.list_longest(list_1, list_2, list_3)
        if long == 1:
            result_1, result_2, result_3 = function.make_list_1(
                list_1, list_2, list_3, list_1_y, list_2_y, list_3_y, width_1
            )
        elif long == 2:
            result_1, result_2, result_3 = function.make_list_2(
                list_1, list_2, list_3, list_1_y, list_2_y, list_3_y, width_2
            )
        elif long == 3:
            result_1, result_2, result_3 = function.make_list_3(
                list_1, list_2, list_3, list_1_y, list_2_y, list_3_y, width_3
            )

        ans_1, ans_2, ans_3 = function.change_member_no(result_1, result_2, result_3)

        print(f"単価:{list_1}")
        print(f"個数:{list_2}")
        print(f"金額:{list_3}")
        print(f"単価(new):{result_1}")
        print(f"個数(new):{result_2}")
        print(f"金額(new):{result_3}")
        print(f"単価(fin):{ans_1}")
        print(f"個数(fin):{ans_2}")
        print(f"金額(fin):{ans_3}")
        ans_old = int(function.check(list_1, list_2, list_3))
        ans_new = int(function.check(result_1, result_2, result_3))
        ans_fin = int(function.check(ans_1, ans_2, ans_3))
        print(f"正答率(old):{ans_old}%")
        print(f"正答率(new):{ans_new}%")
        print(f"正答率(fin):{ans_fin}%")
