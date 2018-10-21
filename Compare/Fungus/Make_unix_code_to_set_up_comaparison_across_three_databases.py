# BOILER PLATE ---------------------------------------------------------------------------------------------------------------


# FUNCTIONS ----------------------------------------------------------------------------------------------------------------------

# This function was built to take in csv files and turn them into lists of lists, where every element of the
# list is an individual row of the csv file and ever element of the sublist are the entries for each column
# of that particular row
# returns this list of lists


def make_list_and_parse_lines_from_document(filename, parse_by):
    f = open(filename)
    list_of_lists = []
    for l in f:
        line = l.strip().split(parse_by)
        list_of_lists += [line]
    f.close()
    return list_of_lists

# This function takes in a list of lists (which is a parsed csv file) and the position of the value that
# you want to be the key, and the position of the value of that key within the sublist, and uses those
# variables to make a dictionary out of the list of lists. For our purposes placek = position of taxID and
# placev = position of the file name.
# returns a dictionary


def make_list_of_lists_into_dictionary(list_of_lists, placek, placev):
    dict = {}
    for i in list_of_lists:
        if not i[placek] in dict.keys():  # make new key
            dict[i[placek]] = [i[placev]]
        else:
            dict[i[placek]] += [i[placev]]
    return dict

# This function takes in three dictionaries and pairs the values in the first two by their keys. So for our purposes
# this function will match the filenames of references from two seperate databases by the species taxid
# It creates list of lists (matched) where each element of the parent list is pair of lists
# (one for each database)
# If a taxid found in both of the first two directories AND in the third is not included.
# The element of each of the sub-lists is one filename holding from that database (held as a string)
# (or directory name, depending on how the references are organized in each database)
# It takes in the paths to the references for each of the two databases (path1, path2) and writes a
# text file (with the name given by filename_output) that holds the unix script that will copy the files
# from where they are stored within the server (locations given by path1 and path2) to move to the
# directory where the code is run and gives the files new names (count_datab_name.fasta.gz)


def get_matches_and_write_copy_over_script_first_is_directory(dict1, dict2, dict3, path1, path2, filename_output, datab_name1, datab_name2):
    # make the matches
    matched = []
    for i in dict1.keys():
        if i in dict2.keys() and not i in dict3.keys():
            matched += [[dict1[i], dict2[i]]]
    # write the Unix code to move them
    u = open(filename_output, "w")
    for i in matched:
        u.write("mkdir " + i[0][0] + "\n")
        u.write("cd " + i[0][0] + "\n")
        count = 0
        for j in i[0]:
            # copy database1 files over to new postion
            u.write("cp " + path1 + j + "/* " + str(count) + "_" + datab_name1 + ".fasta.gz\n")
            count += 1
        count = 0
        for k in i[1]:
            # copy database2 files over to new position
            u.write("cp " + path2 + k + " " + str(count) + "_" + datab_name2 + ".fasta.gz\n")
            count += 1
        u.write("cd .. \n\n")
    u.close()
    return

# The same function as above EXCEPT that the first entry (dict1, path1) will lead to a file NOT a directory


def get_matches_and_write_copy_over_script(dict1, dict2, dict3, path1, path2, filename_output, datab_name1, datab_name2):
    # make the matches
    matched = []
    for i in dict1.keys():
        if i in dict2.keys() and not i in dict3.keys():
            matched += [[dict1[i], dict2[i]]]
    # write the Unix code to move them
    u = open(filename_output, "w")
    for i in matched:
        u.write("mkdir " + i[0][0] + "\n")
        u.write("cd " + i[0][0] + "\n")
        count = 0
        for j in i[0]:
            # copy database1 files over to new postion
            u.write("cp " + path1 + j + " " + str(count) + "_" + datab_name1 + ".fasta.gz\n")
            count += 1
        count = 0
        for j in i[1]:
            # copy database2 files over to new position
            u.write("cp " + path2 + j + " " + str(count) + "_" + datab_name2 + ".fasta.gz\n")
            count += 1
        u.write("cd .. \n\n")
    u.close()
    return

# This code finds the species that are shared across all three databases and writes the code that will
# create a directory for each species found and copy the references into them.
# NOTE: it is assumed that the third database path leads to a specific directory, not a file. Also,
# the directory is assumed to only have one single file in it which will be copied. If this is not the case
# the resulting code is going to throw an error.


