import csv


def open_csv_recordings(filename):
    recordings = []
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            recordings.append(row)
    return recordings