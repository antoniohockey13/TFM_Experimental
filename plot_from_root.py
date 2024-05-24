import ROOT 
import click
import os


omit_plots = False
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(111111)

@click.command()
@click.argument('inputfiles', nargs=-1)

def main(inputfiles):

    input_name = inputfiles[0].split('/')
    input_name[-1] = input_name[-1].split('.')[0]
    folder = f"{input_name[1]}/{input_name[2]}"
    try:
        os.mkdir("Pictures")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"Pictures/{input_name[1]}")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"Pictures/{folder}")
    except FileExistsError:
        pass

    for inputfile in inputfiles:
        file = ROOT.TFile(inputfile)

        # c = ROOT.TCanvas("c", "c")
        # file.Hits.Draw("col:row>>hit_map(16,0,16,16,0,16)", "", "colz")
        # hit_map = ROOT.gDirectory.Get("hit_map")
        # hit_map.SetTitle(f"Hit Map {input_name[-1]}")
        # hit_map.GetXaxis().SetTitle("Row")
        # hit_map.GetYaxis().SetTitle("Column")
        # c.Draw()
        # input("Press Enter to continue...")
        # c.SaveAs(f"Pictures/{folder}/{input_name[-1]}.png")

        file.Hits.SetLineStyle(1)
        file.Hits.SetLineColor(1)
        c1 = ROOT.TCanvas("c1", "c1")
        file.Hits.Draw("cal>>cal1(1024,1,1024)", "row == 6", "")
        cal1 = ROOT.gDirectory.Get("cal1")
        cal1.SetTitle(f"Calibration {input_name[-1]}")
        cal1.GetXaxis().SetTitle("Calibration")
        cal1.GetYaxis().SetTitle("Counts")
        # Find bin with max entries
        max_bin_1 = cal1.GetMaximumBin()
        

        # file.Hits.SetLineStyle(2)
        # file.Hits.SetLineColor(2)
        # file.Hits.Draw("cal>>cal2(1024,1,1024)", "row == 7", "same")
        # cal2 = ROOT.gDirectory.Get("cal2")

        # file.Hits.SetLineStyle(3)
        # file.Hits.SetLineColor(3)
        # file.Hits.Draw("cal>>cal3(1024,1,1024)", "row == 8", "same")
        # cal3 = ROOT.gDirectory.Get("cal3")

        # file.Hits.SetLineStyle(4)
        # file.Hits.SetLineColor(4)
        # file.Hits.Draw("cal>>cal4(1024,1,1024)", "row == 9", "same")
        # cal4 = ROOT.gDirectory.Get("cal4")


        # legend = ROOT.TLegend(0.1, 0.2, 0.6, 0.9)
        # legend.AddEntry(cal1, "Column 6", "l")
        # legend.AddEntry(cal2, "Column 7", "l")
        # legend.AddEntry(cal3, "Column 8", "l")
        # legend.AddEntry(cal4, "Column 9", "l")
        # legend.Draw()
        # c1.Draw()
        input("Press Enter to continue...")
        # c1.SaveAs(f"Pictures/{folder}/{input_name[-1]}_cal.png")
        file.Hits.SetLineStyle(1)
        file.Hits.SetLineColor(1)
        c2 = ROOT.TCanvas("c2", "c2")
        file.Hits.Draw("cal>>cal2(1024,1,1024)", "row == 7", "")
        cal2 = ROOT.gDirectory.Get("cal2")
        cal2.SetTitle(f"Calibration {input_name[-1]}")
        cal2.GetXaxis().SetTitle("Calibration")
        cal2.GetYaxis().SetTitle("Counts")
        c2.Draw()
        max_bin_2 = cal2.GetMaximumBin()
        input("Press Enter to continue...")
        # c2.SaveAs(f"Pictures/{folder}/{input_name[-1]}_cal.png")

        c3 = ROOT.TCanvas("c3", "c3")
        file.Hits.Draw("cal>>cal3(1024,1,1024)", "row == 8", "")
        cal3 = ROOT.gDirectory.Get("cal3")
        cal3.SetTitle(f"Calibration {input_name[-1]}")
        cal3.GetXaxis().SetTitle("Calibration")
        cal3.GetYaxis().SetTitle("Counts")
        c3.Draw()
        max_bin_3 = cal3.GetMaximumBin()
        input("Press Enter to continue...")
        # c3.SaveAs(f"Pictures/{folder}/{input_name[-1]}_cal.png")

        c4 = ROOT.TCanvas("c4", "c4")
        file.Hits.Draw("cal>>cal4(1024,1,1024)", "row == 9", "")
        cal4 = ROOT.gDirectory.Get("cal4")
        cal4.SetTitle(f"Calibration {input_name[-1]}")
        cal4.GetXaxis().SetTitle("Calibration")
        cal4.GetYaxis().SetTitle("Counts")
        c4.Draw()
        max_bin_4 = cal4.GetMaximumBin()
        input("Press Enter to continue...")
        # c4.SaveAs(f"Pictures/{folder}/{input_name[-1]}_cal.png")

        c5 = ROOT.TCanvas("c5", "c5")
        file.Hits.Draw("ToT_cal>>tot1()", "row == 6 && abs(cal-max_bin_1)<1.5", "")
        tot1 = ROOT.gDirectory.Get("tot1")
        tot1.SetTitle(f"ToT {input_name[-1]}")
        tot1.GetXaxis().SetTitle("ToT")
        tot1.GetYaxis().SetTitle("Counts")
        c5.Draw()
        input("Press Enter to continue...")
        
        file.Close()

if __name__ == '__main__':
    main()