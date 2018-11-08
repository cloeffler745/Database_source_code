# BOILER PLATE ---------------------------------------------------------------------------------------------------------


# FUNCTIONS ------------------------------------------------------------------------------------------------------------

# Isolate the column of the inputed csv file that has the taxIDs. These TaxIDs will then be put through the
# website https://www.ncbi.nlm.nih.gov/Taxonomy/TaxIdentifier/tax_identifier.cgi to get the species names
# that will be inputed into the csv file.

def csv_to_list(i_filename, o_filename, desired_column):
    # get the values
    f = open(i_filename)
    list_of_values = []
    for l in f:
        line = l.strip().split("\t")
        if not line[0] == "#":
            list_of_values += [line[desired_column]]
    f.close()

    # put value in a new text file for easy input to the website
    # https://www.ncbi.nlm.nih.gov/Taxonomy/TaxIdentifier/tax_identifier.cgi
    u = open(o_filename, "w")
    for i in list_of_values:
        u.write(str(i) + "\n")
    u.close()
    return


# MAIN FUNCTION --------------------------------------------------------------------------------------------------------

# set up variables...
# Input file names for all three text files

onek_i_file = "new_1k_taxid_filenames.txt"
ensembl_i_file = "ensembl_taxID_filename.txt"

# Output file names for all three text files

onek_o_file = "onek_taxid_list.txt"
ensembl_o_file = "ensembl_taxid_list.txt"

# Use the functions...
# Make the text files for the taxIDs only

csv_to_list(onek_i_file, onek_o_file, 0)
csv_to_list(ensembl_i_file, ensembl_o_file, 0)

# NOTE: the taxid file for NCBI already has species names.

print("DONE")