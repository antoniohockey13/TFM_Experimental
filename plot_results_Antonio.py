import numpy as np
import click
import matplotlib.pyplot as plt
import math

#import ROOT
# Constants
T3 = 3.125


@click.command()
@click.argument('inputfiles', nargs=-1)
def main(inputfiles):
    """
    """


    # 2 dimensions and 
    hit_map = np.zeros((16,16))
    tots= []
    toas= []
    cals= []
    #hit_map = ROOT.TH2F("hits","",0,15,0,15)
    
    for inputfile in inputfiles:
        with open(inputfile) as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == 'D':
                    _,_,_,col,row,toa,tot,cal = line.replace("\n","").split(" ")
                    if int(cal) == 0:
                        # print("ERROR cal = 0\n ----------------------------------------")
                        continue

                    hit_map[int(col),int(row)] += 1
                    t_bin = T3/int( cal )
                    tots.append( (2*int(tot)-math.floor(int(tot)/32))*t_bin )
                    toas.append( t_bin*int(toa) )
                    cals.append( int(cal) )
                    #hit_map.Fill(int(col), int(row))

    #c = ROOT.TCanvas()
    #c.SetLogz()
    #hit_map.Draw('colz')
    #input('Press any key...')

    hit_map = np.log10(hit_map)
    
    fig = plt.figure()
    ax0 = fig.add_subplot()
    img0 = ax0.imshow(hit_map)
    ax0.title(f"ToT")
    ax0.set_aspect("equal")
    ax0.invert_xaxis()
    ax0.invert_yaxis()
    plt.xticks(range(16), range(16), rotation="vertical")
    plt.yticks(range(16), range(16), rotation="vertical")
    fig.colorbar(img0, orientation="vertical")
    plt.show()


    counts,bins = np.histogram(np.array(tots),100)
    plt.hist(bins[:-1], bins, weights=counts)
    plt.title("ToT")
    plt.x_axis("t/ns")
    #plt.hist(100, np.linspace(0,100,100), np.array(tots))

    plt.show()
    
    counts,bins = np.histogram(np.array(toas),150)
    plt.hist(bins[:-1], bins, weights=counts)
    plt.title("ToA")
    plt.x_axis("t/ns")
    plt.show()

    print(f"Total hits: {len(tots)}")

if __name__ == '__main__':
    main()
