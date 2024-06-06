import ROOT
import click
import math
import os
from array import array

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
    input_name = inputfiles[0].split('/')
    try:
        os.mkdir("Root_files")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"Root_files/{input_name[1]}")
    except FileExistsError:
        pass

    folder = inputfiles[0].split('/')[1:3]
    folder = f"{folder[0]}/{folder[1]}"

    hits = ROOT.TFile(f"Root_files/{folder}.root", "RECREATE")
    col = array('i', [0])
    row = array('i', [0])
    toa_code = array('i', [0])
    tot_code = array('i', [0])
    cal = array('i', [0])
    toa_cal = array('f', [0])
    tot_cal = array('f', [0])

    hits_tree = ROOT.TTree("Hits", "Hits")
    hits_tree.Branch("col", col, "col/I")
    hits_tree.Branch("row", row, "row/I")
    hits_tree.Branch("toa_code", toa_code, "toa_code/I")
    hits_tree.Branch("tot_code", tot_code, "tot_code/I")
    hits_tree.Branch("cal", cal, "cal/I")
    hits_tree.Branch("toa_cal", toa_cal, "toa_cal/F")
    hits_tree.Branch("tot_cal", tot_cal, "tot_cal/F")

    for inputfile in inputfiles:
        with open(inputfile) as f:
            lines = f.readlines()
            for l in lines:
                if l[0] == 'D':
                    _, _, _, icol, irow, itoa_code, itot_code, ical = l.strip().split()
                    icol, irow, itoa_code, itot_code, ical = int(icol), int(irow), int(itoa_code), int(itot_code), int(ical)
                    if ical != 0:
                        col[0] = icol
                        row[0] = irow
                        toa_code[0] = itoa_code
                        tot_code[0] = itot_code
                        cal[0] = ical
                        t_bin = T3 / cal[0]
                        tot_cal[0] = ((2 * tot_code[0] - math.floor(tot_code[0] / 32)) * t_bin)
                        toa_cal[0] = (t_bin * toa_code[0])
                        hits_tree.Fill()
    hits_tree.Write()
    hits.Write()
    hits.Close()

if __name__ == '__main__':
    main()


                
