# BIOLER PLATE ------------------------------------------------------------------------------------------------------


# FUNCTIONS ---------------------------------------------------------------------------------------------------------

# Takes every line in a file, seperates each part of the line by PARSE_BY, and makes that list an element of a list_of_lists
def make_list_and_parse_lines_from_document(filename, parse_by):
    f = open(filename)
    list_of_lists = []
    for l in f:
        line = l.strip().split(parse_by)
        list_of_lists += [line]
    f.close()
    return list_of_lists

# In a list of lists of strings and I want something specific in the list. So input is the list and the element of the thing I want
# Additionally, it adds "wget " to the beginning of every line, to create the bash script that will be run in Unix
def list_to_file_specific(list, number, out_file):
    f = open(out_file, "w")
    for i in list:
        if i == list[0]: # skip first line with the header
            continue
        else:
            f.write("wget " + i[number] + "\n")
    f.close()

# MAIN FUNCTION -----------------------------------------------------------------------------------------------------

# Variables:
filename_i = "fungiDB_taxid_species_name_strain_file.txt"
filename_o = "get_fasta_files_from_internet.txt"

output_list = make_list_and_parse_lines_from_document(filename_i, "\t")

# Run functions

list_to_file_specific(output_list, 2, filename_o)