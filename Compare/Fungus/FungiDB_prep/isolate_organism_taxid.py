# BOILER PLATE ----------------------------------------------------------------------------------------------


# FUNCTIONS ------------------------------------------------------------------------------------------------

# Takes a string input and selects the part of the string before a given part of the string. Returns the reduced
# string
def select_string_segment(string, want_part_before):
    segments = string.split(want_part_before)
    if not segments[0] == "":
        return segments[0]
    else:
        return "NO_TAXID"


# Takes every line in a file, seperates each part of the line by PARSE_BY, and makes that list an element of a list_of_lists
# This also takes the second element in the list and takes only the part of the string before "("
# returns a list of lists with only the zeroth and second element
def make_list_and_parse_lines_from_document(filename, parse_by):
    f = open(filename)
    list_of_lists = []
    for l in f:
        line = l.strip().split(parse_by)
        line = [line[0], select_string_segment(line[2], "(")]
        list_of_lists += [line]
    f.close()
    return list_of_lists

#   Takes every element of a list of lists of strings, takes the sub list and combines all the elements with "combine_with"
#   and writes all lines to a text file
def list_of_lists_to_file(list_o_l, filename, combine_with):
    f = open(filename, "w")
    for i in list_o_l:
        line = combine_with.join(i) + "\n"
        f.write(line)
    f.close()

# MAIN FUNCTION ---------------------------------------------------------------------------------------------

# Variables

in_filename = "Fungidb_taxid_actual.txt"
out_filename = "Fungidb_taxid_isolated_leave_blanks.txt"

# Use functions:

isolated = make_list_and_parse_lines_from_document(in_filename, "\t")
list_of_lists_to_file(isolated, out_filename, "\t")

print("DONE")