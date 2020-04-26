import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import matplotlib.ticker as ticker
from scipy.stats import t
from scipy.stats import chi2
from scipy.stats import norm
import math

alpha = 0.95
F = 0.334


class Interval:

    def __init__(self):
        self.interval = []
        self.name = ""
        self.right_param = 0

    def __str__(self):
        return f"{self.name}: {self.interval} right param was = {self.right_param}"


def read_data():

    zeros_data = []
    ones_data = []
    all_data = []
    boolean_arr = []

    wb = load_workbook('../data.xlsx')
    sheet = wb.get_sheet_by_name('Лист1')

    for i in range(1, 50):
        boolean_arr.append(sheet[f'A{i + 1}'].value)
        all_data.append(sheet[f'L{i + 1}'].value)

    for i in range(len(all_data)):
        if boolean_arr[i] == 0:
            zeros_data.append(all_data[i])
        else:
            ones_data.append(all_data[i])

    return zeros_data, ones_data


def get_x(arr, locator):
    arr[arr.index(max(arr))] -= locator
    return arr


def getT2(x):
    mean = np.mean(x)
    sum = 0
    for i in x:
        sum += (i - mean) * (i - mean)
    return sum


def get_plot_to_interval(data1, data2, name):
    fig, ax = plt.subplots()
    plt.title(name)

    locator = int(max(data1[1], data1[0], data2[1], data2[0])) - int(min(data1[1], data1[0], data2[1], data2[0]))

    if locator < 10:
        locator = 1
    else:
        locator = int((locator - locator % 10) / 10)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(locator))

    ax.plot([data1[0], data1[1]], [1, 1], label='zeros', zorder=1)
    ax.plot([data2[0], data2[1]], [1, 1], label='ones', zorder=1)
    ax.scatter([data1[0], data1[1]], [1, 1], zorder=2)
    ax.scatter([data2[0], data2[1]], [1, 1], zorder=2)

    dot1 = float('{:.2f}'.format(data1[0]))
    dot2 = float('{:.2f}'.format(data1[1]))
    dot3 = float('{:.2f}'.format(data2[0]))
    dot4 = float('{:.2f}'.format(data2[1]))

    x1, x2, x3, x4 = get_x([data1[0], data1[1], data2[0], data2[1]], locator)

    ax.annotate(f'{dot1}', (data1[0], 1), xytext=(x1, 1 + 0.007))
    ax.annotate(f'{dot2}', (data1[1], 1), xytext=(x2, 1 + 0.007))
    ax.annotate(f'{dot3}', (data2[0], 1), xytext=(x3, 1 - 0.007))
    ax.annotate(f'{dot4}', (data1[1], 1), xytext=(x4, 1 - 0.007))

    plt.legend()
    plt.savefig(f'plots/{name}.png')
    # plt.show()


def get_interval_to_variance_by_unknown_mean_and_variance(data):
    variance = np.var(data)
    n = len(data)
    return n * variance / chi2.ppf((1 + alpha) / 2, n - 1), n * variance / chi2.ppf((1 - alpha) / 2, n - 1)


def get_interval_to_mean_by_unknown_mean_and_variance(data):
    mean = np.mean(data)
    param = (math.sqrt(np.var(data)) / math.sqrt(len(data) - 1)) * t.ppf((1 + alpha) / 2, len(data) - 1)
    return mean - param, mean + param


def get_interval_to_mean_normal_distr(data):
    mean = np.mean(data)
    variance = math.sqrt(np.mean(data))
    ppf = norm.ppf((1 + alpha) / 2)
    sqrt_n = math.sqrt(len(data))

    return mean - (variance * ppf) / sqrt_n, mean + (variance * ppf) / sqrt_n


def get_interval_to_variance_normal_distr(data):
    T2 = getT2(data)
    return T2 / chi2.ppf((1 + alpha) / 2, len(data)), T2 / chi2.ppf((1 - alpha) / 2, len(data))


def get_interval_to_mean_exponential_distribution(data):
    x1 = sorted(data)[0]
    n = len(data)
    return x1 + (1 / n) * math.log((1 - alpha) / 2), x1 + (1 / n) * math.log((1 + alpha) / 2)


