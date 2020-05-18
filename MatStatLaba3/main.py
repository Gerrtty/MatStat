from read_data import read_data
from scipy.stats import normaltest
from scipy.stats import kstest
from scipy.stats import ks_2samp
from scipy.stats import ttest_ind
from scipy.stats import wilcoxon
from scipy.stats import chi2_contingency
from scipy.stats import mannwhitneyu as w
from scipy.stats import f
from scipy.stats import t
import numpy as np
import math

alfa = 0.05
critial_u = 0

def hi2_test(data, name):
    print(f"Hi^2 test of {name} data")
    test = normaltest(data)

    print(test)

    if test[1] < 0.05:
        print("Ho отвергается т.к p-value < 0.05")
        print("Распределение не является нормальным")
    else:
        print(f"Ho принимается т.к p-value > 0.05")
        print("Распределение является нормальным")

    print()

    return test


def ks_test(data, name):
    print(f"Kolmogorov test of {name} data")

    test = kstest(data, 'norm', (np.mean(data), np.var(data)))

    print(test)

    if test[1] < 0.05:
        print("Ho отвергается т.к p-value < 0.05")
        print("Распределение не является нормальным")
    else:
        print(f"Ho принимается т.к p-value > 0.05")
        print("Распределение является нормальным")

    print()

    return test


def student_test(data1, data2):
    print("Student test of Ex = Ey")
    n, m = len(data1), len(data2)

    criteria = t.cdf((1 - alfa) / 2, len(data1) + len(data2) - 2)

    # test = ttest_ind(data1, data2)

    test = ((np.mean(data1) - np.mean(data2)) * math.sqrt(n * m *(n + m - 2))) \
           / (math.sqrt((n + m) * (n * np.var(data1) + m * np.var(data2))))

    if test > criteria:
        print(f"Ho отвергается т.к значение > {criteria}")
        print("Ex != Ey")
    else:
        print(f"Ho подтверждается т.к значение < {criteria}")
        print("Ex = Ey")

    print()

    return criteria, test


def fisher_test(data1, data2):
    print("Fisher test of Dx = Dy")
    n, m = len(data1), len(data2)

    F = (n * (m - 1) * np.var(data1)) / (m * (n - 1) * np.var(data2))

    interval = [f.cdf(alfa / 2, n - 1, m - 1), f.cdf(1 - alfa / 2, n - 1, m - 1)]

    s = f"принадлежит интервалу [{interval[0]}; {interval[1]}]"

    if interval[0] < F < interval[1]:
        print(f"Ho подтверждается т.к. значение " + s)
        print("Dx = Dy")
    else:
        print("Ho отвергается т.к значение не " + s)
        print("Dx != Dy")

    print()

    return F, interval


def wilcoxon_test(data1, data2):
    n, m = len(data1), len(data2)
    test = w(data1, data2)

    Uobt = test[0]

    crit = abs(Uobt - (n * m / 2)) / math.sqrt((n * m * (n + m + 1)) / 12)

    print(f"Wilcoxon test of equals of two distribution {test}")

    if test[1] < crit:
        print(f"Ho отвергается т.к значение < {crit}")
        print("Данные принадлежат разным распределениям")
    else:
        print(f"Ho принимается т.к значене > {crit}")
        print("Данные принадлежат одному распределению")

    print()


def my_sort(tup):
    return tup[1]


def table(bollean_arr, all_data):

    arr = []

    for i in range(0, len(boolean_arr)):
        arr.append((boolean_arr[i], all_data[i]))

    arr = sorted(arr, key=my_sort)

    delitemer = int(len(arr) / 3) + 1

    arr = [arr[0:delitemer], arr[delitemer: delitemer * 2], arr[delitemer * 2:]]

    print(np.array(arr))

    h_z = [0, 0, 0]
    h_o = [0, 0, 0]

    for i in range(len(arr)):
        a = arr[i]
        for j in range(len(a)):
            if a[j][0] == 0:
                h_z[i] += 1
            else:
                h_o[i] += 1

    table = [h_z, h_o]
    print(np.array(table))

    stat, p, dof, expected = chi2_contingency(table)

    print(f"stat = {stat}")
    print(f"p = {p}")
    print(f"dof = {dof}")

    if(stat < dof):
        print("Ho принимается")
        print("Данные зависимы")
    else:
        print("Ho отвергается")
        print("Данные не зависимы")

    print()


if __name__ == "__main__":
    zeros_data, ones_data, boolean_arr, all_data = read_data()

    print(len(zeros_data))
    print(len(ones_data))
    # raise Exception

    print(f"Mean of zeros = {np.mean(zeros_data)}")
    print(f"Mean of ones = {np.mean(ones_data)}")
    print(f"Variance of zeros = {np.var(ones_data)}")
    print(f"Variance of ones = {np.var(zeros_data)}")
    print()

    hi2_test(zeros_data, "zeros")
    hi2_test(ones_data, "ones")

    ks_test(zeros_data, "zeros")
    ks_test(ones_data, "ones")

    student_test(zeros_data, ones_data)
    fisher_test(zeros_data, ones_data)

    wilcoxon_test(zeros_data, ones_data)

    table(boolean_arr, all_data)