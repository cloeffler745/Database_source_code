# BOILER PLATE ---------------------------------------------------------------------------------------------------------------
import string

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
# variables to make a dictionary out of the list of lists.
# returns a dictionary


def make_list_of_lists_into_dictionary(list_of_lists, placek, placev):
    dict = {}
    for i in list_of_lists:
        if not i[placek] in dict.keys():  # make new key
            dict[i[placek]] = [i[placev]]
        else:
            dict[i[placek]] += [i[placev]]
    return dict

# This function takes in two dictionaries and pairs the values in each by their keys. So for our purposes
# this function will match the filenames of references from two seperate databases by the species taxid
# It creates list of lists (matched) where each element of the parent list is pair of lists
# (one for each database)
# The element of each of the sub-lists is one filename holding from that database (held as a string)
# (or directory name, depending on how the references are organized in each database)
# It takes in the paths to the references for each of the two databases (path1, path2) and writes a
# text file (with the name given by filename_output) that holds the unix script that will copy the files
# from where they are stored within the server (locations given by path1 and path2) to move to the
# directory where the code is run and gives the files new names (count_datab_name.fasta.gz)


def get_matches_and_write_copy_over_script_first_is_directory(dict1, dict2, path1, path2, filename_output, datab_name1, datab_name2):
    # make the matches
    matched = []
    for i in dict1.keys():
        matched += [dict1[i], dict2[i]]
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
        for j in i[1]:
            # copy database2 files over to new position
            u.write("cp " + path2 + j + " " + str(count) + "_" + datab_name2 + ".fasta.gz\n")
            count += 1
        u.write("cd .. \n\n")
    u.close()
    return

# The same function as above EXCEPT that the first entry (dict1, path1) will lead to a file NOT a directory


def get_matches_and_write_copy_over_script(dict1, dict2, path1, path2, filename_output, datab_name1, datab_name2):
    # make the matches
    matched = []
    for i in dict1.keys():
        matched += [dict1[i], dict2[i]]
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

# MAIN FUNCTION ----------------------------------------------------------------------------------------------------------------------

# The names of the text files that hold the csv styled lists matching taxID's to filenames.
onek_filename = "1k_taxid_filename.txt" # This one is a list of directories, so must be treated differently
ensembl_filename = ""
ncbi_filename = "NCBI_taxID_list.txt"

# The paths to the reference files of each database
onek_path = "~/scratch/1000G/single_files/"
ensembl_path = "~/scratch/ensemble/references/single_files/"
ncbi_path = "~/scratch/NCBI/rop/rop/db_human/fungi/NCBInew/"

# The name of the text files to be created
onek_ncbi_matched_filename = ""
ensmebl_ncbi_matched_filename = ""


# make the csv files into list of lists
onek_csv = make_list_and_parse_lines_from_document(onek_filename, "\t")
ncbi_csv = make_list_and_parse_lines_from_document(ncbi_filename, "\t")
ensembl_csv = make_list_and_parse_lines_from_document(ensembl_filename, "")

# turn the csv lists into dictionaries for easier taxID matching
onek_dict = make_list_of_lists_into_dictionary(onek_csv, 0, 0)
ncbi_dict = make_list_of_lists_into_dictionary(ncbi_csv, 0, 0)
ensembl_dict = make_list_of_lists_into_dictionary(ensembl_csv, 0, 0)

# now make the UNIX script
# for 1k and ncbi matches
get_matches_and_write_copy_over_script_first_is_directory(onek_dict, ncbi_dict, onek_path, ncbi_path, "1k_ncbi_create_place_to_compare_script.txt","1k", "ncbi")

# for ensembl and ncbi matches
get_matches_and_write_copy_over_script(ensembl_dict, ncbi_dict, ensembl_path, ncbi_path, "ensembl_ncbi_create_place_to_compare_script.txt", "ensembl", "ncbi")

print("DONE")