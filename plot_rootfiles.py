import ROOT
import click
import os

# CONSTANTS
FORMAT = ".pdf"
save_plots = True
omit_plots = False
ROOT.gROOT.SetBatch(omit_plots)
# ROOT.gStyle.SetOptStat(111111)
ROOT.gStyle.SetOptStat(0)
def plot_hit_map(file, canvas_name, title, file_name, folder, cut=""):
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
    
def plot_tot_code(file, canvas_name, title, file_name, folder, cut=""):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    file.Hits.Draw("tot_code>>tot_code(512,0,511)", cut,"")
    tot_code = ROOT.gDirectory.Get("tot_code")
    # tot_code.SetTitle(title)
    tot_code.GetXaxis().SetTitle("ToT/code")
    tot_code.GetYaxis().SetTitle("Entries")
    c.Draw()
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")

def plot_tot_calibrated(file, canvas_name, title, file_name, folder, cut=""):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    file.Hits.Draw("tot_cal>>tot_calibrated(100,0,10)", cut,"")
    tot_calibrated = ROOT.gDirectory.Get("tot_calibrated")
    tot_calibrated.SetTitle(title)
    tot_calibrated.GetXaxis().SetTitle("ToT/ns")
    tot_calibrated.GetYaxis().SetTitle("Entries")
    c.Draw()
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")

def plot_tot_calibrated_full(file, canvas_name, title, file_name, folder, cut=""):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    c.SetLogy()
    file.Hits.Draw("tot_cal>>tot_calibrated(500,0,20)", cut,"")
    tot_calibrated = ROOT.gDirectory.Get("tot_calibrated")
    tot_calibrated.SetTitle(title)
    tot_calibrated.GetXaxis().SetTitle("ToT/ns")
    tot_calibrated.GetYaxis().SetTitle("Entries")
    c.SetLogy()
    c.Draw()
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")
def plot_toa_code(file, canvas_name, title, file_name, folder, cut=""):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    file.Hits.Draw("toa_code>>toa_code(1025,0,1024)", cut,"")
    toa_code = ROOT.gDirectory.Get("toa_code")
    toa_code.SetTitle(title)
    toa_code.GetXaxis().SetTitle("ToA/code")
    toa_code.GetYaxis().SetTitle("Entries")
    c.Draw()
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")

def plot_toa_calibrated(file, canvas_name, title, file_name, folder, cut=""):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    file.Hits.Draw("toa_cal>>toa_calibrated(125,0,14)", cut,"")
    toa_calibrated = ROOT.gDirectory.Get("toa_calibrated")
    toa_calibrated.SetTitle(title)
    toa_calibrated.GetXaxis().SetTitle("ToA/ns")
    toa_calibrated.GetYaxis().SetTitle("Entries")
    c.Draw()
    if save_plots:
        c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    if not omit_plots:
        input("Press Enter to continue...")

def plot_cal(file, canvas_name, title, file_name, folder, cut=""):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    file.Hits.Draw("cal>>cal(1024,1,1024)", cut,"")
    cal = ROOT.gDirectory.Get("cal")
    cal.SetTitle(title)
    cal.GetXaxis().SetTitle("Calibration")
    cal.GetYaxis().SetTitle("Entries")
    c.SetLogy()
    c.Draw()
    # if save_plots:
        # c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
    # if not omit_plots:
        # input("Press Enter to continue...")
    max_bin = cal.GetMaximumBin()
    return max_bin

def plot_tot_toa(file, canvas_name, title, file_name, folder, cut=""):
    c = ROOT.TCanvas(canvas_name, canvas_name)
    file.Hits.Draw("tot_cal:toa_cal>>tot_toa(200,0,10,500,0,14)", cut,"colz")
    tot_toa = ROOT.gDirectory.Get("tot_toa")
    tot_toa.SetTitle(title)
    tot_toa.GetXaxis().SetTitle("ToT/ns")
    tot_toa.GetYaxis().SetTitle("ToA/ns")
    c.Draw()
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

        # Plot functions
        # plot_hit_map(file, "hit_map", f"Hit Map", f"hit_map", folder)
        max_bin = []
        for i in range(6,10):
            max_bin.append(plot_cal(file, f"cal{i}", f"Calibration {i}", f"cal_row_{i}", folder, f"row == {i}"))
        # for i in range(6,10):
        #     plot_tot_code(file, f"tot_code{i}", f"ToT Code {i}", f"tot_code_row_{i}", folder, f"row == {i}")
        for i in range(6,10):
            # plot_tot_calibrated(file, f"tot_calibrated{i}", f"ToT Calibrated {i}", f"tot_calibrated_row_{i}", folder, f"abs(cal-{max_bin[i-6]})<2.5 && row == {i}")
            plot_tot_calibrated_full(file, f"tot_calibrated_full{i}", f"ToT Calibrated Full {i}", f"tot_calibrated_full_row_{i}", folder, f"abs(cal-{max_bin[i-6]})<2.5 && row == {i}")
        # for i in range(6,10):    
        #     plot_toa_code(file, f"toa_code{i}", f"ToA Code {i}", f"toa_code_row_{i}", folder, f"abs(cal-{max_bin[i-6]})<1.5 && row == {i}")
        for i in range(6,10):    
            plot_toa_calibrated(file, f"toa_calibrated{i}", f"ToA Calibrated {i}", f"toa_calibrated_row_{i}", folder, f"abs(cal-{max_bin[i-6]})<2.5 && row == {i}")
            plot_toa_calibrated(file, f"toa_calibrated{i}", f"ToA Calibrated Inversed {i}", f"toa_calibrated_row_{i}", folder, f"abs(cal-{max_bin[i-6]})>2.5 && row == {i}")
        # for i in range(6,10):
            # plot_tot_toa(file, f"tot_toa{i}", f"ToT vs ToA {i}", f"tot_toa_row_{i}", folder, f"abs(cal-{max_bin[i-6]})<2.5 && row == {i}")

        file.Close()

if __name__ == '__main__':
    main()
