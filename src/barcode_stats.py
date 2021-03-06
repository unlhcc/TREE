'''
       barcode_stats.py

       Input: provide path to input ripser files and desired output folder.

       Usage: python barcode_stats.py -i  <path/to/sequence/files> -o
       </path/to/output/folder/>

      Authors: Devon Humphreys, Melissa McGuirl, Michael Miyagi
      Corresponding Author: Melissa McGuirl (melissa_mcguirl@brown.edu)
      Updated: 05/10/18
 '''

import sys, os
import numpy as np
import argparse
import glob

# A function that extracts barcodes from ripser output
# This function is for old version of Ripser.
def getBars(RipserFile):

    inFile = open(RipserFile, 'r')
    lines = inFile.read().splitlines()
    dim0 = []
    dim1 = []
    # get endpoint while extracting lines
    count = 0
    for line in lines:
        if line != '':
            line = line.split(",")
            start_point = float(line[0])
            try:
                end_point = float(line[1])
            except ValueError:
                end_point = ''

            if start_point == 0:
                dim0.append([start_point, end_point])
            elif start_point != 0:
                dim1.append([start_point, end_point])
    dim0.remove([0.0, ''])
    end_point = lines[1].split(',')[1]
            # if count ==0:
            #     line = line.split(',')
            #     end_point = line[1]
            #     count = 1
            #
            # elif count ==1:
            #     count = 2
            # elif count ==2:
            #                 # Add dimension 0 bars
            #     if line != '':
            #         line = line.split(',')
            #         dim0.append([line[0], line[1]])
            #     else:
            #                         # moving into dimension 1
            #         count = 3
            # elif count ==3:
            #     if line != '':
            #                         # add in dimension 1 bars
            #         line = line.split(',')
            #         dim1.append([line[0], line[1]])
            #     else:
            #         count = 4
    return end_point, dim0, dim1

# A function that extracts TREE barcode stats from barcode data
def barStats(endpoint, dim0, dim1, BarcodeFile):
    barlengths0 = []
    barlengths1 = []

	# compute all barlengths
    if len(dim0) > 1:
        for i in range(len(dim0) - 1):
            barlengths0.append(float(dim0[i][1]) - float(dim0[i][0]))
        barlengths0.append(max(barlengths0))
    else:
        barlengths0.append(endpoint)

        # repeat for dim 1
    for i in range(len(dim1)):
        barlengths1.append(float(dim1[i][1]) - float(dim1[i][0]))

        # compute psi and phi
    if barlengths0 != []:
        try:
            avg0 = np.mean(barlengths0)
            var0 = np.var(barlengths0)
        except TypeError:
            barlengths0 = [float(barlengths0[i]) for i in range(len(barlengths0))]
            avg0 = np.mean(barlengths0)
            var0 = np.var(barlengths0)
    else:
        avg0 = 0
        var0 = 0

        # compute betti1
    if barlengths1 != []:
        betti1 = len(barlengths1)
    else:
        betti1 = 0


    barcodestats = [avg0, var0, betti1]
    np.savetxt(BarcodeFile, barcodestats)



def main():

	descriptor = "Extracts barcode statistics from ripser files and saves them to a np file "
	parser = argparse.ArgumentParser(description = descriptor)
	parser.add_argument('-i', '--indir', required = True, action = 'store',
			    help = 'provide path to Ripser files')
	parser.add_argument('-o', '--outdir', required = True, action = 'store',
			    help = 'provide name of desired output directory')

	args = parser.parse_args()

	os.chdir(args.indir)


	for file in glob.glob('Rip*'):
		RipserFile = file
		OUT = args.outdir + '/bstats-' + RipserFile[7::]

		end_point, dim0, dim1 = getBars(RipserFile)
		barStats(end_point,dim0, dim1, OUT)

if __name__ == "__main__":
	main()
