# BOILER PLATE ---------------------------------------------------------------------------------------------------------
import shutil

# FUNCTIONS ------------------------------------------------------------------------------------------------------------

# This takes every line in a text file, parses it by "parse_by" and selects "placek" for the key and "placev"
# as the value.
# NOTE: this was made specifically for csv files, hence the absence of any line that starts with #


def make_dictionary_from_document(filename, parse_by, placek, placev):
    f = open(filename)
    dict = {}
    for l in f:
        line = l.strip().split(parse_by)
        if not line[0][0] == "#":
            dict[line[placek]] = [line[placev]]
    f.close()
    return dict

# special function for the file "directory_and_contents_with_filenames.txt" to make it into a dictionary
# where the directory names are keys and the filenames inside are values

def special_dictionary_from_document(filename):
    f = open(filename)
    dict = {}
    val = ""
    key = ""
    track = 0
    for l in f:
        line = l.strip()
        if track == 2:
            dict[key] = [val]
            track = 0
        elif track == 0:
            line = line[:-1] # remove the ":" at the end of the line
            key = line
            track += 1
        elif track == 1:
            val = line
            track += 1
    f.close()
    return dict

# Match file names with taxIDs and create a new csv file
# dict1 = directory -> taxID
# dict2 = directory -> file


def match_and_rewrite(output_filename, dict1, dict2):
    u = open(output_filename, "w")
    u.write("# TaxID    filename    directory\n")
    for i in dict1.keys():
        direct_name = i
        tax = dict1[i]
        file = dict2[direct_name]
        u.write("\t".join([tax[0], file[0], direct_name]) + "\n")

    # handle the two special cases
    # the commented out lines were put back into the text file so that the core would run
    # properly at line 56

    # u.write("\t".join(list([dict1["Ascsa1"], "Ascocoryne_sarcoides.allmasked.gz", "Ascsa1"])) + "\n")
    u.write("\t".join(list([dict1["Ascsa1"][0], "Ascsa1_AssemblyScaffolds_Repeatmasked.fasta.gz", "Ascsa1"])) + "\n")
    # u.write("\t".join(list([dict1["CocheC5_3"], "CocheC5_1_assembly_scaffolds_repeatmasked.fasta.gz", "CocheC5_3"])) + "\n")
    u.write("\t".join(list([dict1["CocheC5_3"][0], "CocheC5_3_AssemblyScaffolds_Repeatmasked.fasta.gz", "CocheC5_3"])) + "\n")

    u.close()
    return


# Create a csv file from a list of lists
# This joins the entries of that list by tabs


def create_csv(list_of_lists, first_line, output_filename):
    f = open(output_filename, "w")
    f.write(first_line)
    for i in list_of_lists:
        f.write("\t".join(i) + "\n")
    f.close()


# MAIN FUNCTI0N --------------------------------------------------------------------------------------------------------

# Set up the variables:
# for the file names
orgininal_csv = "1k_taxid_filenames.txt"
file_with_filename_info = "directory_and_contents_with_fileneames.txt"
output_filename = "new_1k_taxid_filenames.txt"

# Use functions:
# get dictionaries:
orig_dict = make_dictionary_from_document(orgininal_csv, "\t", 1, 0)
files_dict = special_dictionary_from_document(file_with_filename_info)

# make comparisons and write the new file
match_and_rewrite(output_filename, orig_dict, files_dict)

# Save the text file we just created to the parent folder of the current folder.
shutil.copy(output_filename, "..")

print("DONE")