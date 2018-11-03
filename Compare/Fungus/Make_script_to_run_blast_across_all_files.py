# BOILER PLATE ---------------------------------------------------------------------------------------------------------------


# FUNCTIONS ------------------------------------------------------------------------------------------------------------------

# Takes every line in a file and makes it an element of a list
# In this code, it will take in the text file where every line is a name of a directory that holds two sequneces
# that we want to compare (MSA) using blastn
# NOTE: That text file needs to be prepared before hand. This is typically gotten by "ls > file_names.txt"


def make_list_from_document(filename):
    f = open(filename)
    list = []
    for l in f:
        line = l.strip()
        list += [line]
    f.close()
    return list

# This will write the Unix script that will go into each directory and run blastn on the two gzipped fasta files
# that are inside.
# NOTE: query_name and subject_name is just the name of the database, MAKE SURE THAT THESE MATCH UP TO THE NAMES OF
# THE FILES THAT ARE ACTUALLY INSIDE YOUR DIRECTORIES. eg. if your filename is 0_1k.fasta.gz then query_name = 1k


def write_script_that_will_compare(filename_output, query_name, subject_name, list_of_directories):
    code = open(filename_output, "w")
    for i in list_of_directories:
        code.write("cd " + i + "\n")

        code.write("gunzip 0_" + query_name + ".fasta.gz\n")
        code.write("awk '/^>/ {printf(\"\\n%s\\n\",$0);next; } { printf(\"%s\",$0);}  END {printf(\"\\n\");}' 0_" + query_name + ".fasta > " + query_name + "_new.fasta\n")
        code.write("gzip 0_" + query_name + ".fasta\n")

        code.write("gunzip 0_" + subject_name + ".fasta.gz\n")
        code.write("awk '/^>/ {printf(\"\\n%s\\n\",$0);next; } { printf(\"%s\",$0);}  END {printf(\"\\n\");}' 0_" + subject_name + ".fasta > " + subject_name + "_new.fasta\n")
        code.write("gzip 0_" + subject_name + ".fasta\n")

        code.write("~/project/anaconda2/bin/blastn -query " + query_name + "_new.fasta -subject " + subject_name + "_new.fasta  -outfmt \"7 qseqid sseqid pident qlen slen length qstart sstart mismatch\" -max_target_seqs 10 -out blast_results.txt\n")
        code.write("~/project/anaconda2/bin/python ../extract.py blast_results.txt\n")
        code.write("cd ..\n\n")
    code.close()
    return

# MAIN FUNCTION ------------------------------------------------------------------------------------------------------------------

# Set up variable names...
# ...for filenames
onek_e_input_filename = "onek_e_directory_list.txt" # reminder, this text file must be prepared before hand
onek_e_output_filename = "onek_e_compare.sh"

onek_ncbi_input_filename = "onek_ncbi_directory_list.txt" # reminder, this text file must be prepared before hand
onek_ncbi_output_filename = "onek_ncbi_compare.sh"

ncbi_e_input_filename = "ncbi_e_directory_list.txt" # reminder, this text file must be prepared before hand
ncbi_e_output_filename = "ncbi_e_compare.sh"

# ...for database names
onek = "1k"
ensembl = "ensembl"
ncbi = "ncbi"

# Use functions:
# create the lists of directory names
list_of_onek_e_directories = make_list_from_document(onek_e_input_filename)
list_of_onek_ncbi_directories = make_list_from_document(onek_ncbi_input_filename)
list_of_ncbi_e_directories = make_list_from_document(ncbi_e_input_filename)

# write the code to a text file
write_script_that_will_compare(onek_e_output_filename, onek, ensembl, list_of_onek_e_directories)
write_script_that_will_compare(onek_ncbi_output_filename, onek, ncbi, list_of_onek_ncbi_directories)
write_script_that_will_compare(ncbi_e_output_filename, ncbi, ensembl, list_of_ncbi_e_directories)

print("DONE")