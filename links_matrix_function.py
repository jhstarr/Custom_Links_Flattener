# Jeff Starr, 26 September, 2017

# This is a function that takes the links matrix provided to 01Click
# by Customer and returns a flattened matrix that can be processed 
# written to a file then imported into the Conversations app.

#------------Imports, initialization, and read the input_matrix----------

from operator import itemgetter
import csv

def process_links_matrix(links_input_filename,history_input_filename):
    """Take links matrix and return output and history matrices."""

# initialize several lists
    input_matrix = []
    in_hotplay_ids = []
    in_hotplay_names = []
    to_hotplay_ids = []
    to_hotplay_names= []
    pre_output_matrix = []
    output_matrix = []
    history_matrix = []
    row_extract = []
    history_extract = []
    discard_matrix = []

# Create constants that correspond to the field positions in the output
# and history matrices.
    IN_HOTPLAY_ID_COLUMN = 1
    TO_HOTPLAY_NAME_COLUMN = 2
    TO_HOTPLAY_ID_COLUMN = 3
    BUCKET_COLUMN = 4
    SORT_ORDER_COLUMN = 6
    MANUAL_EDIT_FLAG_COLUMN = 10

# Read in the data from a csv into a reader object.  Iterate through that
# reader object and append each row (which is a list) to a list-of-lists
# called input_matrix.

    with open(links_input_filename, encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            input_matrix.append(row)

# ----Clean up the matrix-----

# Put the first row of input_matrix into list in_hotplay_ids.  Pop off the 
# first two items which are leftward column headings.  Finally, remove this
# row from input_matrix now that it is stored within in_hotplay_ids.
    in_hotplay_ids = input_matrix[0]
    in_hotplay_ids.pop(0)
    in_hotplay_ids.pop(0)
    input_matrix.pop(0)

# Repeat for the hotplay names which are in the next row.
    in_hotplay_names = input_matrix[0]
    in_hotplay_names.pop(0)
    in_hotplay_names.pop(0)
    input_matrix.pop(0)

# Grab first two items in row which are the to hotplay id and hotplay name.
# Append them to a list of numbers and names respectively.
# Then, pop them off. After this, input_matrix is stripped of 
# header rows and columns with the convo ids and names.

    for row in input_matrix:
        to_hotplay_ids.append(row[0])
        to_hotplay_names.append(row[1])
        row.pop(0)
        row.pop(0)

# ---------Build the records of pre_output_matrix-----------------

# Walk through the remaining core of the matrix that does not have headers.
# If item is blank, pass over.
# If the item is not blank create the required record.

    r = 0
    c = 0

    for row in input_matrix:
        for cell in row:
            if cell == '':
                pass
            else:
                pre_output_matrix.append([
                    in_hotplay_names[c],
                    int(in_hotplay_ids[c]),
                    to_hotplay_names[r],
                    int(to_hotplay_ids[r]),
                    cell,
                    "Customer Asset",
                    "",
                    to_hotplay_names[r],
                    "https://customer.01click.net/web?hp_id="+
                        str(to_hotplay_ids[r]),
                    "Link to Conversation",
                    ""])
            c +=1
        r+=1
        c = 0


# -------Sort links then add sort order numbers to the records---------

# Sort by in_hotplay, by bucket, then by to_hotplay name.
# Note that "Z" sorts before "a" in python.

    pre_output_matrix =  sorted(
        pre_output_matrix, 
        key=itemgetter(TO_HOTPLAY_NAME_COLUMN))
    
    pre_output_matrix =  sorted(
        pre_output_matrix, 
        key=itemgetter(BUCKET_COLUMN))
    
    pre_output_matrix =  sorted(
        pre_output_matrix, 
        key=itemgetter(IN_HOTPLAY_ID_COLUMN))

# Step through rows and create an increasing sort order for collaterals  
# with the same in_hotplay_id and same bucket.

    previous_in_hotplay_id = ""
    previous_bucket = ""
    sort_order = 0
       
    for row in pre_output_matrix:
        if (
            row[IN_HOTPLAY_ID_COLUMN] == previous_in_hotplay_id 
            and row[BUCKET_COLUMN] == previous_bucket
            ):
            sort_order = sort_order + 10
        else:
            sort_order = 10
        
        row[SORT_ORDER_COLUMN] = sort_order
        previous_in_hotplay_id = row[IN_HOTPLAY_ID_COLUMN]
        previous_bucket = row[BUCKET_COLUMN]
        

# -----------Check new records against history file---------------------------

# Now that pre_output_matrix is sorted, convert all items to a string
# so that you can make comparisons with history file.
# I use list comprehension on earch row of the matrix.

    for row in range(len(pre_output_matrix)):
        pre_output_matrix[row] = [str(cell) for cell in pre_output_matrix[row]]

# Read in the history file

    with open(history_input_filename, encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            history_matrix.append(row)

# Create an extract that only includes the in_hotplay_id, to_hotplay_id, and
# bucket which are the essential elements defining a link.

    for row in history_matrix:
        row_extract = [
            row[IN_HOTPLAY_ID_COLUMN],
            row[TO_HOTPLAY_ID_COLUMN], 
            row[BUCKET_COLUMN]]
        
        history_extract.append(row_extract)

#  In history_matrix, remove the manual edit flags before comparison.

    for row in history_matrix:
        row[MANUAL_EDIT_FLAG_COLUMN] = ""

# Remove all records in pre_output_matrix which are already in history file.
# If a record is in history_matrix, append it to discard_matrix for a 
# future test. (MOD)
# If there is a match in history_extract, then mark for manual edit.  
# (This will often be a change to Sort Order due to insertion of new rows.)

    for row in pre_output_matrix:
        if row in history_matrix:
            discard_matrix.append(row)
        else:
            if (
                [row[IN_HOTPLAY_ID_COLUMN],
                row[TO_HOTPLAY_ID_COLUMN], 
                row[BUCKET_COLUMN]] 
                in 
                history_extract
                ):
                row[MANUAL_EDIT_FLAG_COLUMN] = "edit"
            output_matrix.append(row)
            history_matrix.append(row)

#-------------- Return the output and history matrices-----------------------

# Create headers for the output_matrix.

    output_matrix.insert(0,[
        "in_hotplay_name",
        "in_hotplay_id",
        "to_hotplay_name",
        "to_hotplay_id",
        "collateral_bucket",
        "collateral_asset_type",
        "collateral_sort_order",
        "collateral_name",
        "collateral_url",
        "collateral_description",
        "manual_edit_flag"])

    return output_matrix, history_matrix


