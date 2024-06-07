import sifca_utils
import sifca_utils.functions
import ROOT
import sifca_utils
import scipy.constants as const
import click
import os
import matplotlib.pyplot as plt

# sifca_utils.plotting.set_sifca_style()

#CONSTANTS
FORMAT = ".pdf"
save_plots = False
omit_plots = False
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(111111)
# ROOT.gStyle.SetOptStat(0)
h = const.Planck
c = const.speed_of_light
e = const.elementary_charge
percentage = [0.001/100]

# UNITS
V = 1
kV = 1e3*V

def get_cal(file, cut=""):
    cal = ROOT.TH1F("calibration", "", 1024, 1, 1024)
    file.Hits.Project("calibration", "cal", cut)
    max_bin = cal.GetMaximumBin()
    return max_bin

def tot_fit_histogram(file, canvas_name, cut, V, file_name, folder):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    histo = ROOT.TH1F("histo", "", 100, 0, 10)
    file.Hits.Project("histo", "tot_cal", cut)
    histo.Draw()
    fit = ROOT.TF1("fit", f"[0]*([1]/x-1)*x^2", 0, 10)
    fit.SetParameter(0, 1e5)
    fit.SetParameter(1, 6)
    histo.Fit(fit)
    fit.Draw("same")
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
    for ipercentage in percentage:
        low_value = {}
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
                # low_value[irow].append(tot_fit_gauss(f,f"c_row_{irow}", f"abs({max_bin}-cal)<2.5 && row == {irow}", f"ToT_fit_row{irow}", folder, ipercentage))
                fit = tot_fit_histogram(f,f"c_row_{irow}", f"abs({max_bin}-cal)<2.5 && row == {irow}", V[i], f"ToT_fit_row{irow}", folder)

        # for i in range(6,10):
        #     plt.plot(V, low_value[i],'.', label=f"Row {i}")
        # plt.xlabel("Voltage [kV]")
        # plt.ylabel("ToT/ns")
        # plt.legend()
        # plt.show()

            

if __name__ == "__main__":
    main()