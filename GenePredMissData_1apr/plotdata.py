import sys
from classes.plotter import Plotter
import datetime


def interpfile(filename):
    title = ""
    try:
        file = open(filename, "r")
    except:
        print("Could not open file")
    lines = file.readlines()
    file.close()
    legends = []
    plotconfig = []
    data = []
    for line in lines:
        sp = line.split()
        key = sp[0].strip(":")
        if len(sp) > 1:
            if key == "title":
                title = sp[1].strip()
            if key == "legend":
                legends.append(":".join(sp[1:]).strip())
                plotconfig.append(["", ""])
            if key == "linetype":
                plotconfig[-1][1] = sp[1].strip()
            if key == "color":
                plotconfig[-1][0] = sp[1].strip()
        if sp[0].isnumeric():
            speval = line.split(";")
            evals = {}
            frac = 0
            for spe in speval:
                spesp = spe.strip().split("\t")
                if len(spesp) > 1:
                    frac = int(spesp[0])
                    evals[spesp[1]] = float(spesp[2])
            data.append((frac, evals))
    return title, plotconfig, legends, data
                
def plot(title, plotconfig, legends, data):
    plotter = Plotter()
    for frac in data:
        plotter.add_score(frac[0], frac[1])
    extrastring = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    plotter.plot_performance(title, legends, plotconfig, extrastring)
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("Give results file")
        exit()
    title, plotconfig, legends, data = interpfile(filename)
    print("title:", title)
    print("plotconfig:", plotconfig)
    print("legends:", legends)
    for frac in data:
        print(frac[0], frac[1])
    plot(title, plotconfig, legends, data)
    
    
