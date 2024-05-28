import ROOT
import click
import os

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
    

    max_bin_value = {}
    for irow in range(6,10):
        c = ROOT.TCanvas(f"c{irow}", f"c{irow}")
        legend = ROOT.TLegend(0.1,0.7,0.48,0.9)
        opt = ""
        tot_calibrated = []
        max_bin_value[irow] = {}
        for i, inputfile in enumerate(inputfiles):
            file = ROOT.TFile(inputfile)
            max_bin_value[irow][i] = get_cal(file, f"row=={irow}")
    
            if i > 0:
                opt = "same"
            file.Hits.SetLineColor(i+1)
            print(max_bin_value[irow][i])
            tot_calibrated.append(ROOT.TH1F(f"tot_calibrated_{i}", "", 250, 0, 25))
            tot_calibrated[-1].SetDirectory(0)
            file.Hits.Project(f"tot_calibrated_{i}", "tot_cal", f"row == {irow} && cal-{max_bin_value[irow][i]}<2.5")
            tot_calibrated[-1].Scale(1.0 / tot_calibrated[-1].Integral()) 
            tot_calibrated[-1].SetTitle("ToT Calibrated for Different Voltages")
            tot_calibrated[-1].GetXaxis().SetTitle("ToT/ns")
            tot_calibrated[-1].GetYaxis().SetTitle("Entries")
            legend.AddEntry(tot_calibrated[-1], f"{inputfile}", "l")
            tot_calibrated[-1].Draw(opt)
            file.Close()
        legend.Draw()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/tot_calibrated_for_different_kV_row_{irow}.{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")

if __name__ == '__main__':
    main()