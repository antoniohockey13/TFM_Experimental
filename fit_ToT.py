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
    cal = ROOT.TH1F("calibration", "", 1024, 0, 1023)
    file.Hits.Project("calibration", "cal", cut)
    max_bin = cal.GetMaximumBin()
    return max_bin

def tot_fit_histogram(file, canvas_name, cut, Voltages, file_name, folder):
    # Create canvas
    c = ROOT.TCanvas(canvas_name, canvas_name)
    legend = ROOT.TLegend(0.25,0.2,0.55,0.6)
    legend.SetTextSize(0.028) 
    c.SetLogy()
    # Draw data
    histo = ROOT.TH1F("histo", "", 80, 0, 8)
    file.Hits.Project("histo", "tot_cal", cut)
    histo.GetXaxis().SetTitle("ToT/ns")
    histo.GetYaxis().SetTitle("Entries")
    histo.Draw("PE")
    legend.AddEntry(histo, f"ToT measured", "PE")
    # # Fit gaussian
    fit_gaus = ROOT.TF1("fit_gaus", "gaus", 2, 5)
    histo.Fit(fit_gaus, "R")
    # fit_gaus.SetLineColor(ROOT.kBlue)
    # fit_gaus.SetLineStyle(9)
    # fit_gaus.Draw("same")
    # # Obtain mu
    # mu = round(fit_gaus.GetParameter(1),3)
    # mu_error = round(fit_gaus.GetParError(1), 3)
    # sigma = round(fit_gaus.GetParameter(2),3)
    # sigma_error = round(fit_gaus.GetParError(2),3)
    # legend.AddEntry(fit_gaus, f"Gaussian fit:", "l")
    # legend.AddEntry(fit_gaus, f"\mu={mu}\pm{mu_error} ns,", "")
    # legend.AddEntry(fit_gaus, f" \sigma={sigma}\pm{sigma_error} ns", "")
    
    max = fit_gaus.GetParameter(1)
    # # Fit to region 1 
    # fit1 = ROOT.TF1("fit1", f"[0]*exp([1]*x+[2])", 1.1*max, 1.6*max)
    # fit1.SetParameter(0, 2e4)
    # fit1.SetParameter(1, -3)
    # fit1.SetParameter(2, 15)
    # histo.Fit(fit1, "R")
    # fit1.Draw("same")
    # fit1.SetLineColor(ROOT.kGreen)
    # A = round(fit1.GetParameter(0),1)
    # A_error = round(fit1.GetParError(0),1)
    # B = round(fit1.GetParameter(1),3)
    # B_error = round(fit1.GetParError(1),3)
    # C = round(fit1.GetParameter(2),2)
    # C_error = round(fit1.GetParError(2),2)
    # legend.AddEntry(fit1, "Fit exponential to region 1:", "l")
    # legend.AddEntry(fit1, f"A = {A}\pm{A_error}", "")
    # legend.AddEntry(fit1, f"B = {B}\pm{B_error} /ns", "")
    # legend.AddEntry(fit1, f"C = {C}\pm{C_error}", "")
    ### Change 1.6*max to optimise the fit ###
    # Fit region 2
    fit = ROOT.TF1("fit", f"[0]*exp([1]*x+[2])", 1.6*max, 8)
    fit.SetParameter(0, 2e4)
    fit.SetParameter(1, -3)
    file.Hits.Project("calibration", "cal", cut)
    fit.SetParameter(2, 15)
    histo.Fit(fit, "R")
    fit.SetLineColor(ROOT.kRed)
    fit.Draw("same")
    A = round(fit.GetParameter(0),1)
    A_error = round(fit.GetParError(0),1)
    B = round(fit.GetParameter(1),2)
    B_error = round(fit.GetParError(1),2)
    C = round(fit.GetParameter(2),2)
    C_error = round(fit.GetParError(2),2)
    legend.AddEntry(fit, "Fit exponential to region 2:", "l")
    legend.AddEntry(fit, f"A = {A:.0f}\pm{A_error:.0f}", "")
    legend.AddEntry(fit, f"B = {B:.3f}\pm{B_error:.2f} /ns", "")
    legend.AddEntry(fit , f"C = {C:.3f}\pm{C_error:.2f}", "")

    
    legend.Draw()
    c.Update()
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")
    return fit

# def tot_fit_gauss(file, canvas_name, cut, file_name, folder, percentage):
#     c = ROOT.TCanvas(canvas_name, canvas_name)
#     histo = ROOT.TH1F("histo", "", 100, 0, 10)
#     file.Hits.Project("histo", "tot_cal", cut)
#     histo.Draw()
#     fit = ROOT.TF1("fit", "gaus", 0, 10)    
#     histo.Fit(fit)
#     fit.Draw("same")
#     c.Update()
#     mean = fit.GetParameter(1)
#     mean_error = fit.GetParError(1)
#     max_value = fit.GetMaximum()
#     limit_value = percentage*max_value
#     limit = fit.GetX(limit_value, xmin=mean, xmax=10)
#     print(limit)
#     if save_plots:
#         c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
#     if not omit_plots:
#         input("Press Enter to continue...")
#     return limit

