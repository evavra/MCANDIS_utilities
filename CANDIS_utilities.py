#!/usr/bin/python
import datetime as dt
import numpy as np
import new_baseline_table
import subprocess
import os, sys
import glob

# Utility functions for running MCANDIS
# Ellis Vavra, July 15, 2019


# ---------------------------- DRIVERS ----------------------------

def prepMCANDIS(intf_in, baseline_table):

    # Run in directory above interferograms
    # Inputs:
    # intf_in - list of interferograms to be used in common scene stacking
    # input_table - baseline_table.dat for scenes used in processing

    # Outputs:
    # dates.run - renamed list of interferograms to be used in common scene stacking
    # dates.dat - list of unique scenes used in processing
    #   Returned to command line as newList
    # baseline.dat - two column version of baseline_table.dat with only dates and perpendicular baseline
    #   Returned to command line as newTable

    newList = make_dates_to_use(intf_in)
    newTable = make_baseline_info(baseline_table)


def runMCANDIS(intf_in, baseline_table):

    # Prep input files
    prepMCANDIS(intf_in, baseline_table)



# ---------------------------- UTILITY FUNCTIONS ----------------------------

def make_dates_to_use(intf_in, code):

# Load dates into 'master' and 'slave' arrays
    print('Reading in dates...')

    with open(intf_in, "r") as file:
        origList = file.readlines()
    
    input_list = []
    master = []
    slave = []

    print()
    print('Masters: Slaves:')

    if code == 1: # Starting from intf.in
        for line in origList:
            # DONT use datetime because GMTSAR doesnt use real julian day convention
            input_list.append(line[0:15])
            # Find SLCs in each directory - they have the full YYYYMMDD dates that we want.
            print('Searching: ' + line[0:15] + "/*SLC")
            SLCs = glob.glob(line[0:15] + "/*SLC")
            print(SLCs)
            # Add their dates to the master and slave image lists
            master.append(SLCs[0][19:27])
            slave.append(SLCs[1][19:27] )
            print(master[-1] + '_' + slave[-1])

    elif code == 2: # Directories have already been renamed, so use dates.run instead of intf.in
        for line in origList:
            # DONT use datetime because GMTSAR doesnt use real julian day convention
            input_list.append(line[0:17])
            # Find SLCs in each directory - they have the full YYYYMMDD dates that we want.
            print('Searching: ' + line[0:17] + "/*SLC")
            SLCs = glob.glob(line[0:17] + "/*SLC")
            print(SLCs)
            # Add their dates to the master and slave image lists
            master.append(SLCs[0][21:29])
            slave.append(SLCs[1][21:29] )

    # Now find unique dates
    all_dates = master + slave
    unique_dates = []

    print()
    print('Unique dates:')
    for date in all_dates:
        if date not in unique_dates:
            unique_dates.append(date)
            print(date)

    # Write unique dates to new file "dates.dat"
    with open('dates.dat', 'w') as newList:
        for date in unique_dates:
            newList.write('%s\n' % date)

    print()
    print('File written:')
    print(newList)

    return newList


def make_baseline_info(baseline_table):
    # Load baseline_table.dat
    print('Reading in table...')

    orbit, dates, jday, blpara, blperp, datelabels = new_baseline_table.readBaselineTable(baseline_table)

    print(datelabels)

    with open('baseline.dat', 'w') as newTable:
        for i in range(len(datelabels)):
            newTable.write(datelabels[i] + " " + str(blperp[i]) + '\n')

    print()
    print('File written:')
    print(newTable)

    return newTable


def rename_intfs(intf_in):
    # Input:
    #   intf_in - GMTSAR formatted (YYYYDDD) interferogram directory list
    # Output:
    #   dates.run - Interferogram directory list renamed with MCANDIS format (YYYYMMDD)
    #   Also renames all directories in intf_in to the corresponding name in output_list

# Load dates into 'master' and 'slave' arrays
    print('Reading in dates...')


    with open(intf_in, "r") as file:
        origList = file.readlines()

    input_list = []
    master = []
    slave = []

    print()
    print('New filenames:')

    for line in origList:
        # DONT use datetime because GMTSAR doesnt use real julian day convention
        input_list.append(line[0:15])
        # Find SLCs in each directory - they have the full YYYYMMDD dates that we want.
        print('Searching: ' + line[0:15] + "/*SLC")
        SLCs = glob.glob(line[0:15] + "/*SLC")
        print(SLCs)
        # Add their dates to the master and slave image lists
        master.append(SLCs[0][19:27])
        slave.append(SLCs[1][19:27] )
        print(master[-1] + '_' + slave[-1])

# Use original input_list to write list in new format
    output_list = []
    with open('dates.run', 'w') as newfile:
        for i in range(len(master)):
            newfile.write(master[i]+ '_' + slave[i] + '\n')
            output_list.append(master[i] + '_' + slave[i])

        print()
        print('File written:')
        print(newfile)

# Use old and new lists to rename interferogram directories
    for i in range(len(input_list)):
        os.rename(input_list[i], output_list[i])
        print('Renamed ' + input_list[i] + ' to ' + output_list[i])

    # Show directory contents
    subprocess.call(['ls'], shell=False )

    return output_list



if __name__ == "__main__":
    #rename_intfs('intf.in')
    make_dates_to_use('dates.run', 2)

