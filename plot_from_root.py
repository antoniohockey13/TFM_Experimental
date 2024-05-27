
import ROOT 
import click@click.command()
@click.argument('inputfiles', nargs=-1)
import os

# CONSTANTS
FORMAT = ".png"
save_plots = False
omit_plots = False
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(111111)


def main(inputfiles):
    for inputfile in inputfiles:
        input_name = inputfile.split('/')
        input_name[-1] = input_name[-1].split('.')[0]
        folder = "/".join(input_name[1:-1])

        # Create necessary directories
        os.makedirs(f"Pictures/{folder}", exist_ok=True)

        file = ROOT.TFile(inputfile)

        def plot_hit_map(canvas_name, file_name):
            c = ROOT.TCanvas(canvas_name, canvas_name)
            file.Hits.Draw("col:row>>hit_map(16,0,16,16,0,16)", "", "colz")
            hit_map = ROOT.gDirectory.Get("hit_map")
            hit_map.SetTitle(f"Hit Map {input_name[-1]}")
            hit_map.GetXaxis().SetTitle("Row")
            hit_map.GetYaxis().SetTitle("Column")
            c.Draw()
            input("Press Enter to continue...")
            if save_plots:
                c.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")
        plot_hit_map("hit_map", f"{input_name[-1]}_hit_map")

        def plot_calibration(row_num, canvas_name, file_name):
            canvas = ROOT.TCanvas(canvas_name, canvas_name)
            file.Hits.Draw(f"cal>>{canvas_name}(1024,1,1024)", f"row == {row_num}", "")
            cal_hist = ROOT.gDirectory.Get(canvas_name)
            cal_hist.SetTitle(f"Calibration {input_name[-1]}")
            cal_hist.GetXaxis().SetTitle("Calibration")
            cal_hist.GetYaxis().SetTitle("Counts")
            canvas.Draw()
            input("Press Enter to continue...")
            if save_plots:
                canvas.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")

        # Plot calibration for rows 6 to 9
        for row in range(6, 10):
            plot_calibration(row, f"cal{row}", f"{input_name[-1]}_cal_row_{row}")

        # Additional processing for ToT plots
        def plot_tot_code(row_num, max_bin, canvas_name, file_name):
            canvas = ROOT.TCanvas(canvas_name, canvas_name)
            file.Hits.Draw(f"ToT_cal>>{canvas_name}()", f"row == {row_num} && abs(cal-{max_bin})<1.5", "")
            tot_hist = ROOT.gDirectory.Get(canvas_name)
            tot_hist.SetTitle(f"ToT {input_name[-1]}")
            tot_hist.GetXaxis().SetTitle("ToT")
            tot_hist.GetYaxis().SetTitle("Counts")
            canvas.Draw()
            if save_plots:
                canvas.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")

        max_bins = []
        for row in range(6, 10):
            hist_name = f"cal{row}"
            file.Hits.Draw(f"cal>>{hist_name}(1024,1,1024)", f"row == {row}", "")
            cal_hist = ROOT.gDirectory.Get(hist_name)
            max_bin = cal_hist.GetMaximumBin()
            max_bins.append(max_bin)
        
        for i, row in enumerate(range(6, 10)):
            plot_tot(row, max_bins[i], f"tot{row}", f"{input_name[-1]}_tot_row_{row}")

        def plot_toa(row_num, canvas_name, file_name):
            canvas = ROOT.TCanvas(canvas_name, canvas_name)
            file.Hits.Draw(f"toa>>{canvas_name}(1024,1,1024)", f"row == {row_num}", "")
            toa_hist = ROOT.gDirectory.Get(canvas_name)
            toa_hist.SetTitle(f"ToA {input_name[-1]}")
            toa_hist.GetXaxis().SetTitle("ToA")
            toa_hist.GetYaxis().SetTitle("Counts")
            canvas.Draw()
            if save_plots:
                canvas.SaveAs(f"Pictures/{folder}/{file_name}{FORMAT}")



        file.Close()
if __name__ == '__main__':
    main()
