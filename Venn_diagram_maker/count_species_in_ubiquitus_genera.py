# BOILER PLATE --------------------------------------------------------------------------------------------------------------------------

# FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------

# Takes every line in a file, separates each part of the line by PARSE_BY, and makes that
# list an element of a list_of_lists

def make_list_and_parse_lines_from_document(filename, parse_by):
    f = open(filename)
    list_of_lists = []
    for l in f:
        line = l.strip().split(parse_by)
        list_of_lists += [line]
    f.close()
    return list_of_lists

# This function takes a text file of species names (set up so that the genus name is first). It will then create a
# dictionary. The keys will be the genera names, and the values will be the number of species in that genera in the
# list. Returns the dictionary.
# NOTE: this function does not check for duplicates. So if a species is listed twice, it will be counted twice.


def file_to_dictionary_count_addition(filename):
    l = make_list_and_parse_lines_from_document(filename, " ")
    lines = []
    for i in l:
        lines += [[i[0], " ".join(i[1:])]]
    dictionary = {}
    for j in lines:
        if not j[0] in dictionary.keys():
            dictionary[j[0]] = 1
        elif j[0] in dictionary.keys():
            dictionary[j[0]] += 1
    return dictionary


# This function takes in three dictionaries where the keys are strings and the value is a number. It creates a csv file
# named "Species_count_in_genera_found_in_all.txt" which is formated like a csv file. with header #genera_name D1 D2 D3,
# where D#
# is the number of species of genera_name in that particular database (at least that is what the number means in this
# script).
# It only outputs genera that are in all three databases.
# All the columns of the file are separated by tabs.


def make_csv(d1, d2, d3, d1_name, d2_name, d3_name):
    f = open("Species_count_in_genera_found_in_all.txt", "w")
    header = "\t".join(list(["#genera_name", d1_name, d2_name, d3_name + "\n"]))
    f.write(header)
    for i in d1.keys():
        if i in d2.keys() and i in d3.keys(): # only want genera found in all databases
            f.write("\t".join([i, str(d1[i]), str(d2[i]), str(d3[i]) + "\n"]))
    f.close()


# MAIN FUNCTION --------------------------------------------------------------------------------------------------------------------------

# Initialize variables:
# text files with list of species names. These text files must be prepared before hand.
onek_species_filename = "1000G_Species.txt"
ncbi_species_filename = "NCBI_species.txt"
ensembl_species_filename = "Ensembl_species.txt"

# Use functions
# Make dictionaries
onek_dict = file_to_dictionary_count_addition(onek_species_filename)
ncbi_dict = file_to_dictionary_count_addition(ncbi_species_filename)
ensembl_dict = file_to_dictionary_count_addition(ensembl_species_filename)

# make the text file named "Species_count_in_genera_found_in_all.txt"
make_csv(onek_dict, ncbi_dict, ensembl_dict, "1000G", "NCBI", "Ensembl")

print("DONE")