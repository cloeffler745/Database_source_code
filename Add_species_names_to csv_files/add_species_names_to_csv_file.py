# BOILER PLATE ---------------------------------------------------------------------------------------------------------


# FUNCTIONS ------------------------------------------------------------------------------------------------------------

# Takes the output from the website  https://www.ncbi.nlm.nih.gov/Taxonomy/TaxIdentifier/tax_identifier.cgi
# found in the files ending with "_output_from_website.txt" and creates a dictionary where the keys are taxids
# and the values are the species names (at least that is how this function is going to be used in this
# script).
# placek = column number of the value we want to be the key
# placev = column number of the value we want to be the value of the dictionary


def make_directory_from_document(filename, placek, placev):
    f = open(filename)
    dict = {}
    for l in f:
        line = l.strip().split("\t")
        if not line[0][0] == "#" and not line[placek] in dict.keys(): # don't want the header, if there is one
            dict[line[placek]] = [line[placev]]
    f.close()
    return dict

# takes in the current database cwsv files that do nto have the species names in them, and the dictionary
# of taxid -> species names. It will create a new csv file that appends the species names as the last
# column in the file.


def append_species_name_to_csv_file(in_filename, out_filename, dict, taxid_pos):
    f = open(in_filename)  # current csv file
    u = open(out_filename, "w")  # new csv file

    for l in f:
        if l[0] == "#":
            u.write(l.strip() + "\tSpecies name\n" )
        else:
            line = l.strip().split("\t")
            u.write(l.strip() + "\t" + dict[line[taxid_pos]][0] + "\n")

    u.close()
    f.close()
    return


# MAIN FUNCTION --------------------------------------------------------------------------------------------------------
# NOTE: the NCBI already has species names in the csv file, so it was not included

# Setup variables...
# input file names:
# ...for the original csv files
onek_i_filename = "new_1k_taxid_filenames.txt"
ensembl_i_filename = "ensembl_taxID_filename.txt"

# ...for the website output
onek_i_website = "onek_output_from_website.txt"
ensembl_i_website = "ensembl_output_from_website.txt"

# output file names
onek_o_filename = "updated_onek_csv.txt"
ensembl_o_filename = "updated_ensembl_csv.txt"


# Use functions...
# to get the dictionary for the two databases
onek_dict = make_directory_from_document(onek_i_website, 1, 3)
ensembl_dict = make_directory_from_document(ensembl_i_website, 1, 3)

# to update the csv files
append_species_name_to_csv_file(onek_i_filename, onek_o_filename, onek_dict, 0)
append_species_name_to_csv_file(ensembl_i_filename, ensembl_o_filename, ensembl_dict, 0)




print("DONE")