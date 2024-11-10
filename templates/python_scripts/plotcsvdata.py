import os, csv,pprint, re
import numpy as np
import matplotlib.pyplot as plt


def readcsv():

    adata = []
    cwd = os.getcwd()
    print(cwd)
    datacsv = cwd + "/[csv_file]"

    #read csv file
    with open(datacsv, encoding='utf-8') as csvf:
        reader = csv.reader(csvf)
        for row in reader:
            n = row[1]
            if not re.match("[A-Z][a-z]", n):
                adata.append(float(n))

    return adata


def plotarray(adata):

    # Plotting the graph
    xpoints = list(range(len(adata)))
    ypoints = np.array(adata)

    plt.plot(xpoints,ypoints)
    plt.show()


if __name__ == '__main__':
    adata = readcsv()
    #adata = [1, 4, 6, 7, 10]
    print(len(adata))
    plotarray(adata)