# def all_rows_together(inputfiles):
#     Voltages = []
#     # Value of max ToT and error
#     low_value = []
#     error = []
#     for i, file in enumerate(inputfiles):
#         Voltages.append(int(file.split('/')[-1].split("_")[0]))
#         print(f"Voltage: {Voltages[-1]}kV")
#         input_name = file.split('/')
#         input_name[-1] = input_name[-1].split('.')[0]
#         folder = f"{input_name[1]}/{input_name[-1]}"
#         if save_plots:
#             os.makedirs(f"Pictures/{folder}", exist_ok=True) 
        
#         f = ROOT.TFile(file)
#         df = ROOT.RDataFrame("Hits", f)
#         cal = {}
#         for irow in range(6,10):
#             cal[irow] = get_cal(f, f"row=={irow}")
#         # Filter df to cal+-1 for each row
#         filtered_file = f"{folder}/filtered.root"
#         df_filtered = df.Filter(" || ".join([f"row == {irow} && abs(cal - {cal[irow]}) < 2.5" for irow in range(6, 10)]))

#         # Plot ToT histogram

#         c = ROOT.TCanvas("c", "c")
#         legend = ROOT.TLegend(0.65,0.75,0.9,0.9)
#         c.SetLogy()
#         # Data
#         h = df_filtered.Histo1D(("histo", "", 100, 0, 10), "tot_cal")
#         legend.AddEntry(h.GetPtr(), f"ToT measured", "l")
#         h.Draw("PE")

#         # Fit gaussian
#         fit_gaus = ROOT.TF1("fit_gaus", "gaus", 2, 5)
#         h.Fit(fit_gaus, "R")
#         fit_gaus.SetLineColor(ROOT.kBlue)
#         fit_gaus.SetLineStyle(9)
#         # fit_gaus.Draw("same")
#         # legend.AddEntry(fit_gaus, f"Gaussian fit", "l")
    
#         max = fit_gaus.GetParameter(1)

#         # Fit region 2
#         # fit to exponential y = A e^(Bx+C)
#         fit = ROOT.TF1("fit", f"[0]*exp([1]*x+[2])", 1.6*max, 8)
#         fit.SetParameter(0, 2e4)
#         fit.SetParameter(1, -3)
#         fit.SetParameter(2, 15)
#         h.Fit(fit, "R")
#         fit.SetLineColor(ROOT.kRed)
#         fit.Draw("same")
#         legend.AddEntry(fit, f"Fit exponential to region 2", "l")

#         legend.Draw()
#         c.Update()
#         if save_plots:
#             c.SaveAs(f"Pictures/{folder}/All_ToT_together_{input_name[-1]}{FORMAT}")
#         if not omit_plots:
#             input("Press Enter to continue...")
#         # Select max value of ToT when fit = e ^-1
#         low_value.append((np.log(fit.GetParameter(0))+fit.GetParameter(2)+1)/-fit.GetParameter(1))
#         dx_da = -1/(fit.GetParameter(0)*fit.GetParameter(1))
#         dx_db = (np.log(fit.GetParameter(0))+fit.GetParameter(2)+1)/(fit.GetParameter(1)**2)
#         dx_dc = -1/(fit.GetParameter(1))
#         error.append(np.sqrt(dx_da**2*fit.GetParError(0)**2 + dx_db**2*fit.GetParError(1)**2 + dx_dc**2*fit.GetParError(2)**2))
#     return low_value, error


