# BOILER PLATE -----------------------------------------------------------------------------------------------------------------------
import string
import shutil

# FUNCTIONS --------------------------------------------------------------------------------------------------------------------------

# This function takes the csv file from WEBSITE and makes a list of lists. Every element of the list is one row of the
# csv file. The sub-list has two elements, the first is the taxID and the second is the file name for that taxID.
# NOTE: the file name is constructed from parts of the row. Most of the time, this creates the actual file name found
# in the database. But there are a couple instances where the suggested filename is not correct. These errors must be
# corrected by going through the files by hand and finding the actual file names manually.


def remake_ensmebl_taxid_table(filename):
    # Start by pulling the lines from the file
    h = open(filename)
    work_space = []
    for l in h:
        line = l.strip().split("\t")
        # Want taxID and then construct the file name from other parts of the line
        if not [line[3], str(string.capwords(line[1], " ") + "." + line[4].replace(" ", "_") + ".dna.toplevel.fa.gz")] in work_space and not line[0][0] == "#":
            work_space += [[line[3], str(string.capwords(line[1], " ") + "." + line[4].replace(" ", "_") + ".dna.toplevel.fa.gz")]]
    h.close()
    # fix some of the smaller text issue with the file name
    for i in work_space:
        i[1].replace(" ", "_")
    return work_space



# create a csv file from a list of lists. This particular function creates a text file called
# "ensembl_taxID_filename.txt". This file will be copied to the parent folder "Fungus"


def create_csv(list):
    f = open("ensembl_taxID_filename.txt", "w")
    for i in list:
        f.write("\t".join(i) + "\n")
    f.close()

# MAIN FUNCTION ------------------------------------------------------------------------------------------------------------------------

# The variables, specifically the file name for the ensembl csv file from WEBSITE
filename = "ensembl_db.txt"

# Get a list of lists with the taxID (in position 0) and the most probable filename (in position 1)
new_table = remake_ensmebl_taxid_table(filename)

# put the new table into a text file called "ensembl_taxID_filename.txt"
create_csv(new_table)

# Save the text file we just created to the parent folder of the current folder.
shutil.copy("ensembl_taxID_filename.txt", "..")

print("DONE")
