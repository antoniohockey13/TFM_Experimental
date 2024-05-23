import numpy as np
import click
import matplotlib.pyplot as plt
import time
import math
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(111111)

# Units
ns = 1
# Constants
T3 = 3.125 * ns
FORMAT = ".png"

@click.command()
@click.argument('inputfiles', nargs=-1)
def main(inputfiles):
    """
    Process TOT and TOA data from input files and generate a 2D hit map.
    
    INPUTFILES: List of input files to process.
    """
    cals_code_list = []
    tots_code_list = []
    toas_code_list = []
    tots_cal_list = []
    toas_cal_list = []
    tots_code = {}
    toas_code = {}
    tots = {}
    toas = {}
    cals = {}
    toas_vs_cal = {}
    tot_vs_toa = {}
    # Create a 2D histogram for the hit map with 16x16 pixels
    hit_map = ROOT.TH2F("hits", "Hit Map;Column;Row", 16, 0, 16, 16, 0, 16)
    for i in range(5):
        toas_vs_cal[i] = ROOT.TH2F(f"ToA_vs_Cal{i}", f"Time of Arrival vs Calibration {i};ToA;Cal", 500, 0, 25, 1024, 1, 1024)
        tot_vs_toa[i] = ROOT.TH2F(f"ToT_vs_ToA{i}", f"Time over Threshold vs Time of Arrival {i};ToT;ToA", 500, 0, 25, 500, 0, 15)
        tots_code[i] = ROOT.TH1F(f"ToT_code{i}", f"Time over Threshold {i};ToT/code", 512, 0, 511)
        toas_code[i] = ROOT.TH1F(f"ToA_code{i}", f"Time of Arrival {i};ToA/code", 1024, 0, 1023)
        # tots range 0 - 3144
        tots[i] = ROOT.TH1F(f"ToT{i}", f"Time over Threshold {i};ToT/ns", 500, 0, 25)
        # toas range 0 - 3197
        toas[i] = ROOT.TH1F(f"ToA{i}", f"Time of Arrival {i};ToA/ns", 500  , 0, 15)
        cals[i] = ROOT.TH1F(f"Cal{i}", f"Calibration {i};Cal", 1024, 1, 1024)

    for inputfile in inputfiles:
        with open(inputfile) as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == 'D':
                    # Parse the line
                    _, _, _, col, row, toa_code, tot_code, cal = line.strip().split()
                    col, row, toa_code, tot_code, cal = int(col), int(row), int(toa_code), int(tot_code), int(cal)
                    cal += 1 # Add 1 to avoid 0 calibration and dividing by 0 error
                    cals_code_list.append(cal)
                    tots_code_list.append(tot_code)
                    toas_code_list.append(toa_code)

                    t_bin = T3 / cal
                    tot_cal = ((2 * tot_code - math.floor(tot_code / 32)) * t_bin)
                    toa_cal = (t_bin * toa_code)

                    #Fill histograms
                    hit_map.Fill(row, col)
                    tots_code[0].Fill(tot_code)
                    toas_code[0].Fill(toa_code)
                    
                    tots[0].Fill(tot_cal)
                    toas[0].Fill(toa_cal)
                    cals[0].Fill(cal)
                    toas_vs_cal[0].Fill(toa_cal, cal)
                    tot_vs_toa[0].Fill(tot_cal, toa_cal)
                    tots_cal_list.append(tot_cal)
                    toas_cal_list.append(toa_cal)
                    
                    if row in range(6, 10):
                        index = row - 5
                        tots_code[index].Fill(tot_code)
                        toas_code[index].Fill(toa_code)
                        tots[index].Fill(tot_cal)
                        toas[index].Fill(toa_cal)
                        cals[index].Fill(cal)
                        toas_vs_cal[index].Fill(toa_cal, cal)
                        tot_vs_toa[index].Fill(tot_cal, toa_cal)

    print(f"max TOT_code = {max(tots_code_list)}, min TOT_code = {min(tots_code_list)}")
    print(f"max TOA_code = {max(toas_code_list)}, min TOA_code = {min(toas_code_list)}")
    print(f"max CAL = {max(cals_code_list)}, min CAL = {min(cals_code_list)}")
    print(f"max TOT_cal = {max(tots_cal_list)}, min TOT_cal = {min(tots_cal_list)}")
    print(f"max TOA_cal = {max(toas_cal_list)}, min TOA_cal = {min(toas_cal_list)}")
    print(f"Total hits: {len(tots_code_list)}")

    save_histograms(hit_map, tots_code, toas_code, tots, toas, cals, toas_vs_cal, tot_vs_toa)


def save_histograms(hit_map, tots_code, toas_code, tots, toas, cals, toas_vs_cal, tot_vs_toa):
    # Hit map
    c = ROOT.TCanvas("c", "Hit Map Canvas", 800, 600)
    # c.SetLogz()
    hit_map.Draw('COLZ')
    c.SaveAs(f"Pictures/hit_map{FORMAT}")
    
    for i in range(5):
        save_canvas(f"ToT Code {i}", tots_code[i], f"tot_code_{i}")
        save_canvas(f"ToT {i}", tots[i], f"tot_{i}")
        save_canvas(f"ToA Code {i}", toas_code[i], f"toa_code_{i}")
        save_canvas(f"ToA {i}", toas[i], f"toa_{i}")
        save_canvas(f"Cal {i}", cals[i], f"cal_{i}")
        save_canvas(f"ToA vs Cal {i}", toas_vs_cal[i], f"toa_vs_cal_{i}")
        save_canvas(f"ToT vs ToA {i}", tot_vs_toa[i], f"tot_vs_toa_{i}")

def save_canvas(title, histogram, filename):

    c = ROOT.TCanvas(title, title, 800, 600)
    histogram.Draw()
    c.Draw()
    # input("Press Enter to continue...")
    c.SaveAs(f"Pictures/{filename}{FORMAT}")

if __name__ == '__main__':
    main()
