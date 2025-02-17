import csv, os, re, pprint
import numpy as np
import matplotlib.pyplot as plt

def getdata(csvfile):

    popdata = {}

    with open(csvfile, 'r') as file:
        next(file)
        data = [row for row in csv.reader(file)]

    for row in data:
        population = row[4:len(row)-1]
        popdata[row[1]] = population

    return popdata

def plotarray(data):

    jpnpoints = data["JPN"]
    jpn_xpoints = list(range(len(jpnpoints)))
    jpn_sypoints = np.array(jpnpoints)
    jpn_ypoints = [int(element) for element in jpn_sypoints]

    frapoints = data["FRA"]
    fra_xpoints = list(range(len(frapoints)))
    fra_sypoints = np.array(frapoints)
    fra_ypoints = [int(element) for element in fra_sypoints]

    plt.plot(jpn_xpoints, jpn_ypoints)
    plt.plot(fra_xpoints,fra_ypoints)

    plt.show()

def main():

    popdata = getdata('[CSVFILE]')
    plotarray(popdata)

if __name__ == '__main__':
    main()

