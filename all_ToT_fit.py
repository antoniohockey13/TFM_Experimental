import ROOT
import sifca_utils
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

@click.command()
@click.argument('inputfiles', nargs=-1)
def main(inputfiles):
    Voltages = []
    # Value of max ToT and error
    low_value = []
    error = []
    for i, file in enumerate(inputfiles):
        Voltages.append(int(file.split('/')[-1].split("_")[0]))
        print(f"Voltage: {Voltages[-1]}kV")
        input_name = file.split('/')
        input_name[-1] = input_name[-1].split('.')[0]
        folder = f"{input_name[1]}/{input_name[-1]}"
        if save_plots:
            os.makedirs(f"Pictures/{folder}", exist_ok=True) 
        
        f = ROOT.TFile(file)
        df = ROOT.RDataFrame("Hits", f)
        cal = {}
        for irow in range(6,10):
            cal[irow] = get_cal(f, f"row=={irow}")
        # Filter df to cal+-1 for each row
        filtered_file = f"{folder}/filtered.root"
        df_filtered = df.Filter(" || ".join([f"row == {irow} && abs(cal - {cal[irow]}) < 2.5" for irow in range(6, 10)]))

        # Plot ToT histogram

        c = ROOT.TCanvas("c", "c")
        legend = ROOT.TLegend(0.65,0.75,0.9,0.9)
        c.SetLogy()
        # Data
        h = df_filtered.Histo1D(("histo", "", 100, 0, 10), "tot_cal")
        legend.AddEntry(h.GetPtr(), f"ToT measured", "l")
        h.Draw("PE")

        # Fit gaussian
        fit_gaus = ROOT.TF1("fit_gaus", "gaus", 2, 5)
        h.Fit(fit_gaus, "R")
        fit_gaus.SetLineColor(ROOT.kBlue)
        fit_gaus.SetLineStyle(9)
        # fit_gaus.Draw("same")
        # legend.AddEntry(fit_gaus, f"Gaussian fit", "l")
    
        max = fit_gaus.GetParameter(1)

        # Fit region 2
        # fit to exponential y = A e^(Bx+C)
        fit = ROOT.TF1("fit", f"[0]*exp([1]*x+[2])", 1.6*max, 8)
        fit.SetParameter(0, 2e4)
        fit.SetParameter(1, -3)
        fit.SetParameter(2, 15)
        h.Fit(fit, "R")
        fit.SetLineColor(ROOT.kRed)
        fit.Draw("same")
        legend.AddEntry(fit, f"Fit exponential to region 2", "l")

        legend.Draw()
        c.Update()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/All_ToT_together_{input_name[-1]}{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")
        # Select max value of ToT when fit = e ^-1
        low_value.append((np.log(fit.GetParameter(0))+fit.GetParameter(2)+1)/-fit.GetParameter(1))
        dx_da = -1/(fit.GetParameter(0)*fit.GetParameter(1))
        dx_db = (np.log(fit.GetParameter(0))+fit.GetParameter(2)+1)/(fit.GetParameter(1)**2)
        dx_dc = -1/(fit.GetParameter(1))
        error.append(np.sqrt(dx_da**2*fit.GetParError(0)**2 + dx_db**2*fit.GetParError(1)**2 + dx_dc**2*fit.GetParError(2)**2))
    
    print(low_value)
    print(error)

    # Plot max ToT vs Voltage
    fit = {}
    points = {}
    c_fit = ROOT.TCanvas("c_fit", "c_fit", 800, 600)
    limits = ROOT.TH2F("limits", "limits", 1, 0, 40,1, 4, 10)
    limits.Draw()
    legend = ROOT.TLegend(0.2, 0.7, 0.5, 0.9)
    # Define the linear function to fit
    points = ROOT.TGraphErrors(len(Voltages), array('d', Voltages), array('d', low_value), array('d', [0.1]*len(Voltages)), array('d', error))
    points.SetMarkerStyle(20)
    points.SetMarkerSize(1)
    points.Draw("P") 

    legend.AddEntry(points, f"Max ToT measured", "p")

    fit = ROOT.TF1(f"fit", "[0]+[1]*x", 0, 40)
    for idx in range(len(Voltages)):
        points.SetPointError(idx, 0.1, error[idx])
        points.Fit(fit, "R")
        fit.Draw("Same")
        # Compute R squared
        residuals = []
        for idx in range(len(Voltages)):
            residuals.append((low_value[idx]-fit.Eval(Voltages[idx]))**2)
        residuals = np.array(residuals)
        ss_res = np.sum(residuals)
        ss_tot = np.sum((np.array(low_value)-np.mean(low_value))**2)
        r_squared = 1 - (ss_res/ss_tot)
        print(f"R squared: {r_squared}")

    legend.Draw()
    limits.GetXaxis().SetTitle("Voltage /kV")
    limits.GetYaxis().SetTitle("Max ToT/ns")
    c_fit.Update()
    if save_plots:
        c_fit.SaveAs(f"Pictures/Analysis/MaxTot_V{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")


# Plot E vs Max ToT
    fit = {}
    points = {}
    c_fit = ROOT.TCanvas("c_fit", "c_fit", 800, 600)
    limits = ROOT.TH2F("limits", "limits", 1, 4, 10,1,0, 40)
    limits.Draw()
    legend = ROOT.TLegend(0.2, 0.7, 0.5, 0.9)
    # Define the linear function to fit
    points = ROOT.TGraphErrors(len(Voltages), array('d', low_value), array('d', Voltages), array('d', error), array('d', [0.1]*len(Voltages)))
    points.SetMarkerStyle(20)
    points.SetMarkerSize(1)
    points.Draw("P") 

    legend.AddEntry(points, f"Max ToT measured", "p")

    fit = ROOT.TF1(f"fit", "[0]+[1]*x", 0, 40)
    for idx in range(len(Voltages)):
        points.SetPointError(idx, error[idx], 0.1)
        points.Fit(fit, "R")
        fit.Draw("Same")
        # Compute R squared
        residuals = []
        for idx in range(len(Voltages)):
            residuals.append((low_value[idx]-fit.Eval(Voltages[idx]))**2)
        residuals = np.array(residuals)
        ss_res = np.sum(residuals)
        ss_tot = np.sum((np.array(low_value)-np.mean(low_value))**2)
        r_squared = 1 - (ss_res/ss_tot)
        print(f"R squared: {r_squared}")

    legend.Draw()
    limits.GetYaxis().SetTitle("Voltage /kV")
    limits.GetXaxis().SetTitle("Max ToT/ns")
    c_fit.Update()
    if save_plots:
        c_fit.SaveAs(f"Pictures/Analysis/E_vs_MaxToT{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
