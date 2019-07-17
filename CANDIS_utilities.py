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

def make_dates_to_use(intf_in):

# Load dates into 'master' and 'slave' arrays
    print('Reading in dates...')

    with open(intf_in, "r") as file:
        origList = file.readlines()

    master = []
    slave = []

    print()
    print('Masters: Slaves:')

    for line in origList:
        master.append(dt.datetime.strptime(line[0:7],"%Y%j"))
        slave.append(dt.datetime.strptime(line[8:15],"%Y%j"))

        print(master[-1].strftime("%Y%j") + '  ' + slave[-1].strftime("%Y%j"))

    # Now find unique dates
    all_dates = master + slave
    unique_dates = []

    print()
    print('Unique dates:')
    for date in all_dates:
        if date not in unique_dates:
            unique_dates.append(date)
            print(date.strftime("%Y%m%d"))

    # Write unique dates to new file "dates.dat"
    with open('dates.dat', 'w') as newList:
        for date in unique_dates:
            newList.write('%s\n' % date.strftime("%Y%m%d"))

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

        # Find SLCs in each directory - they have the full YYYYMMDD dates that we want.
        SLCs = glob.glob(line + "/*SLC")
        print(SLCs)
        # Add their dates to the master and slave image lists
        master.append(SLCs[0][3:11])
        slave.append(SLCs[1][3:11] )
        print(master[-1] + '_' + slave[-1])

        # OLD
        # input_list.append(line[0:15])
        # master.append(dt.datetime.strptime(line[0:7],"%Y%j"))
        # slave.append(dt.datetime.strptime(line[8:15],"%Y%j"))
        # print(master[-1].strftime("%Y%j") + '_' + slave[-1].strftime("%Y%j"))


# Use original input_list to write list in new format
    output_list = []
    with open('dates.run', 'w') as newfile:
        for i in range(len(master)):
            newfile.write(master[i].strftime("%Y%m%d") + '_' + slave[i].strftime("%Y%m%d") + '\n')
            output_list.append(master[i].strftime("%Y%m%d") + '_' + slave[i].strftime("%Y%m%d"))\

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
    rename_intfs('intf.in')


