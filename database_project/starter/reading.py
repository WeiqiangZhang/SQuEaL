# Functions for reading tables and databases

import glob
from database import *

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.

# A database is a dict of {str:table},
# where the keys are table names and values are the tables.

# YOU DON'T NEED TO KEEP THE FOLLOWING CODE IN YOUR OWN SUBMISSION
# IT IS JUST HERE TO DEMONSTRATE HOW THE glob CLASS WORKS. IN FACT
# YOU SHOULD DELETE THE PRINT STATEMENT BEFORE SUBMITTING

# print(file_list)


# Write the read_table and read_database functions below
def read_table(csv):
    '''(str) -> Table
    REQ: A valid file name that can be found
    REQ: The file has to have at least one header

    >>>read_table('books.csv').get_dict()
    {'book.year': ['1979', '2014', '2015', '2014'], 'book.title':
    ['Godel Escher Bach', 'What if?', 'Thing Explainer', 'Alan Turing:
    The Enigma'], 'book.author': ['Douglas Hofstadter',
    'Randall Munroe', 'Randall Munroe', 'Andrew Hodges']}
    '''
    # Create a Table object
    return_value = Table()
    # Open the file
    my_file = open(csv, 'r')
    # read every line of the file
    file_list = my_file.readlines()
    # Create a holder list
    new_list = []
    j = 0
    title_num = 0
    # Go through every line of the file
    for next_line in file_list:
        # Check if the line is empty or not
        if (next_line.strip() != ''):
            # Make each string seperated by , an element
            next_line = next_line.split(',')
            # Get rid of any spaces in the elements
            for i in range(len(next_line)):
                next_line[i] = next_line[i].strip()
            # Append the list to the holder list
            new_list.append(next_line)
    for title in new_list[title_num]:
        # Call set_header using the headers
        return_value.set_header(title)
    # Go through every header
    for title in new_list[title_num]:
        # Go through every rows
        for i in range(1, len(new_list)):
            # Call set_table to make a Table object using the header and
            # rows of that header
            return_value.add_elements(title, new_list[i][j])
        j += 1
    # Close the file
    my_file.close()
    # Return the Table object
    return return_value


def read_database():
    '''() -> Database
    Read all the files and make the file name the key and Table object of that
    file the value
    REQ: The files has to have at least one header each

    >>>read_database().get_dict()
    {'imdb': <database.Table object at 0x02860E50>,
    'oscar-film': <database.Table object at 0x0295E3F0>,
    'oscar-actor': <database.Table object at 0x0295EF10>,
    'boxoffice': <database.Table object at 0x02930290>,
    'seinfeld-foods': <database.Table object at 0x02A24750>,
    'olympics-locations': <database.Table object at 0x0295E450>,
    'books': <database.Table object at 0x029302B0>,
    'seinfeld-episodes': <database.Table object at 0x02A1B8B0>,
    'olympics-results': <database.Table object at 0x0295E430>}

    '''
    # Make a Database object
    return_value = Database()
    # Read every file
    file_list = glob.glob('*.csv')
    for file in file_list:
        # Add each Table in the Database
        return_value.add_tables(file.replace('.csv', ''), read_table(file))
    # Return the Database
    return return_value
