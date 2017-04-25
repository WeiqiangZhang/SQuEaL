from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


def get_where(query):
    '''(str) -> list
    return the list of requirements for where condition from query.
    REQ: Proper query syntax

    >>>get_where("select * from movies,oscars where m.year=o.year")
    ['m.year=o.year']
    >>>get_where("select * from movies,oscars where m.year=o.year,m.year>1997")
    ['m.year=o.year', 'm.year>1997']
    '''
    space = " "
    # The index where condition is found
    where_placement = 5
    # Split everything by space
    query = query.split(" ")
    # Combine the strings that have spaces in them
    query = space.join(query[5:])
    # Seperate each where condition into an element in a list
    query = query.split(",")
    # Return the where condition
    return (query)


def get_from(query):
    '''(str) -> list
    return the list of requirements for from condition from query.
    REQ: Proper query syntax

    >>>get_from("select * from movies where m.year=o.year")
    ['movies']
    >>>get_from("select * from movies,oscars where m.year=o.year,m.year>1997")
    ['movies', 'oscars']
    '''
    # Index where from condition is found
    from_placement = 3
    # Split everything by space
    query = query.split(" ")
    # Get the from condition
    query = query[from_placement]
    # Seperate each from condition into an element in a list
    query = query.split(",")
    return query


def get_select(query):
    '''(str) -> list
    return the list of requirements for select condition from query.
    REQ: Proper query syntax

    >>>get_select("select * from movies where m.year=o.year")
    ['*']
    >>>get_select("select o.year,o.title,m.title from movies,oscars")
    ['o.year', 'o.title', 'm.title']
    '''
    select_placement = 1
    # Split using the string from
    query = query.split(" ")
    # Get the select conditions as a string
    query = query[select_placement]
    # Turn the select conditions into a list sperated by ,
    query = query.split(',')
    return query


def run_query(data_base, query):
    ''' (Database, str) -> Table
    Return a Table object that represents the conditions of the query that is
    entered.
    REQ: Database containing one or more Tables
    REQ: Proper query syntax

    >>>run_query(read_database(), 'select * from olympics-locations,
    books where book.year=l.year').get_dict()
    {'book.title': ['What if?', 'Alan Turing: The Enigma'], 'book.author':
    ['Randall Munroe', 'Andrew Hodges'], 'l.year': ['2014', '2014'],
    'l.city': ['Sochi', 'Sochi'], 'l.country': ['Russia', 'Russia'],
    'book.year': ['2014', '2014']}
    >>>run_query(read_database(), 'select l.year,book.year
    from olympics-locations,books where book.year=l.year').get_dict()
    {'l.year': ['2014', '2014'], 'book.year': ['2014', '2014']}
    '''
    # Call get_from to get a list of from conditions
    from_query = get_from(query)
    # Call get_select to get a list of select conditions
    select_query = get_select(query)
    # Get a Table object from from_condition
    save_table = from_condition(data_base, from_query)
    # Check if where condition is found in the query
    if("where" in query):
        # Call get_where to get a list of where conditions
        where_query = get_where(query)
        # Call where_condition to mutate the Table according the the given
        # where conditions
        where_condition(save_table, where_query)
    # Check if select condition is all the columns
    if (select_query != ["*"]):
        # If not, call the select_condition method to remove the none selected
        # columns
        save_table.select_condition(select_query)
    # Return the final completed Table object with all the conditions fulfiled
    return save_table


def from_condition(data_base, from_query):
    '''(Database, list of str) -> Table
    Return a cartesian product of the Table/Tables following the from
    conditions
    REQ: Database containing one or more Tables
    REQ: Proper query syntax
    REQ: From conditions have to be a valid file

    >>>from_condition(read_database(), ['books']).get_dict()
    {'book.year': ['1979', '2014', '2015', '2014'], 'book.author':
    ['Douglas Hofstadter', 'Randall Munroe', 'Randall Munroe',
    'Andrew Hodges'], 'book.title': ['Godel Escher Bach', 'What if?',
    'Thing Explainer', 'Alan Turing: The Enigma']}
    '''
    only_table = 0
    one_table = 1
    # Check if the Database only contains one Table
    if(len(from_query) == one_table):
        # Call get_table method from Database class to get the Table Object
        save_table = data_base.get_table(from_query[only_table])
    else:
        # Go through each Table object in Database object
        for i in range(len(from_query) - 1):
            # Check if it's the first two Tables
            if (i == 0):
                # Call cartesian_product to combine the two Table objects
                save_table = cartesian_product(data_base.get_table(
                    from_query[i]), data_base.get_table(from_query[i + 1]))
            else:
                # If a previous Table has already been combined
                # Combine that Table with the next one
                save_table = cartesian_product(data_base.get_table(
                                                from_query[i + 1]), save_table)
    # Return the final cartesian_product
    return save_table


