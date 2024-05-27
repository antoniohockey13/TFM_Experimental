import ROOT
import click
import os

# CONSTANTS
FORMAT = ".png"
save_plots = False
omit_plots = False
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(111111)


@click.command()
@click.argument('inputfiles', nargs=-1)
def main(inputfiles):
    # Directory to store the output plots
    if save_plots:
        input_name = inputfile.split('/')
        input_name[-1] = input_name[-1].split('.')[0]
        folder = "/".join(input_name[1:-1])
        os.makedirs(f"Pictures/{folder}", exist_ok=True)
    # Functios to do the plots
    def plot_hit_map(canvas_name, title, file_name, cut=""):
        c = ROOT.TCanvas(canvas_name, canvas_name)
        file.Hits.Draw("col:row>>hit_map(16,0,16,16,0,16)", cut,"colz")
        hit_map = ROOT.gDirectory.Get("hit_map")
        hit_map.SetTitle(title)
        hit_map.GetXaxis().SetTitle("Row")
        hit_map.GetYaxis().SetTitle("Column")
        c.Draw()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")      
        
    def plot_tot_code(canvas_name, title, file_name, cut=""):
        c = ROOT.TCanvas(canvas_name, canvas_name)
        file.Hits.Draw("ToT>>tot_code(512,0,511)", cut,"")
        tot_code = ROOT.gDirectory.Get("tot_code")
        tot_code.SetTitle(title)
        tot_code.GetXaxis().SetTitle("ToT/code")
        tot_code.GetYaxis().SetTitle("Entries")
        c.Draw()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")

    def plot_tot_calibrated(canvas_name, title, file_name, cut=""):
        c = ROOT.TCanvas(canvas_name, canvas_name)
        file.Hits.Draw("ToT>>tot_calibrated(500,0,25)", cut,"")
        tot_calibrated = ROOT.gDirectory.Get("tot_calibrated")
        tot_calibrated.SetTitle(title)
        tot_calibrated.GetXaxis().SetTitle("ToT/ns")
        tot_calibrated.GetYaxis().SetTitle("Entries")
        c.Draw()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")

    def plot_toa_code(canvas_name, title, file_name, cut=""):
        c = ROOT.TCanvas(canvas_name, canvas_name)
        file.Hits.Draw("ToA>>toa_code(1025,0,1024)", cut,"")
        toa_code = ROOT.gDirectory.Get("toa_code")
        toa_code.SetTitle(title)
        toa_code.GetXaxis().SetTitle("ToA/code")
        toa_code.GetYaxis().SetTitle("Entries")
        c.Draw()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")
    
    def plot_toa_calibrated(canvas_name, title, file_name, cut=""):
        c = ROOT.TCanvas(canvas_name, canvas_name)
        file.Hits.Draw("ToA>>toa_calibrated(500,0,14)", cut,"")
        toa_calibrated = ROOT.gDirectory.Get("toa_calibrated")
        toa_calibrated.SetTitle(title)
        toa_calibrated.GetXaxis().SetTitle("ToA/ns")
        toa_calibrated.GetYaxis().SetTitle("Entries")
        c.Draw()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")
    def plot_cal(canvas_name, title, file_name, cut=""):
        c = ROOT.TCanvas(canvas_name, canvas_name)
        file.Hits.Draw("cal>>cal(1024,1,1024)", cut,"")
        cal = ROOT.gDirectory.Get("cal")
        cal.SetTitle(title)
        cal.GetXaxis().SetTitle("Calibration")
        cal.GetYaxis().SetTitle("Entries")
        c.Draw()
        if save_plots:
            c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
        if not omit_plots:
            input("Press Enter to continue...")
        max_bin = cal.GetMaximumBin()
        max_bin_value = cal.GetBinValue(max_bin)
        return max_bin_value
            
    for inputfile in inputfiles:
        file = ROOT.TFile(inputfile)

        # Plot functions

        file.Close()



if __name__ == '__main__':
    main()