def get_interval_to_var(data):
    var = np.var(data)
    param = F * math.sqrt((get_m4(data) - var * var) / len(data))
    return var - param, var + param


def get_m4(data):
    mean = np.mean(data)
    sum = 0
    for x in data:
        sum += math.pow((x - mean), 4)
    return sum / len(data)


def get_interval_to_mean(data):
    mean = np.mean(data)
    param = math.sqrt(np.var(data) / len(data)) * F

    return mean - param, mean + param


def get_interval_to_Ex_minus_Ey(data1, data2):
    n = len(data1)
    m = len(data2)
    param = t.ppf((1 + alpha) / 2, (m / n) - 2)
    means_diff = np.mean(data1) - np.mean(data2)
    param2 = math.sqrt(((m + n) / (n * m * (m + n - 2))) * (n * np.var(data1) + m * np.var(data2)))

    return means_diff - param * param2, means_diff + param * param2


def get_interval_to_Dx_div_Dy(data1, data2):
    n = len(data1)
    m = len(data2)
    ppf1 = t.ppf((1 + alpha) / 2, n - 1, m - 1)
    ppf2 = t.ppf((1 - alpha) / 2, n - 1, m - 1)

    param = (n * (m - 1) * np.var(data1)) / (m * (n - 1) * np.var(data2))

    return param / ppf1, param / ppf2


def get_plot(interval, name):
    fig, ax = plt.subplots()
    plt.title(name)

    ax.plot([interval[0], interval[1]], [1, 1], zorder=1)
    ax.scatter([interval[0], interval[1]], [1, 1], zorder=2)

    # ax.annotate(f'{dot1}', (data1[0], 1), xytext=(x1, 1 + 0.007))
    # ax.annotate(f'{dot2}', (data1[1], 1), xytext=(x2, 1 + 0.007))
    # ax.annotate(f'{dot3}', (data2[0], 1), xytext=(x3, 1 - 0.007))
    # ax.annotate(f'{dot4}', (data1[1], 1), xytext=(x4, 1 - 0.007))

    plt.legend()
    plt.savefig(f'plots/{name}.png')
    # plt.show()