@click.command()
@click.argument("inputfiles", nargs=-1)
def main(inputfiles):
    low_value = {}
    error = {}

    for irow in range(6,10):
        low_value[irow] = []
        error[irow] = []
        Voltages = []
        for i, file in enumerate(inputfiles):
            Voltages.append(int(file.split('/')[-1].split("_")[0]))
            print(f"Voltage: {Voltages[-1]}kV \n Row {irow}")
            input_name = file.split('/')
            input_name[-1] = input_name[-1].split('.')[0]
            folder = f"{input_name[1]}/{input_name[-1]}"
            if save_plots:
                os.makedirs(f"Pictures/{folder}", exist_ok=True) 

            f = ROOT.TFile(file)
            max_bin = get_cal(f, f"row=={irow}")
            # fit to exponential y = A e^(Bx+C)
            fit = tot_fit_histogram(f,f"c_row_{irow}", f"abs({max_bin}-cal)<2.5 && row == {irow}", Voltages[i], f"ToT_fit_row{irow}_{input_name[-1]}", folder)
            # Select max value of ToT when fit = e ^-1
            low_value[irow].append((np.log(fit.GetParameter(0))+fit.GetParameter(2)+1)/-fit.GetParameter(1))
            # Error calculation
            dx_da = -1/(fit.GetParameter(0)*fit.GetParameter(1))
            dx_db = (np.log(fit.GetParameter(0))+fit.GetParameter(2)+1)/(fit.GetParameter(1)**2)
            dx_dc = -1/(fit.GetParameter(1))
            error[irow].append(np.sqrt(dx_da**2*fit.GetParError(0)**2 + dx_db**2*fit.GetParError(1)**2 + dx_dc**2*fit.GetParError(2)**2))
    # low_value_together, error_together = all_rows_together(inputfiles)
    # Row 10 all together
    # low_value[10] = low_value_together
    # error[10] = error_together
    print(low_value)
    print(error)
    # ROOT.gROOT.SetBatch(False)
    fit = {}
    points = {}
    c_fit = ROOT.TCanvas("c_fit", "c_fit", 800, 600)
    limits = ROOT.TH2F("limits", "limits", 1, 0, 40,1, 4, 10)
    limits.Draw()
    legend = ROOT.TLegend(0.2, 0.7, 0.5, 0.9)
    colors = [ROOT.kGreen, ROOT.kRed, ROOT.kBlue, ROOT.kOrange, ROOT.kBlack]
    # Define the linear function to fit
    for i, irow in enumerate(range(6, 10)):
        print(f"\n ****************************\n Row {irow}")
        points[irow] = ROOT.TGraphErrors(len(Voltages), array('d', Voltages), array('d', low_value[irow]), array('d', [0.1]*len(Voltages)), array('d', error[irow]))
        points[irow].SetMarkerStyle(20)
        points[irow].SetMarkerSize(1)
        points[irow].SetMarkerColor(colors[i])
        points[irow].SetLineColor(colors[i])
        points[irow].Draw("P") 

        if irow == 10:
            legend.AddEntry(points[irow], f"All sensors combined", "p")
        else:
            legend.AddEntry(points[irow], f"Row {irow}", "p")

        fit[irow] = ROOT.TF1(f"fit{irow}", "[0]+[1]*x", 0, 40)
        for idx in range(len(Voltages)):
            points[irow].SetPointError(idx, 0.1, error[irow][idx])
        points[irow].Fit(fit[irow], "R")
        fit[irow].SetLineColor(colors[i])
        fit[irow].Draw("Same")
        # Compute R squared
        residuals = []
        for idx in range(len(Voltages)):
            residuals.append((low_value[irow][idx]-fit[irow].Eval(Voltages[idx]))**2)
        residuals = np.array(residuals)
        ss_res = np.sum(residuals)
        ss_tot = np.sum((np.array(low_value[irow])-np.mean(low_value[irow]))**2)
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

    # Plot the inverse E vs ToT max
    # for i, irow in enumerate(range(6, 10)):
    #     print(f"\n ****************************\n Row {irow}")
    #     points[irow] = ROOT.TGraphErrors(len(Voltages), array('d', low_value[irow]), array('d', Voltages), array('d', error[irow]), array('d', [0.1]*len(Voltages)))
    #     points[irow].SetMarkerStyle(20)
    #     points[irow].SetMarkerSize(1)
    #     points[irow].SetMarkerColor(colors[i])
    #     points[irow].SetLineColor(colors[i])
    #     points[irow].Draw("P") 

    #     if irow == 10:
    #         legend.AddEntry(points[irow], f"All sensors combined", "p")
    #     else:
    #         legend.AddEntry(points[irow], f"Row {irow}", "p")

    #     fit[irow] = ROOT.TF1(f"fit{irow}", "[0]*x", 0, 40)
    #     for idx in range(len(Voltages)):
    #         points[irow].SetPointError(idx, error[irow][idx], 0.1)
    #     points[irow].Fit(fit[irow], "R")
    #     fit[irow].SetLineColor(colors[i])
    #     fit[irow].Draw("Same")
    #     # Compute R squared
    #     residuals = []
    #     for idx in range(len(Voltages)):
    #         residuals.append((low_value[irow][idx]-fit[irow].Eval(Voltages[idx]))**2)
    #     residuals = np.array(residuals)
    #     ss_res = np.sum(residuals)
    #     ss_tot = np.sum((np.array(low_value[irow])-np.mean(low_value[irow]))**2)
    #     r_squared = 1 - (ss_res/ss_tot)
    #     print(f"R squared: {r_squared}")

    # legend.Draw()
    # limits.GetYaxis().SetTitle("Voltage /kV")
    # limits.GetXaxis().SetTitle("Max ToT/ns")
    # c_fit.Update()
    # if save_plots:
    #     c_fit.SaveAs(f"Pictures/Analysis/V_vs_MaxToT{FORMAT}")
    
    # ROOT.gROOT.SetBatch(False)
    # input("Press Enter to continue...")
if __name__ == "__main__":
    main()
