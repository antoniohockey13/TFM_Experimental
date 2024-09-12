import sifca_utils.plotting
import ROOT
import click
import os
import sifca_utils

sifca_utils.plotting.set_sifca_style()



# CONSTANTS
FORMAT = ".pdf"
save_plots = True
omit_plots = True
ROOT.gROOT.SetBatch(omit_plots)
# ROOT.gStyle.SetOptStat(111111)
ROOT.gStyle.SetOptStat(0)
colors = [ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kOrange]


def max_cal(file, canvas_name, title, file_name, folder, cut=""):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    file.Hits.Draw("cal>>cal(1024,0,1023)", cut,"")
    cal = ROOT.gDirectory.Get("cal")
    cal.SetTitle(title)
    cal.GetXaxis().SetTitle("Calibration")
    cal.GetYaxis().SetTitle("Entries")
    max_bin = cal.GetMaximumBin()
    return max_bin

def plot_cal(file, canvas_name, title, file_name, folder, cut=""):

    cal_histo = []
    c = ROOT.TCanvas(canvas_name, canvas_name)
    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    cal_histo.append(ROOT.TH2F("limits", "", 1, 1, 1024, 1, 1e-3, 1))
    cal_histo[-1].Draw()
    cal_histo[-1].GetXaxis().SetTitle("Calibration")
    cal_histo[-1].GetYaxis().SetTitle("Entries")
    cal_histo[-1].SetTitle(title)
    c.Draw()
    opt = "same"
    for i, irow in enumerate(range(6, 10)):
        file.Hits.SetLineColor(colors[i])
        
        cal_histo.append(ROOT.TH1F(f"cal_{i}", "", 1024, 1, 1024))
        file.Hits.Project(f"cal_{i}", "cal", f"row == {irow}")
        cal_histo[-1].SetDirectory(0)

        legend.AddEntry(cal_histo[-1], f"Row = {irow}", "l")
        cal_histo[-1].SetLineColor(colors[i])
        cal_histo[-1].DrawNormalized(f"HIST {opt}")
    legend.Draw()
    c.Update()
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")

def plot_tot(file, canvas_name, title, file_name, folder, max_bin):
    """
    Plot the ToT distribution for the different rows
    Use filtered data
    """
    tot_histo = []
    c = ROOT.TCanvas(canvas_name, canvas_name)
    # c.SetLogy()
    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    tot_histo.append(ROOT.TH2F("limits", "", 1, 0, 8, 1, 1e-3, 0.1))
    tot_histo[-1].Draw()
    tot_histo[-1].GetXaxis().SetTitle("Tot/ns")
    tot_histo[-1].GetYaxis().SetTitle("Entries")
    tot_histo[-1].SetTitle(title)
    c.Draw()
    opt = "same"
    for i, irow in enumerate(range(6, 10)):
        file.Hits.SetLineColor(colors[i])
        
        tot_histo.append(ROOT.TH1F(f"tot_cal_{i}", "", 80, 0, 8))
        file.Hits.Project(f"tot_cal_{i}", "tot_cal", f"row == {irow} && abs(cal-{max_bin[i]})<2.5")
        tot_histo[-1].SetDirectory(0)

        legend.AddEntry(tot_histo[-1], f"Row = {irow}", "l")
        tot_histo[-1].SetLineColor(colors[i])
        tot_histo[-1].DrawNormalized(f"HIST {opt}")

    legend.Draw()
    c.Update()
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")

@click.command()
@click.argument('inputfiles', nargs=-1)
def main(inputfiles):
    # Directory to store the output plots
    folder = ""
    for inputfile in inputfiles:
        input_name = inputfile.split('/')
        input_name[-1] = input_name[-1].split('.')[0]
        folder = f"{input_name[1]}/{input_name[-1]}"
        if save_plots:
            os.makedirs(f"Pictures/{folder}", exist_ok=True)
        
        file = ROOT.TFile(inputfile)
        max_bin = []
        for irow in range(6, 10):
            max_bin.append(max_cal(file, f"cal{irow}", f"Calibration {irow}", f"cal_row_{irow}", folder, f"row == {irow}"))
        # Plot functions
        # plot_cal(file, f"cal", f"Calibration", f"cal_filtered_all_together_{input_name[-1]}", folder, "")
        plot_tot(file, f"tot_cal", f"ToT", f"tot_filtered_all_together_{input_name[-1]}", folder, max_bin)

if __name__ == '__main__':
    main()