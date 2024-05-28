import numpy as np


class Extract_outlier_iqr_x:
    def __init__(self, list, list_x, list_y, width):
        self.list = list
        self.list_x = list_x
        self.list_y = list_y
        self.width = width

    def extract_outlier_iqr_x(self):
        filtered_list, filtered_list_x, filtered_list_y, filtered_width = [], [], [], []
        if len(self.list_x) > 0:
            Q1 = np.percentile(self.list_x, 25)
            Q2 = np.percentile(self.list_x, 50)
            Q3 = np.percentile(self.list_x, 75)
            IQR = ((Q3 - Q1) + (Q2 - Q1) + (Q3 - Q2)) / 2
            # 外れ値の基準
            lower_bound = Q1 - 1.0 * IQR
            upper_bound = Q3 + 1.0 * IQR
            for i in range(len(self.list_x)):
                if (lower_bound < self.list_x[i]) and (self.list_x[i] < upper_bound):
                    filtered_list.append(list[i])
                    filtered_list_x.append(self.list_x[i])
                    filtered_list_y.append(self.list_y[i])
                    filtered_width.append(self.width[i])
        return (filtered_list, filtered_list_x, filtered_list_y, filtered_width)
