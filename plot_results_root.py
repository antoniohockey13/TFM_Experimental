import numpy as np
import click
import matplotlib.pyplot as plt
import time
import math
import ROOT

ROOT.gROOT.SetBatch(False)

# Units
ns = 1
# Constants
T3 = 3.125 * ns

@click.command()
@click.argument('inputfiles', nargs=-1)
def main(inputfiles):
    """
    Process TOT and TOA data from input files and generate a 2D hit map.
    
    INPUTFILES: List of input files to process.
    """
    cal_code = []
    tot_code = []
    toa_code = []
    tot_cal = []
    toa_cal = []
    
    # Create a 2D histogram for the hit map with 16x16 pixels
    hit_map = ROOT.TH2F("hits", "Hit Map;Column;Row", 16, 0, 16, 16, 0, 16)
    tots_code = ROOT.TH1F("ToT_code", "Time over Threshold;ToT/code", 512, 0, 511)
    toas_code = ROOT.TH1F("ToA_code", "Time of Arrival;ToA/code", 1024, 0, 1023)
    tots = ROOT.TH1F("ToT", "Time over Threshold;ToT/ns", 50000, 0, 2000)
    toas = ROOT.TH1F("ToA", "Time of Arrival;ToA/ns", 500, 0, 150)
    cals = ROOT.TH1F("Cal", "Calibration;Cal", 1024, 1, 1024)

    # ETROC 1
    tots_code_1 = ROOT.TH1F("ToT_code_1", "Time over Threshold ETROC 1;ToT/code", 512, 0, 511)
    toas_code_1 = ROOT.TH1F("ToA_code_1", "Time of Arrival ETROC 1;ToA/code", 1024, 0, 1023)
    tots_1 = ROOT.TH1F("ToT_1", "Time over Threshold ETROC 1;ToT/ns", 50000, 0, 2000)
    toas_1 = ROOT.TH1F("ToA_1", "Time of Arrival ETROC 1;ToA/ns", 500, 0, 150)
    cals_1 = ROOT.TH1F("Cal", "Calibration ETROC 1;Cal", 1024, 1, 1024)

    # ETROC 2
    tots_code_2 = ROOT.TH1F("ToT_code_2", "Time over Threshold ETROC 2;ToT/code", 512, 0, 511)
    toas_code_2 = ROOT.TH1F("ToA_code_2", "Time of Arrival ETROC 2;ToA/code", 1024, 0, 1023)
    tots_2 = ROOT.TH1F("ToT_2", "Time over Threshold ETROC 2;ToT/ns", 50000, 0, 2000)
    toas_2 = ROOT.TH1F("ToA_2", "Time of Arrival ETROC 2;ToA/ns", 500, 0, 150)
    cals_2 = ROOT.TH1F("Cal", "Calibration ETROC 2;Cal", 1024, 1, 1024)

    # ETROC 3
    tots_code_3 = ROOT.TH1F("ToT_code_3", "Time over Threshold ETROC 3;ToT/code", 512, 0, 511)


    for inputfile in inputfiles:
        with open(inputfile) as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == 'D':
                    # Parse the line

                    _, _, _, col, row, toa, tot, cal = line.strip().split()
                    col, row, toa, tot, cal = int(col), int(row), int(toa), int(tot), int(cal)
                    cal += 1 # Add 1 to avoid 0 calibration and dividing by 0 error

                    cal_code.append(cal)
                    tot_code.append(tot)
                    toa_code.append(toa)

                    #Fill code histograms
                    tots_code.Fill(tot)
                    toas_code.Fill(toa)
                    
                    t_bin = T3 / cal
                    tot = ((2 * tot - math.floor(tot / 32)) * t_bin)
                    toa = (t_bin * toa)
                                    
                    # Fill the histograms
                    hit_map.Fill(row, col)
                    tots.Fill(tot)
                    toas.Fill(toa)
                    cals.Fill(cal)
                    tot_cal.append(tot)
                    toa_cal.append(toa)


    print(f"max TOT_code = {max(tot_code)}, min TOT_code = {min(tot_code)}")
    print(f"max TOA_code = {max(toa_code)}, min TOA_code = {min(toa_code)}")
    print(f"max CAL = {max(cal_code)}, min CAL = {min(cal_code)}")
    print(f"max TOT_cal = {max(tot_cal)}, min TOT_cal = {min(tot_cal)}")
    print(f"max TOA_cal = {max(toa_cal)}, min TOA_cal = {min(toa_cal)}")
    print(f"Total hits: {len(tot_code)}")

    # Hit map
    c = ROOT.TCanvas("c", "Hit Map Canvas", 800, 600)
    c.SetLogz()
    hit_map.Draw('COLZ')
    c.Draw()
    input('Press any key...')
    # Tot Code
    c1 = ROOT.TCanvas("c1", "ToT Code Canvas", 800, 600)
    tots_code.Draw()
    c1.Draw()
    input('Press any key...')
    # Tot
    c2 = ROOT.TCanvas("c2", "ToT Canvas", 800, 600)
    tots.Draw()
    c2.Draw()
    input('Press any key...')
    # Toa Code
    c3 = ROOT.TCanvas("c3", "ToA Code Canvas", 800, 600)
    toas_code.Draw()
    c3.Draw()
    input('Press any key...')

    # Toa
    c4 = ROOT.TCanvas("c4", "ToA Canvas", 800, 600)
    toas.Draw()
    c4.Draw()
    input('Press any key...')
    # Cal
    c5 = ROOT.TCanvas("c5", "Cal Canvas", 800, 600)
    cals.Draw()
    c5.Draw()
    input('Press any key...')

if __name__ == '__main__':
    main()
