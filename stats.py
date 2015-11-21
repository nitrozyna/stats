import random, scipy.stats
import matplotlib.pyplot as plt
import os.path, os, sys

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
    global figureNo
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(independentVar, dependentVar)

    leftBorder, rightBorder = lowerUpperBoundary(independentVar, 0.1)

    leftBorderLine, rightBorderLine = lowerUpperBoundary(independentVar, 0.05)

    bottomBorder, topBorder = lowerUpperBoundary(dependentVar, 0.3)

    xs, ys = bestFitLine(leftBorderLine, rightBorderLine, intercept, slope)



    fig = plt.figure(figsize=(10, 5))

    verticalBar = scipy.std(dependentVar)

    horizontalBar = scipy.std(independentVar)    

    ax = fig.add_subplot(111)
    fig.subplots_adjust(left=0.15, bottom=0.4, top=0.85)
    ax.set_title(descriptions[figureNo] + '\n', fontsize=16)
    figureNo += 1
    d1 = 'Best fit line slope: ' + '%.3g' % slope + "\n"
    d2 = "Pearson's coefficient-value: " + '%.3g' % r_value + "\n"
    d3 = 'Null hypothesis p-value: ' + '%.3g' % p_value + "\n"
    
    fig.text(0.12, 0.02, d1 + d2 + d3 , fontsize=16)
    
    ax.set_xlabel(independentVarName, fontsize = 18)
    ax.set_ylabel(dependentVarName, fontsize = 18)
    
    ax.plot(xs, ys, label='line of best fit') # shows line of best fit
    #fig.suptitle('sample correlation', fontsize=12)
    ax.errorbar(independentVar, dependentVar, yerr=verticalBar, fmt='go', label='individuals')
    ax.legend(loc=(0.74, -0.72), shadow=True, fancybox=True)
    ax.axis([leftBorder, rightBorder, bottomBorder, topBorder]) # creates canvas

    if slope < 0:
        print("independentVar is negatively correlated to dependentVar in our sample")
    else:
        print("independentVar is positvely correlated to dependentVar in our sample")

    plt.savefig(plotname)


figureNo = int(sys.argv[3])
descriptions = ["Correlation between BMI and Energy Balance in females", "Correlation between Body Fat and Energy Balance in females", "Correlation between Waist to Hip Ratio and Energy Balance in females"]
descriptions += [stringa[:-7] + "males" for stringa in descriptions]

dependentDir = sys.argv[2]

independentDir = sys.argv[1]

def allFilenames(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        yield os.path.join(dirname, filename), filename

def processFile(absoluteFilePath):
    variables = []
    with open(absoluteFilePath) as myFile:
        print(absoluteFilePath)
        for index, line in enumerate(myFile):
            if index == 0:
                varName = str(line)
                isFirst = False
            else:
                variables.append(float(line))
    return varName, variables

indFilenames = list(allFilenames(independentDir))
indFilenames.sort()
depFilenames = list(allFilenames(dependentDir))
depFilenames.sort()

for indFilename, indRel in indFilenames:
    indName, indVar = processFile(indFilename)
    for depFilename, depRel in depFilenames:
        depName, depVar = processFile(depFilename)
        makePlot(indVar, depVar, indName, depName, os.path.join("plots", depRel + indRel + ".png"))

