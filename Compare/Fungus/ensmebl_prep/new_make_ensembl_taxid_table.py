# BOILER PLATE ---------------------------------------------------------------------------------------------------------------------
import string
import shutil

# FUNCTIONS ------------------------------------------------------------------------------------------------------------------------

# Takes every line in a file, separates each part of the line by PARSE_BY. One of these elements becomes the key
# and the other is the value. These variables are preset.
# In this script it will be used to parse ensembl_db.txt to get all the elements into
# a variable that can be used.


def make_dictionary_from_document(filename, parse_by):
    f = open(filename)
    dict = {}
    for l in f:
        line = l.strip().split(parse_by)
        if not line[0][0] == "#":
            dict[string.capwords(line[1], " ")] = [line[3]]
    f.close()
    return dict

# Takes every line in a file and makes it an element of a list. In this script it will be used to get all the
# filenames for ensembl that are currently found on the hoffman cluster (at the moment there is one missing of
# the 811 files that are supposed to be there).


def make_list_from_document(filename):
    f = open(filename)
    list = []
    for l in f:
        line = l.strip()
        list += [line]
    f.close()
    return list

# This function was created to serve a specific purpose in this script. It takes a dictionary where the keys are
# the "species division" column of "ensembl_db.txt" and the values are the "taxonomy_id" column of the same file.
# The list taken is the list of file names for the ensembl fungal references found on Hoffman. The elements of
# this list are parsed by "." and the first part is matched up to a key in the dictionary.
# The full, unparsed file name from the input list and the taxID that it is matched with are then placed together
# as a list element in a list of lists. This list_of_lists is returned.


def match_filename_to_taxID(db_dict, file_list):
    to_print = []
    for i in file_list:
        l = i.split(".")[0]
        to_print += [[db_dict[l][0], i]]
    return to_print

# create a csv file from a list of lists. This particular function creates a text file called
# "ensembl_taxID_filename.txt". This file will be copied to the parent folder "Fungus"


def create_csv(list, output_filename):
    f = open(output_filename, "w")
    for i in list:
        f.write("\t".join(i) + "\n")
    f.close()


#MAIN FUNCTION ---------------------------------------------------------------------------------------------------------------------

# Set up Variables:
input_filename_db = "ensembl_db.txt"
input_filename_files = "Filename_list_from_hoffman.txt"
output_filename = "ensembl_taxID_filename.txt"

# Use functions:
# Make text files into usable variables
en_dict = make_dictionary_from_document(input_filename_db, "\t")
files = make_list_from_document(input_filename_files)

# Match the filenames with the taxIDs
print_this = match_filename_to_taxID(en_dict, files)

# Make the csv file as a text file wih header "taxID    filename"
create_csv(print_this, output_filename)

# Save the text file we just created to the parent folder of the current folder.
shutil.copy(output_filename, "..")

print("DONE")