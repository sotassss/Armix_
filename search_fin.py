# 0523作成

import json
import os
import function_fin
import numpy as np

# 処理フォルダ名、words_a：完全一致テキスト、words_b：含まれるテキスト
input_folder = "02_gray_ocr/"
words_1_a = ["単価", "数量", "診察項目名", "診療明細内容", "日付"]
words_1_b = ["単価", "数量", "単", "数", "診療明細", "日", "ちゃん"]
words_2_a = ["小計", "合計", "消費税", "外税"]
words_2_b = ["税", "計"]

# 各グループの高さ幅の初期化(基本は前のファイルの値を流用)
width_1, width_2, width_3 = 20, 20, 20
width_x = 40
y_min = 100
y_max = 1200

# input_folder内のJSONファイルをリストに取得し、ソートする
file_names = [f for f in os.listdir(input_folder) if f.endswith(".json")]
file_names.sort()

# ソートされた順にファイルを処理する
for file_name in file_names:
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
    ) = function_fin.process_data(data)

    print("---------------------------------------------------------")
    print(f"{file_name}")

    # 探索範囲の決定
    x_min = np.min(x_min_list)
    x_max = np.max(x_max_list)
    y_min = function_fin.find_word_y(
        words_1_a, words_1_b, text_list, y_max_list, 0, y_min
    )
    y_max = function_fin.find_word_y(
        words_2_a, words_2_b, text_list, y_min_list, y_min + 80, y_max
    )

    # 数字探索＋外れ値除去＋3グループに分類
    (
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
    ) = function_fin.find_number(
        text_list, x_mean_list, y_mean_list, y_max_list, y_min_list, y_min, y_max
    )

    # グループの幅を計算
    width_1, width_2, width_3 = function_fin.calculate_width(
        group1_y_width, group2_y_width, group3_y_width, width_1, width_2, width_3
    )

    # 水平方向を探索・存在しない場合は"no"とする
    long = function_fin.list_longest(group1, group2, group3)
    if long == 1:
        result_1, result_2, result_3 = function_fin.make_list_1(
            group1, group2, group3, group1_y, group2_y, group3_y, width_1
        )
    elif long == 2:
        result_1, result_2, result_3 = function_fin.make_list_2(
            group1, group2, group3, group1_y, group2_y, group3_y, width_2
        )
    elif long == 3:
        result_1, result_2, result_3 = function_fin.make_list_3(
            group1, group2, group3, group1_y, group2_y, group3_y, width_3
        )

    # 数字部分を抜き出す（"no"はそのまま)
    result_1, result_2, result_3 = function_fin.extract_digit(
        result_1, result_2, result_3
    )

    # "no"となった部分を計算により求める
    ans_1, ans_2, ans_3 = function_fin.change_member_no(result_1, result_2, result_3)
    print(f"個数{ans_1}")
    print(f"単価{ans_2}")
    print(f"金額{ans_3}")

    # 正答率の確認
    percent = function_fin.check(ans_1, ans_2, ans_3)
    print(f"正答率:{percent}%")

    ####################確認用#######################
    # print(f"y_min={y_min}")
    # print(f"y_max={y_max}")
    # print(f"text_list={text_list}")
    # print(f"result={result}")
