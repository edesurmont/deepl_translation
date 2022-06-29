# import
import csv

# the file to cut
file_to_cut = "tour_translations.csv"
# the filename whithout extension, so that we can add 
# "_part_i.csv" at the end of it
filename_no_extension = file_to_cut.split(".")[0]

# the number of rows per file
max_rows = 400

# returns the data from the file 
def get_data():
    data = []
    with open(file_to_cut, newline='') as data_file:
        datareader = csv.reader(data_file, delimiter=',', quotechar='"')
        for row in datareader:
            data.append(row)
    return data

# divides the data into parts
def cut(data):
    data_cut = []
    nb_it = len(data) // max_rows

    # adding everything
    for i in range(nb_it):
        data_cut.append([data[k] for k in range(i*max_rows, (i+1)*max_rows)])
    # adding the rest
    rest = [data[k] for k in range(nb_it*max_rows, len(data))]
    if len(rest) != 0:
        data_cut.append(rest)

    return data_cut

# writes the different parts to the files, and adds the first line to every part
def write_data(header, data_cut):
    for i in range(len(data_cut)):
        with open(filename_no_extension + "_part_" + str(i+1) + ".csv", 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(header)
            for row in data_cut[i]:
                spamwriter.writerow(row)

def main():
    data = get_data()

    header = data[0]
    data.pop(0)

    data_cut = cut(data)

    write_data(header, data_cut)

if __name__ == "__main__":
    main()
