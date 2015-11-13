import random, scipy.stats
import matplotlib.pyplot as plt
def lowerUpperBoundary(varsy, slackFraction):
    varsyMax = max(varsy)
    varsyMin = min(varsy)
    slack = (varsyMax - varsyMin) * slackFraction
    return varsyMin - slack, varsyMax + slack

def bestFitLine(leftBorder, rightBorder, intercept, slope):
    lowY = leftBorder * slope + intercept
    highY = rightBorder * slope + intercept
    return [leftBorder, rightBorder], [lowY, highY]


def makePlot(independentVar, dependentVar, independentVarName, dependentVarName, plotname):
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(independentVar, dependentVar)

    leftBorder, rightBorder = lowerUpperBoundary(independentVar, 0.1)

    leftBorderLine, rightBorderLine = lowerUpperBoundary(independentVar, 0.05)

    bottomBorder, topBorder = lowerUpperBoundary(dependentVar, 0.1)

    xs, ys = bestFitLine(leftBorderLine, rightBorderLine, intercept, slope)



    fig = plt.figure()
    #fig.suptitle('sample correlation', fontsize=12)

    ax = fig.add_subplot(111)
    fig.subplots_adjust(left=0.2, bottom=0.4)
    ax.set_title('Sample correlation', fontsize=16)
    d1 = 'best fit line slope: ' + '%.3g' % slope + "\n"
    d2 = 'best fit line r-value: ' + '%.3g' % r_value + "\n"
    d3 = 'best fit line p-value: ' + '%.3g' % p_value + "\n"
    d4 = 'best fit line standard error: ' + '%.3g' % std_err + "\n"
    
    fig.text(0.12, 0.02, d1 + d2 + d3 + d4 , fontsize=16)
    
    ax.set_xlabel(independentVarName, fontsize = 18)
    ax.set_ylabel(dependentVarName, fontsize = 18)
    
    ax.plot(independentVar, dependentVar, 'ro') # plots all points, red dots
    ax.plot(xs, ys) # shows line of best fit
    ax.axis([leftBorder, rightBorder, bottomBorder, topBorder]) # creates canvas

    if slope < 0:
        print("independentVar is negatively correlated to dependentVar in our sample")
    else:
        print("independentVar is positvely correlated to dependentVar in our sample")

    plt.savefig(plotname)

import os.path, os, sys

dependentDir = sys.argv[2]

independentDir = sys.argv[1]

def allFilenames(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        yield os.path.join(dirname, filename), filename

def processFile(absoluteFilePath):
    variables = []
    with open(absoluteFilePath) as myFile:
        for index, line in enumerate(myFile):
            print(index, line)
            if index == 0:
                varName = str(line)
                isFirst = False
            else:
                variables.append(float(line))
    return varName, variables
            
for indFilename, indRel in allFilenames(independentDir):
    indName, indVar = processFile(indFilename)
    for depFilename, depRel in allFilenames(dependentDir):
        depName, depVar = processFile(depFilename)
        makePlot(indVar, depVar, indName, depName, os.path.join("plots", depRel + indRel + ".png"))

