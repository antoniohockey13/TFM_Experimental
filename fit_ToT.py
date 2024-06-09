import sifca_utils
import ROOT
import scipy.constants as const
import click
import os
import matplotlib.pyplot as plt
import numpy as np

sifca_utils.plotting.set_sifca_style()

#CONSTANTS
FORMAT = ".pdf"
save_plots = False
omit_plots = True 
ROOT.gROOT.SetBatch(omit_plots)
# ROOT.gStyle.SetOptStat(111111)
ROOT.gStyle.SetOptStat(0)
h = const.Planck
c = const.speed_of_light
e = const.elementary_charge

# UNITS
kV = 1
V = 1e-3*kV

def get_cal(file, cut=""):
    cal = ROOT.TH1F("calibration", "", 1024, 1, 1024)
    file.Hits.Project("calibration", "cal", cut)
    max_bin = cal.GetMaximumBin()
    return max_bin

def tot_fit_histogram(file, canvas_name, cut, V, file_name, folder):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    legend = ROOT.TLegend(0.7,0.8,0.9,0.9)
    c.SetLogy()
    histo = ROOT.TH1F("histo", "", 100, 0, 10)
    file.Hits.Project("histo", "tot_cal", cut)
    histo.GetXaxis().SetTitle("ToT/ns")
    histo.GetYaxis().SetTitle("Entries")
    histo.Draw()
    legend.AddEntry(histo, f"ToT measured", "l")
    fit_gaus = ROOT.TF1("fit_gaus", "gaus", 2, 5)
    histo.Fit(fit_gaus, "R")
    # fit_gaus.Draw("same")
    max = fit_gaus.GetParameter(1)

######## Cambiar valor de 1.3 para encontrar el óptimo ###########

    fit = ROOT.TF1("fit", f"[0]*exp([1]*x+[2])", 1.5*max, 10)
    fit.SetParameter(0, 2e4)
    fit.SetParameter(1, -3)
    fit.SetParameter(2, 15)
    histo.Fit(fit, "RS")
    fit.Draw("same")
    fit.SetLineColor(ROOT.kRed)
    legend.AddEntry(fit, f"Fit exponential", "l")
    legend.Draw()
    c.Update()
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")
    return fit

def tot_fit_gauss(file, canvas_name, cut, file_name, folder, percentage):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    histo = ROOT.TH1F("histo", "", 100, 0, 10)
    file.Hits.Project("histo", "tot_cal", cut)
    histo.Draw()
    fit = ROOT.TF1("fit", "gaus", 0, 10)    
    histo.Fit(fit)
    fit.Draw("same")
    c.Update()
    mean = fit.GetParameter(1)
    mean_error = fit.GetParError(1)
    max_value = fit.GetMaximum()
    limit_value = percentage*max_value
    limit = fit.GetX(limit_value, xmin=mean, xmax=10)
    print(limit)
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")
    return limit





@click.command()
@click.argument("inputfiles", nargs=-1)
def main(inputfiles):
    low_value = {}
    plot_fit = {}
    V = [35*kV, 30*kV, 25*kV, 20*kV, 15*kV, 10*kV]

    for irow in range(6,10):
        low_value[irow] = []
        for i, file in enumerate(inputfiles):
            folder = ""   
            input_name = file.split('/')
            input_name[-1] = input_name[-1].split('.')[0]
            folder = f"{input_name[1]}/{input_name[-1]}"
            if save_plots:
                os.makedirs(f"Pictures/{folder}", exist_ok=True) 

            f = ROOT.TFile(file)
            max_bin = get_cal(f, f"row=={irow}")
            fit = tot_fit_histogram(f,f"c_row_{irow}", f"abs({max_bin}-cal)<2.5 && row == {irow}", V[i], f"ToT_fit_row{irow}", folder)
            low_value[irow].append((np.log(fit.GetParameter(0))+fit.GetParameter(2)+1)/-fit.GetParameter(1))

        plt.scatter(V, low_value[irow], label=f"Row {irow}")

        low = np.array(low_value[irow])
        V = np.array(V)
        plot_fit[irow] = np.polyfit(V, low, 1)
        fit_line = np.polyval(plot_fit[irow], V)
        plt.plot(V, fit_line, label=f"Fit Row {irow}")
        plt.text(V[0], low[0], f"m = {plot_fit[irow][0]:.2f} b = {plot_fit[irow][1]:.2f}")

    plt.xlabel("Voltage/ kV")
    plt.ylabel("ToT/ns")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()