def cartesian_product(table1, table2):
    '''(Table, Table) -> Table
    Takes in two Table objects and return the cartesian_product of the tables
    REQ: Two valid Table objects

    >>>cartesian_product(read_table('books.csv'), read_table('books.csv')).get_
    dict()
    {'book.author': ['Douglas Hofstadter', 'Douglas Hofstadter',
    'Douglas Hofstadter', 'Douglas Hofstadter', 'Randall Munroe',
    'Randall Munroe', 'Randall Munroe', 'Randall Munroe',
    'Randall Munroe', 'Randall Munroe', 'Randall Munroe',
    'Randall Munroe', 'Andrew Hodges', 'Andrew Hodges', 'Andrew Hodges',
    'Andrew Hodges'], 'book.title': ['Godel Escher Bach',
    'Godel Escher Bach', 'Godel Escher Bach', 'Godel Escher Bach',
    'What if?', 'What if?', 'What if?', 'What if?', 'Thing Explainer',
    'Thing Explainer', 'Thing Explainer', 'Thing Explainer',
    'Alan Turing: The Enigma', 'Alan Turing: The Enigma',
    'Alan Turing: The Enigma', 'Alan Turing: The Enigma'],
    'book.year': ['1979', '1979', '1979', '1979', '2014', '2014',
    '2014', '2014', '2015', '2015', '2015', '2015', '2014', '2014',
    '2014', '2014']}
    '''
    first_key = 0
    # Create a new Table object
    save_table = Table()
    # Get a list of keys from the first Table object using key_list method in
    # Table()
    key1 = table1.key_list()
    # Get a list of keys from the second Table object using key_list method in
    # Table()
    key2 = table2.key_list()
    # Get the number of rows in the first Table using num_rows method in
    # Table()
    t1_rows = table1.num_rows(key1[first_key])
    # Get the number of wos in the second Table using num_rows method in
    # Table()
    t2_rows = table2.num_rows(key2[first_key])
    # Check if first Table has any rows
    # Else, both has one or more rows
    # Change first Table object depending on the number of rows of the
    # second Table
    new_table1 = table1.cartesian_table1(t1_rows, t2_rows)
    # Change second Table object depending on the number of rows of the
    # first Table
    new_table2 = table2.cartesian_table2(t1_rows)
    # Combine the changed Tables in a new Table object
    save_table.cartesian_products(new_table1, new_table2)
    # Return the table
    return save_table


def where_condition(save_table, where_query):
    '''(Table, list of str) -> NoneType
    Apply the where conditions to the cartesian product Table object
    REQ: A valid table object
    REQ: A valid where condition

    >>>save_table = cartesian_product(read_table('books.csv'),
    read_table('olympics-locations'))
    >>>where_condition(save_table, ['l.year>book.year'])
    >>>print(save_table.get_dict())
    {'l.year': ['1980', '1984', '1988', '1992', '1994', '1998',
    '2002', '2006', '2010', '2014'], 'book.author':
    ['Douglas Hofstadter', 'Douglas Hofstadter',
    'Douglas Hofstadter', 'Douglas Hofstadter',
    'Douglas Hofstadter', 'Douglas Hofstadter', 'Douglas Hofstadter',
    'Douglas Hofstadter', 'Douglas Hofstadter',
    'Douglas Hofstadter'], 'book.title': ['Godel Escher Bach',
    'Godel Escher Bach', 'Godel Escher Bach', 'Godel Escher Bach',
    'Godel Escher Bach', 'Godel Escher Bach', 'Godel Escher Bach',
    'Godel Escher Bach', 'Godel Escher Bach',
    'Godel Escher Bach'], 'l.country': ['United States',
    'Yugoslavia (until 1988)', 'Canada', 'France', 'Norway', 'Japan',
    'United States', 'Italy', 'Canada', 'Russia'],
    'book.year': ['1979', '1979', '1979', '1979', '1979', '1979',
    '1979', '1979', '1979', '1979'], 'l.city': ['Lake Placid',
    'Sarajevo', 'Calgary', 'Albertville', 'Lillehammer', 'Nagano',
    'Salt Lake City', 'Torino', 'Vancouver', 'Sochi']}
    '''
    remove_apos = 1
    # Go through all the elements in the where condition list
    for i in range(len(where_query)):
        # Check if it's an equal sign argument
        if('=' in where_query[i]):
            # Assign compare as the two elements being compared
            compare = where_query[i].split('=')
            # Check if the value is a string with apostrophes
            if("'" in compare[remove_apos] or '"' in compare[remove_apos]):
                # Remove the apostrophes
                compare[remove_apos] = compare[remove_apos].replace("'", "")
                compare[remove_apos] = compare[remove_apos].replace('"', "")
            # Call which_types method in Table() class to check if
            # the 2nd element in compare is a header or a value
            which_type = save_table.which_types(compare)
            # If the element is a header
            if(which_type == "key"):
                # Call key_equals method to remove all the rows in columns
                # that aren't equal
                save_table.key_equals(compare)
            else:
                # Call value_equals method to remove all the rows of the
                # columns that aren't equal to the value
                save_table.value_equals(compare)
        else:
            # Assign compare as the two elements being compared
            compare = where_query[i].split('>')
            # Call which_types method in Table() class to check if the
            # 2nd element in compare is a header or a value
            which_type = save_table.which_types(compare)
            # if the element is a header
            if(which_type == "key"):
                # Call key_greater method to remove all the rows of the columns
                # that don't have the first column value greater than the
                # second
                save_table.key_greater(compare)
            else:
                # Call value_greater method to remove all the rows of the
                # columns that don't have the first column value greater than
                # the input value
                save_table.value_greater(compare)


def num_rows(table):
    '''(dict) -> int
    Takes the table dictionary and return the number of rows the table has

    >>>{key1: [1, 2, 3], key2: [4, 5, 6]}
    3
    '''
    key = list(table.keys())[0]
    rows = len(table[key])
    return rows


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = num_rows(table.get_dict())
    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))

if(__name__ == "__main__"):
    query = input("Enter a SQuEaL query, or a blank line to exit:")
    if (query != ""):
        print_csv(run_query(read_database(), query))
    while (query != ""):
        query = input("Enter a SQuEaL query, or a blank line to exit:")
        if (query != ""):
            print_csv(run_query(read_database(), query))
