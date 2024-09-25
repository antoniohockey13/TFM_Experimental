import sifca_utils.plotting
import ROOT
import click
import os

# Set SIFCA plotting style
sifca_utils.plotting.set_sifca_style()

# Constants
FORMAT = ".pdf"
save_plots = True  
omit_plots = False 
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(0)
colors = [ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kOrange]

def get_cal(file, cut=""):
    """Function to get the maximum bin of the calibration histogram."""
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
        folder = "/".join(input_name[1:2])
        os.makedirs(f"Pictures/{folder}", exist_ok=True)

    for f in inputfiles:
        voltage = f.split('/')[-1].split("_")[0]
        print(f"Voltage = {voltage}kV")
        file = ROOT.TFile(f)
        max_bin_values = []

        for irow in range(6, 10):
            max_bin_values.append(get_cal(file, f"row=={irow}"))

        toa_calibrated = []
        c = ROOT.TCanvas(f"c_{voltage}", f"c_{voltage}")
        legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
        
        toa_calibrated.append(ROOT.TH2F("limits", "", 1, 0, 14, 1, 0, 2e-2))
        toa_calibrated[-1].Draw()
        toa_calibrated[-1].GetXaxis().SetTitle("ToA/ns")
        toa_calibrated[-1].GetYaxis().SetTitle("Entries")
        toa_calibrated[-1].SetTitle(f"ToA measured for {voltage} kV")
        c.Draw()
        opt = "same"
        for i, irow in enumerate(range(6, 10)):
            print(irow)
            file.Hits.SetLineColor(colors[i])
            
            toa_calibrated.append(ROOT.TH1F(f"toa_calibrated_{i}", "", 125, 0, 14))
            file.Hits.Project(f"toa_calibrated_{i}", "toa_cal", f"row == {irow} && cal-{max_bin_values[i]}<2.5")
            toa_calibrated[-1].SetDirectory(0)
            legend.AddEntry(toa_calibrated[-1], f"Row = {irow}", "l")
            toa_calibrated[-1].SetLineColor(colors[i])
            toa_calibrated[-1].DrawNormalized(f"HIST {opt}")
        legend.Draw()
        c.Update()
        
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/all_ToA_file_{voltage}{FORMAT}")
        
        if not omit_plots:
            input("Press Enter to continue...")
        
        file.Close()

if __name__ == "__main__":
    main()