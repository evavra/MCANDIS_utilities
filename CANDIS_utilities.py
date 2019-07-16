import datetime as dt
import numpy as np
import new_baseline_table
import subprocess

# Utility functions for running MCANDIS
# Ellis Vavra, July 15, 2019


# ---------------------------- DRIVERS ----------------------------

def prepMCANDIS(input_list, input_table):

    # Run in directory above interferograms
    # Inputs:
    # input_list - list of interferograms to be used in common scene stacking
    # input_table - baseline_table.dat for scenes used in processing

    # Outputs:
    # dates.run - renamed list of interferograms to be used in common scene stacking
    # dates.dat - list of unique scenes used in processing
    #   Returned to command line as newList
    # baseline.dat - two column version of baseline_table.dat with only dates and perpendicular baseline
    #   Returned to command line as newTable
    rename(input_list)
    newList = make_dates_to_use(input_list)
    newTable = make_baseline_info(input_table)


def runMCANDIS(input_list, input_table):

    # Prep input files
    prepMCANDIS(input_list, input_table)

    #


# ---------------------------- INPUTS ----------------------------
def rename_intf_list(input_list):
    print()
    subprocess.call(['cp', input_list, 'dates.run'], shell=False)
    print('Copied ' + input_list + ' to dates.run')

    print()

def make_dates_to_use(input_list):

# Load dates into 'master' and 'slave' arrays
    print('Reading in dates...')

    with open(input_list, "r") as file:
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



def make_baseline_info(input_table):
    # Load baseline_table.dat
    print('Reading in table...')

    orbit, dates, jday, blpara, blperp, datelabels = new_baseline_table.readBaselineTable(input_table)

    print(datelabels)

    with open('baseline.dat', 'w') as newTable:
        for i in range(len(datelabels)):
            newTable.write(datelabels[i] + " " + str(blperp[i]) + '\n')

    print()
    print('File written:')
    print(newTable)

    return newTable



if __name__ == "__main__":

    prepMCANDIS('Sp2017_Sp2018_intf.in', 'baseline_table.dat')


