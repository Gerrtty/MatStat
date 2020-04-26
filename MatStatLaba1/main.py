import matplotlib.pyplot as plt

import numpy as np
from openpyxl import load_workbook
import statistics
import matplotlib.ticker as ticker

def read_data():
    zeros_data = []
    ones_data = []
    all_data = []
    boolean_arr = []

    wb = load_workbook('data.xlsx')
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

def sort_and_print(arr, name):
    new_arr = sorted(arr)
    print(f"Sorted data {name}:")
    print(new_arr)
    print()
    return new_arr

def numeric_characteristics(data):
    maximum = max(data)
    minimum = min(data)
    mean = statistics.mean(data)
    med = statistics.median(data)
    quantil_1 = np.quantile(data, 0.25)
    quantil_2 = np.quantile(data, 0.75)
    var = np.var(data)
    csv = statistics.variance(data)

    return maximum, minimum, mean, med, quantil_1, quantil_2, var, csv

def print_numeric_characteristics(data, name):

    maximum, minimum, mean, med, quantil_1, quantil_2, var, crv = numeric_characteristics(data)

    print(f"\033[32m Min in {name} array = {minimum}")
    print(f"Max in {name} array = {maximum}")
    print(f"Med in {name} array = {med}")
    print(f"Quantil 1/4 in {name} array = {quantil_1}")
    print(f"Quantil 3/4 in {name} array = {quantil_2}")
    print(f"Variance in {name} array = {var}")
    print(f"Corrected sample variance in {name} array = {crv}")
    print()

def variance(data):
    sum = 0
    mean = np.mean(data)
    for d in data:
        x = d - mean
        sum += x*x

    return (1 / (len(data))) * sum

def cv(data):
    sum = 0
    mean = np.mean(data)
    for d in data:
        x = d - mean
        sum += x * x

    return (1 / (len(data) - 1)) * sum

def plot_hist(data1, data2):
    fig, ax = plt.subplots()

    ax.xaxis.set_major_locator(ticker.MultipleLocator(50))

    ax.hist(ones_data, bins=len(data1), rwidth=1)

    ax.hist(zeros_data, bins=len(data2), rwidth=0.4)

    plt.savefig("hist.png")
    plt.show()

def plot_box_plot(data1, data2):

    data = [data1, data2]

    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
    ax.boxplot(data, vert=False)

    plt.savefig("boxplot.png")
    plt.show()


if __name__ == "__main__":

    zeros_data, ones_data = read_data()

    ones_data = sort_and_print(ones_data, "ones")
    print_numeric_characteristics(ones_data, "ones")

    zeros_data = sort_and_print(zeros_data, "zeros")
    print_numeric_characteristics(zeros_data, "zeros")

    plot_hist(ones_data, zeros_data)
    plot_box_plot(zeros_data, ones_data)




