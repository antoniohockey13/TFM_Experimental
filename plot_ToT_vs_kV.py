import ROOT
import click
import os
import numpy as np
import matplotlib.pyplot as plt

# CONSTANTS
FORMAT = ".png"
save_plots = False
omit_plots = False
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(111111)

def get_cal(file, cut=""):
    cal = ROOT.TH1F("calibration", "", 1024, 1, 1024)
    file.Hits.Project("calibration", "cal", cut)
    max_bin = cal.GetMaximumBin()
    return max_bin


@click.command()
@click.argument('inputfiles', nargs=-1)
def main(inputfiles):
    if save_plots:
        input_name = inputfile.split('/')
        input_name[-1] = input_name[-1].split('.')[0]
        folder = "/".join(input_name[1:-1])
        os.makedirs(f"Pictures/{folder}", exist_ok=True)
    
    mean = {}
    median = {}
    mode = {}
    voltages_kV = [10,15,20,35,30,35]    

    for irow in range(6,10):
        c = ROOT.TCanvas(f"c{irow}", f"c{irow}")
        legend = ROOT.TLegend(0.1,0.7,0.48,0.9)
        tot_calibrated = []

        
        for i, inputfile in enumerate(reversed(inputfiles)):
            file = ROOT.TFile(inputfile)
            max_bin_value = get_cal(file, f"row=={irow}")
            if i == 0:
                opt = ""
            if i > 0:
                opt = "same"
            file.Hits.SetLineColor(i+1)
            # Change limits
            tot_calibrated.append(ROOT.TH1F(f"tot_calibrated_{i}", "", 100, 0, 10)) 
            file.Hits.Project(f"tot_calibrated_{i}", "tot_cal", f"row == {irow} && cal-{max_bin_value}<2.5")
            tot_calibrated[-1].SetDirectory(0) 
            # Statistics values
            mean[irow] = tot_calibrated[-1].GetMean()
            median[i] = getMedian(tot_calibrated[-1])
            mode[i] = tot_calibrated[-1].GetBinCenter(tot_calibrated[-1].GetMaximumBin())
            # Plot
            tot_calibrated[-1].Scale(1.0 / tot_calibrated[-1].Integral(), "HIST") 
            tot_calibrated[-1].SetTitle("ToT Calibrated for Different Voltages")
            tot_calibrated[-1].GetXaxis().SetTitle("ToT/ns")
            tot_calibrated[-1].GetYaxis().SetTitle("Entries")
            legend.AddEntry(tot_calibrated[-1], f"{inputfile}", "l")
            tot_calibrated[-1].SetLineColor(i+1)
            tot_calibrated[-1].Draw(f"HIST {opt}")
            file.Close()

        legend.Draw()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/tot_calibrated_for_different_kV_row_{irow}.{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")
        
    if not omit_plots:
        for i in range(6,10):
            plt.plot(voltages_kV, mean[i], 'o-', label="Mean")
            plt.plot(voltages_kV, median[i], 'o-', label="Median")
            plt.plot(voltages_kV, mode[i], 'o-', label="Mode")
        plt.xlabel('Voltage [V]')
        plt.ylabel('ToT/ns')
        plt.title('Voltage vs ToT')
        plt.legend()
        plt.show()
        input("Press Enter to continue...")



def getMedian(histo1):
    numBins = histo1.GetXaxis().GetNbins()
    y = np.array([])
    for i in range(numBins):
        x = histo1.GetBinCenter(i)
        for ix in range(int(histo1.GetBinContent(i))):
            y = np.append(y, x)
    return np.median(y)

if __name__ == '__main__':
    main()