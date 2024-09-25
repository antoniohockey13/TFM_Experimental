import ROOT
import click
import os
import numpy as np
import sifca_utils 
import matplotlib.pyplot as plt

sifca_utils.plotting.set_sifca_style()
# CONSTANTS
FORMAT = "pdf"
save_plots = True
omit_plots = False 
ROOT.gROOT.SetBatch(omit_plots)
# ROOT.gStyle.SetOptStat(111111)
ROOT.gStyle.SetOptStat(0)

def get_cal(file, cut=""):
    cal = ROOT.TH1F("calibration", "", 1024, 0, 1023)
    file.Hits.Project("calibration", "cal", cut)
    max_bin = cal.GetMaximumBin()
    return max_bin

@click.command()
@click.argument('inputfiles', nargs=-1)
def main(inputfiles):
    if save_plots:
        input_name = inputfiles[0].split('/')
        input_name[-1] = input_name[-1].split('.')[0]
        folder = "/".join(input_name[1:-1])
        os.makedirs(f"Pictures/{folder}", exist_ok=True)

    for irow in range(7,8):
        c = ROOT.TCanvas(f"c{irow}", f"c{irow}")
        legend = ROOT.TLegend(0.6,0.7,0.9,0.9)
        toa_calibrated = []

        toa_calibrated.append(ROOT.TH2F(f"toa_calibrated", "", 1, 0, 14, 1, 0, 2e-2))
        toa_calibrated[-1].GetXaxis().SetTitle("ToA/ns")
        toa_calibrated[-1].GetYaxis().SetTitle("Entries")
        toa_calibrated[-1].Draw()
        voltages_kV = []
        for i, inputfile in enumerate((inputfiles)):
            voltages_kV.append(int(inputfile.split('/')[-1].split('_')[0]))
            file = ROOT.TFile(inputfile)
            max_bin_value = get_cal(file, f"row=={irow}")
            opt = "same"
            file.Hits.SetLineColor(i+1)
            # Change limits
            toa_calibrated.append(ROOT.TH1F(f"toa_calibrated_{i}", "", 125, 0, 14)) 
            file.Hits.Project(f"toa_calibrated_{i}", "toa_cal", f"row == {irow} && cal-{max_bin_value}<2.5")
            toa_calibrated[-1].SetDirectory(0) 
            # Plot
            toa_calibrated[-1].SetTitle("ToA Calibrated for Different Voltages")
            toa_calibrated[-1].GetXaxis().SetTitle("ToA/ns")
            toa_calibrated[-1].GetYaxis().SetTitle("Entries")
            legend.AddEntry(toa_calibrated[-1], f"V = {voltages_kV[i]:.1f} \pm 0.1 kV", "l")
            toa_calibrated[-1].SetLineColor(i+1)
            toa_calibrated[-1].DrawNormalized(f"HIST {opt}")
            file.Close()
        c.Update()
        legend.Draw()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/toa_calibrated_for_different_kV_row_{irow}.{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")
        
if __name__ == "__main__":
    main()
