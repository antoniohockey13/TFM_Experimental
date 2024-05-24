import ROOT
import click
import math
import os

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
    hits_tree = ROOT.TTree("Hits", "Hits")
    col = ROOT.vector('int')()
    row = ROOT.vector('int')()
    toa_code = ROOT.vector('int')()
    tot_code = ROOT.vector('int')()
    cal = ROOT.vector('int')()
    toa_cal = ROOT.vector('double')()
    tot_cal = ROOT.vector('double')()

    for inputfile in inputfiles:
        with open(inputfile) as f:
            lines = f.readlines()
            for l in lines:
                if l[0] == 'D':
                    _, _, _, icol, irow, itoa_code, itot_code, ical = l.strip().split()
                    icol, irow, itoa_code, itot_code, ical = int(icol), int(irow), int(itoa_code), int(itot_code), int(ical)+1
                    it_bin = T3 / ical
                    itot_cal = ((2 * itot_code - math.floor(itot_code / 32)) * it_bin)
                    itoa_cal = (it_bin * itoa_code)

                    col.push_back(icol)
                    row.push_back(irow)
                    toa_code.push_back(itoa_code)
                    tot_code.push_back(itot_code)
                    cal.push_back(ical)
                    toa_cal.push_back(itoa_cal)
                    tot_cal.push_back(itot_cal)

    hits_tree.Branch("col", col)
    hits_tree.Branch("row", row)
    hits_tree.Branch("toa_code", toa_code)
    hits_tree.Branch("tot_code", tot_code)
    hits_tree.Branch("cal", cal)
    hits_tree.Branch("toa_cal", toa_cal)
    hits_tree.Branch("tot_cal", tot_cal)

    hits_tree.Fill()
    hits_tree.Write()
    hits.Write()
    hits.Close()

if __name__ == '__main__':
    main()


                
