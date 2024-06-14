import sifca_utils
import ROOT
import scipy.constants as const
import click
import os
import matplotlib.pyplot as plt
import numpy as np
from array import array

sifca_utils.plotting.set_sifca_style()

#CONSTANTS
FORMAT = ".pdf"
save_plots = True
omit_plots = False
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
    cal = ROOT.TH1F("calibration", "", 1024, 0, 1023)
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
    histo.Draw("PE")
    legend.AddEntry(histo, f"ToT measured", "l")
    fit_gaus = ROOT.TF1("fit_gaus", "gaus", 2, 5)
    histo.Fit(fit_gaus, "R")
    # fit_gaus.Draw("same")
    max = fit_gaus.GetParameter(1)
### Change 1.5*max to optimise the fit ###
    fit = ROOT.TF1("fit", f"[0]*exp([1]*x+[2])", 1.6*max, 8)
    fit.SetParameter(0, 2e4)
    fit.SetParameter(1, -3)    
    file.Hits.Project("calibration", "cal", cut)
    fit.SetParameter(2, 15)
    histo.Fit(fit, "R")
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
    error = {}

    for irow in range(6,10):
        low_value[irow] = []
        error[irow] = []
        V = []
        for i, file in enumerate(inputfiles):
            V.append(int(file.split('/')[-1].split("_")[0]))
            print(f"Voltage: {V[-1]}kV \n Row {irow}")
            folder = ""   
            input_name = file.split('/')
            input_name[-1] = input_name[-1].split('.')[0]
            folder = f"{input_name[1]}/{input_name[-1]}"
            if save_plots:
                os.makedirs(f"Pictures/{folder}", exist_ok=True) 

            f = ROOT.TFile(file)
            max_bin = get_cal(f, f"row=={irow}")
            # fit to exponential y = A e^(Bx+C)
            fit = tot_fit_histogram(f,f"c_row_{irow}", f"abs({max_bin}-cal)<2.5 && row == {irow}", V[i], f"ToT_fit_row{irow}", folder)
            # Select max value of ToT when fit = e ^-1
            low_value[irow].append((np.log(fit.GetParameter(0))+fit.GetParameter(2)+1)/-fit.GetParameter(1))
            # Error calculation
            dx_da = -1/(fit.GetParameter(0)*fit.GetParameter(1))
            dx_db = (np.log(fit.GetParameter(0))+fit.GetParameter(2)+1)/(fit.GetParameter(1)**2)
            dx_dc = -1/(fit.GetParameter(1))
            error[irow].append(np.sqrt(dx_da**2*fit.GetParError(0)**2 + dx_db**2*fit.GetParError(1)**2 + dx_dc**2*fit.GetParError(2)**2))
                               


    ROOT.gROOT.SetBatch(False)
    fit = {}
    points = {}
    c_fit = ROOT.TCanvas("c_fit", "c_fit", 800, 600)
    limits = ROOT.TH2F("limits", "limits", 1, 0, 40,1, 4, 10)
    limits.Draw()
    legend = ROOT.TLegend(0.2, 0.7, 0.5, 0.9)
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kOrange]

    for i, irow in enumerate(range(6, 10)):
        print(f"\n ****************************\n Row {irow}")
        points[irow] = ROOT.TGraphErrors(len(V), array('d', V), array('d', low_value[irow]), array('d', [0.1]*len(V)), array('d', error[irow]))
        # points[irow] = ROOT.TGraph(len(V), array('d', V), array('d', low_value[irow]))
        points[irow].SetMarkerStyle(20)
        points[irow].SetMarkerSize(1)
        points[irow].SetMarkerColor(colors[i])
        points[irow].SetLineColor(colors[i])
        points[irow].Draw("P") 

        legend.AddEntry(points[irow], f"Row {irow}", "p")

        fit[irow] = ROOT.TF1(f"fit{irow}", "pol1", 0, 40)
        for idx in range(len(V)):
            points[irow].SetPointError(idx, 0.1, error[irow][idx])
        points[irow].Fit(fit[irow], "R")
        fit[irow].SetLineColor(colors[i])
        fit[irow].Draw("Same")

    legend.Draw()
    limits.GetXaxis().SetTitle("Voltage /kV")
    limits.GetYaxis().SetTitle("Max ToT/ns")
    c_fit.Update()
    if save_plots:
        c_fit.SaveAs(f"Pictures/2024-05-23_Array_Test_Results/MaxTot_V{FORMAT}")
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()
