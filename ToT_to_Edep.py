import ROOT
import os
import sifca_utils
import click

sifca_utils.plotting.set_sifca_style()

#CONSTANTS
FORMAT = ".pdf"
save_plots = True
omit_plots = False 
ROOT.gROOT.SetBatch(omit_plots)
ROOT.gStyle.SetOptStat(111111)
# ROOT.gStyle.SetOptStat(0)

@click.command()
@click.argument('inputfiles', nargs = -1)
def main(inputfiles):
    for inputfile in inputfiles:
        # Where to save the file
        name = inputfile.split("/")[-1].split(".")[0]
        voltage = int(name.split("_")[1][0:2])
        folder = f"Pictures/Analysis/{voltage}_kV"
        if save_plots:
            os.makedirs(folder, exist_ok=True)
        
        # Calibrations ToT = A* V + B
        # Row 6 : A = 0.032+-0.028 B = 5.7+-0.8
        # Row 7 : A = 0.062+-0.007 B = 5.9+-0.2
        # Row 8 : A = 0.063+-0.007 B = 5.19+-0.19
        # Row 9 : A = 0.041+-0.036 B = 5.3+-1.0
        # All   : A = 0.070+-0.006 B = 5.61+-0.16 
        calibration = {
            "6" : {"A" : 0.032, "Delta_A" : 0.028, "B" : 5.7, "Delta_B" : 0.8},
            "7" : {"A" : 0.062, "Delta_A" : 0.007, "B" : 5.9, "Delta_B" : 0.2},
            "8" : {"A" : 0.063, "Delta_A" : 0.007, "B" : 5.19, "Delta_B" : 0.19},
            "9" : {"A" : 0.041, "Delta_A" : 0.036, "B" : 5.3, "Delta_B" : 1.0},
            "All" : {"A" : 0.070, "Delta_A" : 0.006, "B" : 5.61, "Delta_B" : 0.16}
        }
        
        
        df = ROOT.RDataFrame("Hits", inputfile)
        c = ROOT.TCanvas()
        h = df.Histo1D(("h", "ToT", 100,0,10), "tot_cal")
        h.Draw()
        c.Draw()
        if not omit_plots:
            input("Press enter to continue")
        for irow in range(6,10):
            A = calibration[str(irow)]["A"]
            Delta_A = calibration[str(irow)]["Delta_A"]
            B = calibration[str(irow)]["B"]
            Delta_B = calibration[str(irow)]["Delta_B"]
            
            df_irow = df.Filter(f"row == {irow}")
            df_irow = df_irow.Define("Edep", f"(tot_cal-{B})/{A}")
            df_irow = df_irow.Define("Edep_err", f"sqrt(pow(({B}-tot_cal) / ({A}*{A}) * {Delta_A}, 2) + pow({Delta_B}/{A}, 2))")

            c = ROOT.TCanvas()
            h = df_irow.Histo1D(("h", f"Energy deposition in row {irow}", 50, -10, 35), "Edep")
            h.Draw()
            c.Draw()
            if not omit_plots:
                input("Press enter to continue")
            if save_plots:
                c.SaveAs(f"{folder}/Edep_row_{irow}{FORMAT}")
        A = 0.070
        Delta_A = 0.006
        B = 5.61
        Delta_B = 0.16
        df = df.Define("Edep", f"(tot_cal-{B})/{A}")
        df = df.Define("Edep_err", f"sqrt(pow(({B}-tot_cal) / ({A}*{A}) * {Delta_A}, 2) + pow({Delta_B}/{A}, 2))")

        c = ROOT.TCanvas()
        h = df_irow.Histo1D(("h", f"Energy deposition in row {irow}", 50, -10, 35), "Edep")
        h.Draw()
        c.Draw()
        if not omit_plots:
            input("Press enter to continue")
        if save_plots:
            c.SaveAs(f"{folder}/Edep_All{FORMAT}")

        h = df.Histo1D(("h", "ToT", 100,0,10), "tot_cal")
        h.Draw()
        c.Draw()
        if not omit_plots:
            input("Press enter to continue")


            
if __name__ == '__main__':
    main()