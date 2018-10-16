# BOILER PLATE --------------------------------------------------------------------------------------------------------------------------


# FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------

# This function takes a file, and a string and returns a list, where every element is a row from the file. The purpose
# of this function within this code is to take in a text file where every line in the name of a genus found in one
# of the databases being analyzed.
# NOTE: The list of genera names needs to be prepared before hand.


def make_list_from_document(filename):
    f = open(filename)
    lists = []
    for l in f:
        line = l.strip()
        lists += [line]
    f.close()
    return lists

# This function takes two lists. compares the objects in the lists, and returns a list of elements that the two
# lists have in common.


def Shared(comp, other):
    shared = [] #in 1000G and other
    for i in comp:
        if i in other:
            shared += [i]
    return shared

# This function takes two lists and returns a list of elements found in the first list, but not the second one


def leftOvers(comp, other):
    left_over = []
    for i in comp:
        if not i in other:
            left_over += [i]
    return left_over

# This function takes in seven lists and creates a text file called "Venn_Diagram_Genera_lists_Fungus.txt" which
# lists all the genera in each of the parts of the venn diagram for genera overlap across the three databases. It
# also creates a second text file "Venn_Diagram_Genera_numbers_Fungus.txt" that has the count of genera in the
# parts of the venn diagram.
# Also takes in three strings, the three names of the databases.


def out_put_files(only1, only2, only3, one_and_two, one_and_three, two_and_three, in_all, name1, name2, name3):
    f = open("Venn_Diagram_Genera_lists_Fungus.txt", "w")
    u = open("Venn_Diagram_Genera_numbers_Fungus.txt", "w")
# Start with the genera that are only found in one database
    f.write("--IN ONE DATABASE\n\n")

    f.write("-" + name1 + " GENERA:\n")
    for i in only1:
        f.write(i + "\n")
    u.write(name1 + " only: " + str(len(only1)) + "\n\n")

    f.write("\n-" + name2 + " GENERA:\n")
    for j in only2:
        f.write(j + "\n")
    u.write(name2 + " only: " + str(len(only2)) + "\n\n")

    f.write("\n-" + name3 + " GENERA:\n")
    for k in only3:
        f.write(k + "\n")
    u.write(name3 + " only: " + str(len(only3)) + "\n\n")

# Next, list the genera that are only found in two databases
    f.write("\n--IN TWO DATABASES\n")

    f.write("\n-" + name1 + " AND " + name3 + ":\n")
    for m in one_and_three:
        f.write(m + "\n")
    u.write(name1 + " and " + name3 + ": " + str(len(one_and_three)) + "\n\n")

    f.write("\n-" + name1 + " AND " + name2 + ":\n")
    for i in one_and_two:
        f.write(i + "\n")
    u.write(name1 + " and " + name2 + ": " + str(len(one_and_two)) + "\n\n")

    f.write("\n-" + name2 + " AND " + name3 + ":\n")
    for j in two_and_three:
        f.write(j + "\n")
    u.write(name2 + " and " + name3 + ": " + str(len(two_and_three)) + "\n\n")

# Finally, print the genera that are present in all three genera
    f.write("\n--IN ALL THREE DATABASES\n")
    for m in in_all:
        f.write(m + "\n")
    u.write("In all databases: " + str(len(in_all)) + "\n\n")

    f.close()
    u.close()
    return

# MAIN FUNCTION ------------------------------------------------------------------------------------------------------------------------

# Set up variables
onek_genera_list_filename = "1000G_Genera.txt"
ncbi_genera_list_filename = "NCBI_genera.txt"
ensembl_genera_list_filename = "Ensemble_genera.txt"

# Use functions:
# convert the text files to lists:
onek_genera = make_list_from_document(onek_genera_list_filename)
ncbi_genera_list = make_list_from_document(ncbi_genera_list_filename)
ensembl_genera_list = make_list_from_document(ensembl_genera_list_filename)

# create the seven lists that will compose the seven different parts of the venn diagram
# Venn diagram of enesmbl and 1000G:
onek_ensembl = Shared(onek_genera, ensembl_genera_list) # overlap
e_only = leftOvers(ensembl_genera_list, onek_ensembl) # ensembl only (from this set)
onek_only = leftOvers(onek_genera, onek_ensembl) # 1000G only (from this set)

# Venn diagram of NCBI and the other two
onek_ncbi = Shared(onek_only, ncbi_genera_list) # overlap with 1000G and NCBI
ncbi_only = leftOvers(ncbi_genera_list, onek_ncbi) # The ncbi that does not overlap with 1000G
onek_only = leftOvers(onek_only, onek_ncbi) # FINAL 1000G only

ensembl_ncbi = Shared(e_only, ncbi_only) # overlap with ensembl and NCBI
ncbi_only = leftOvers(ncbi_only, ensembl_ncbi) # NCBI only
e_only = leftOvers(e_only, ensembl_ncbi) # FINAL ensembl only

in_all = Shared(ncbi_only, onek_ensembl) # in all the databases
ncbi_only = leftOvers(ncbi_only, in_all) # FINAL NCBI only
onek_ensembl = leftOvers(onek_ensembl, in_all) # FINAL in only 1000G and ensembl

# Now we have all seven elements we need to make the Venn Diagram
# onek_only, e_only, ncbi_only, ensembl_ncbi, onek_ncbi, onek_ensembl, in_all

out_put_files(onek_only, ncbi_only, e_only, onek_ncbi, onek_ensembl, ensembl_ncbi, in_all, "1000G", "NCBI", "ENSEMBL")

print("DONE")