def get_in_all_matches_and_write_copy_over_script(dict1, dict2, dict3, path1, path2, path3, filename_output, datab_name1, datab_name2, datab_name3):
    # make the matches
    matched = []
    for i in dict1.keys():
        if i in dict2.keys() and i in dict3.keys():
            matched += [[dict1[i], dict2[i], dict3[i]]]
    # write the Unix code to move them
    u = open(filename_output, "w")
    for i in matched:
        u.write("mkdir " + i[2][0] + "\n")
        u.write("cd " + i[2][0] + "\n")
        count = 0
        for j in i[0]:
            # copy database1 files over to new postion
            u.write("cp " + path1 + j + " " + str(count) + "_" + datab_name1 + ".fasta.gz\n")
            count += 1
        count = 0
        for j in i[1]:
            # copy database2 files over to new position
            u.write("cp " + path2 + j + " " + str(count) + "_" + datab_name2 + ".fasta.gz\n")
            count += 1
        count = 0
        for j in i[2]:
            # copy database3 files over to new position
            u.write("cp " + path3 + j + "/* " + str(count) + "_" + datab_name3 + ".fasta.gz\n")
            count += 1
        u.write("cd .. \n\n")
    u.close()
    return

# MAIN FUNCTION ----------------------------------------------------------------------------------------------------------------------

# Set up the variables
# The names of the text files that hold the csv styled lists matching taxID's to filenames.
onek_filename = "1k_taxid_filenames.txt" # This one is a list of directories, so must be treated differently
ensembl_filename = "ensembl_taxID_filename.txt"
ncbi_filename = "NCBI_taxID_list.txt"

# The paths to the reference files of each database
onek_path = "~/scratch/1000G/single_files/" # leads to the list of directories
ensembl_path = "~/scratch/ensemble/references/single_files/"
ncbi_path = "~/scratch/NCBI/rop/rop/db_human/fungi/NCBInew/"

# The name of the text files to be created
onek_ncbi_matched_script_filename = "1k_ncbi_create_place_to_compare_script.txt"
ensmebl_ncbi_matched_script_filename = "ensembl_ncbi_create_place_to_compare_script.txt"
onek_ensembl_matched_script_filename = "1k_ensembl_create_place_to_compare_script.txt"
in_all_matched_script_filename = "in_all_create_place_to_compare_script.txt"



# Use the functions
# make the csv files into list of lists
onek_csv = make_list_and_parse_lines_from_document(onek_filename, "\t")
ncbi_csv = make_list_and_parse_lines_from_document(ncbi_filename, "\t")
ensembl_csv = make_list_and_parse_lines_from_document(ensembl_filename, "\t")

# turn the csv lists into dictionaries for easier taxID matching
# reminder: placek = position of taxid and placev = position of filename
onek_dict = make_list_of_lists_into_dictionary(onek_csv, 0, 1)
ncbi_dict = make_list_of_lists_into_dictionary(ncbi_csv, 2, 0)
ensembl_dict = make_list_of_lists_into_dictionary(ensembl_csv, 0, 1)

# now make the UNIX script...
# ...for 1k and ncbi matches ONLY
get_matches_and_write_copy_over_script_first_is_directory(onek_dict, ncbi_dict, ensembl_dict, onek_path, ncbi_path, onek_ncbi_matched_script_filename,"1k", "ncbi")

# ...for ensembl and ncbi matches ONLY
get_matches_and_write_copy_over_script(ensembl_dict, ncbi_dict, onek_dict, ensembl_path, ncbi_path, ensmebl_ncbi_matched_script_filename, "ensembl", "ncbi")

# ...for 1k and ensmebl matches ONLY
get_matches_and_write_copy_over_script_first_is_directory(onek_dict, ensembl_dict, ncbi_dict, onek_path, ensembl_path, onek_ensembl_matched_script_filename, "1k", "ensembl")

# ...for matches across all three databases
get_in_all_matches_and_write_copy_over_script(ensembl_dict, ncbi_dict, onek_dict, ensembl_path, ncbi_path, onek_path, in_all_matched_script_filename, "ensembl", "ncbi", "1k")

print("DONE")