import ROOT
import click
import os


def get_cal(file, cut=""):
    cal = ROOT.TH1F("calibration", "", 1024, 0, 1023)
    file.Hits.Project("calibration", "cal", cut)
    max_bin = cal.GetMaximumBin()
    return max_bin

@click.command()
@click.argument('inputfiles', nargs=-1)
def main(inputfiles):
    Voltages = []
    for i, file in enumerate(inputfiles):
        Voltages.append(int(file.split('/')[-1].split("_")[0]))
        print(f"Voltage: {Voltages[-1]}kV")
        input_name = file.split('/')
        input_name[-1] = input_name[-1].split('.')[0]
        os.makedirs(f"Root_files/Analysis/Filtered", exist_ok=True)
        
        f = ROOT.TFile(file)
        df = ROOT.RDataFrame("Hits", f)
        cal = {}
        for irow in range(6,10):
            cal[irow] = get_cal(f, f"row=={irow}")
        # Filter df to cal+-1 for each row
        filtered_file = f"Root_files/Analysis/Filtered/filtered_{Voltages[-1]}kV.root"
        df_filtered = df.Filter(" || ".join([f"row == {irow} && abs(cal - {cal[irow]}) < 2.5" for irow in range(6, 10)]))
        # Save filtered file
        df_filtered.Snapshot("Hits", filtered_file, {"tot_cal", "row"})

if __name__ == "__main__":
    main()