if __name__ == "__main__":
    zeros_data, ones_data = read_data()

    variance_zeros = np.var(zeros_data)
    variance_ones = np.var(ones_data)
    mean_zeros = np.mean(zeros_data)
    mean_ones = np.mean(ones_data)

    # 1
    interval_to_mean_By_unknown_var_and_mean_zeros = get_interval_to_mean_by_unknown_mean_and_variance(zeros_data)
    interval_to_mean_By_unknown_var_and_mean_ones = get_interval_to_mean_by_unknown_mean_and_variance(ones_data)
    get_plot_to_interval(interval_to_mean_By_unknown_var_and_mean_zeros,
                         interval_to_mean_By_unknown_var_and_mean_ones,
                         "interval_to_mean_By_unknown_var_and_mean")

    i1 = Interval()
    i1.interval = interval_to_mean_By_unknown_var_and_mean_zeros
    i1.name = "Interval to mean by unknown variance and mean for zeros data"
    i1.right_param = mean_zeros

    i2 = Interval()
    i2.interval = interval_to_mean_By_unknown_var_and_mean_ones
    i2.name = "Interval to mean by unknown variance and mean for ones data"
    i2.right_param = mean_ones

    # 2
    interval_to_var_By_unknown_var_and_mean_zeros = get_interval_to_variance_by_unknown_mean_and_variance(zeros_data)
    interval_to_var_By_unknown_var_and_mean_ones = get_interval_to_variance_by_unknown_mean_and_variance(ones_data)
    get_plot_to_interval(interval_to_var_By_unknown_var_and_mean_zeros,
                         interval_to_var_By_unknown_var_and_mean_ones,
                         "interval_to_variance_By_unknown_var_and_mean")

    i3 = Interval()
    i3.interval = interval_to_var_By_unknown_var_and_mean_zeros
    i3.name = "Interval to variance by unknown variance and mean for zeros data"
    i3.right_param = variance_zeros

    i4 = Interval()
    i4.interval = interval_to_var_By_unknown_var_and_mean_ones
    i4.name = "Interval to variance by unknown variance and mean for ones data"
    i4.right_param = variance_ones

    # 3
    interval_to_var_zeros = get_interval_to_variance_normal_distr(zeros_data)
    interval_to_var_ones = get_interval_to_variance_normal_distr(ones_data)
    get_plot_to_interval(interval_to_var_zeros, interval_to_var_ones, "interval_to_variance")

    i5 = Interval()
    i5.interval = interval_to_var_zeros
    i5.name = "Interval to variance for zeros data"
    i5.right_param = variance_zeros

    i6 = Interval()
    i6.interval = interval_to_var_ones
    i6.name = "Interval to variance for ones data"
    i6.right_param = variance_ones

    # 4
    interval_to_mean_zeros = get_interval_to_mean_normal_distr(zeros_data)
    interval_to_mean_ones = get_interval_to_mean_normal_distr(ones_data)
    get_plot_to_interval(interval_to_mean_zeros, interval_to_mean_ones, "interval_to_mean")

    i7 = Interval()
    i7.interval = interval_to_mean_zeros
    i7.name = "Interval to mean for zeros data"
    i7.right_param = mean_zeros

    i8 = Interval()
    i8.interval = interval_to_mean_ones
    i8.name = "Interval to mean for ones data"
    i8.right_param = mean_ones

    # 5
    interval_to_mean_exp_distr_zeros = get_interval_to_mean_exponential_distribution(zeros_data)
    interval_to_mean_exp_distr_ones = get_interval_to_mean_exponential_distribution(ones_data)
    get_plot_to_interval(interval_to_mean_exp_distr_zeros,
                         interval_to_mean_exp_distr_ones,
                         "interval to mean exp distr case")

    i9 = Interval()
    i9.interval = interval_to_mean_exp_distr_zeros
    i9.name = "Interval to mean for zeros data in exp distr case"
    i9.right_param = mean_zeros

    i10 = Interval()
    i10.interval = interval_to_mean_exp_distr_ones
    i10.name = "Interval to mean for ones data in exp distr case"
    i10.right_param = mean_ones

    # 6
    interval_to_mean_z = get_interval_to_mean(zeros_data)
    interval_to_mean_o = get_interval_to_mean(ones_data)
    get_plot_to_interval(interval_to_mean_z, interval_to_mean_o, "interval_to_mean_large_N")

    i11 = Interval()
    i11.interval = interval_to_mean_z
    i11.name = "Interval to mean for zeros data in large N case"
    i11.right_param = mean_zeros

    i11 = Interval()
    i11.interval = interval_to_mean_o
    i11.name = "Interval to mean for ones data in large N case"
    i11.right_param = mean_ones

    interval_to_var_z = get_interval_to_var(zeros_data)
    interval_to_var_o = get_interval_to_var(ones_data)
    get_plot_to_interval(interval_to_var_z, interval_to_var_o, "interval_to_variance_large_N")

    # 7
    i12 = Interval()
    i12.interval = interval_to_var_z
    i12.name = "Interval to variance in large N case for zeros data"
    i12.right_param = variance_zeros

    i13 = Interval()
    i13.interval = interval_to_var_o
    i13.name = "Interval to variance in large N case for ones data"
    i13.right_param = variance_ones

    # 8
    interval_diff_Ex_Ey = get_interval_to_Ex_minus_Ey(zeros_data, ones_data)
    get_plot(interval_diff_Ex_Ey, "Ex minus Ey")

    i14 = Interval()
    i14.interval = interval_diff_Ex_Ey
    i14.name = "Ex minus Ey"
    i14.right_param = mean_zeros - mean_ones

    interval_div_Dx_Dy = get_interval_to_Dx_div_Dy(zeros_data, ones_data)
    get_plot(interval_div_Dx_Dy, "Dx div Dy")

    i15 = Interval()
    i15.interval = interval_div_Dx_Dy
    i15.name = "Dx div Dy"
    i15.right_param = variance_zeros / variance_ones

    intervals = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15]

    for i in intervals:
        print(i)





