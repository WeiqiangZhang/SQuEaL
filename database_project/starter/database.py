class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self):
        # Initialize the Table object
        self._table = {}

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        self._table = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self._table

    def set_header(self, title):
        '''(Table, str) -> NoneType
        Create the key for each header for the dictionary representation
        of this table.
        '''
        self._table[title] = []

    def add_elements(self, title, rows):
        '''(Table, str, list element) -> NoneType
        Add the rows of each header/elements of each key to the dictionary
        representation of this table.
        '''
        # Create a dictionary with headers as keys and rows as elements
        self._table[title].append(rows)

    def key_list(self):
        '''(Table) -> list of str
        Return a list of keys the dictionary representation of this table
        has.
        REQ: Must be a valid dictionary table object, containing at
        least one header.
        '''
        # Method to get a list of keys in a dictionary
        return list(self._table.keys())

    def select_condition(self, select_query):
        '''(Table, list of str) -> NoneType
        Using the select query remove all the columns of the dictionary
        representation that is not in the select query list.
        REQ: Must be a valid dictionary table object, containing at
        least one header.
        REQ: Elements in select_query must be contained in the dictionary
        table object as a key.
        '''
        # pop holder list
        pop_list = []
        # Go through the keys in the Table object
        for key in self._table:
            # If that key is not in select query list
            if(key not in select_query):
                # Add that key to pop list
                pop_list.append(key)
        # Go through every element in pop list
        for i in range(len(pop_list)):
            # Get rid of all the keys in that table that is not in the select
            # query list
            self._table.pop(pop_list[i], None)

    def cartesian_table1(self, t1_rows, t2_rows):
        '''(Table, int, int) -> dict of {str: list of str}
        Take the dictionary representation of the table and multiply the number
        of rows depending on the number of rows the other table contain.
        REQ: Must be a valid dictionary table object, containing at
        least one header.
        REQ: t1_rows must be the same length as the length of the dictionary
        table.
        '''
        # Go through every key in the Table object
        for key in self._table:
            # Go through every element in that key
            for i in range(t1_rows):
                # Add current element to the end table two row number of times
                self._table[key] += [(self._table[key])[i]] * t2_rows
            for i in range(t1_rows):
                # Remove all the original elements
                self._table[key].pop(0)
        # Return the new table
        return self._table

    def cartesian_table2(self, t1_rows):
        '''(Table, int) -> dict of {str: list of str}
        Take the dictionary representation of the table and multiply the number
        of rows depending on the number of rows the other table contain.
        REQ: Must be a valid dictionary table object, containing at
        least one header.
        '''
        # Go through every column in the table
        for key in self._table:
            # Multiply that column by the number of rows table two has
            self._table[key] = self._table[key] * t1_rows
        return self._table

    def cartesian_products(self, table1, table2):
        '''(Table, dict of {str: list of str},
        dict of {str: list of str}) -> Table
        Add the two dictionaries into the table object.
        REQ: table1 and table2 must be valid dictionaries with
        at least one header each
        '''
        # Add the two changed tables to make a new Table object
        self._table.update(table2)
        self._table.update(table1)

    def num_rows(self, key):
        '''(Table, str) -> int
        Get the length of the key of the dictionary representation of the table
        object.
        REQ: Must be a valid dictionary table object, containing at
        least one header.
        REQ: The key must be within the dictionary table
        '''
        # Get the number of rows a Table has
        return len(self._table[key])

    def which_types(self, compare):
        '''(Table, list of str) -> str
        Check if the the where condition is comparing another column or a
        value.
        REQ: Must be a valid dictionary table object, containing at
        least one header.
        REQ: compare list must have two elements
        compare
        '''
        second_element = 1
        # Check if the second value is a header in the table or just a value
        if(compare[second_element] in self._table):
            return "key"
        else:
            return "value"

    def key_equals(self, compare):
        '''(Table, list of str) -> NoneType
        Check which column value does not equal to the other column value and
        remove it.
        REQ: Must be a valid dictionary table object, containing at
        least two headers.
        REQ: compare list have two elements
        '''
        key1 = 0
        key2 = 1
        # pop holder list
        pop_list = []
        # Go through every row of the Table
        for i in range(len(self._table[compare[key1]])):
            # If the first column's row isn't equal to the second column's row
            if ((self._table[compare[key1]])[i] != (
                                            self._table[compare[key2]])[i]):
                # Append that row number to the holder list
                pop_list.append(i)
        # Call pop_it to pop out the unwanted rows
        self.pop_it(pop_list)

    def value_equals(self, compare):
        '''(Table, list of str) -> NoneType
        Check which column value does not equal to the given value and
        remove it.
        REQ: Must be a valid dictionary table object, containing at
        least one header.
        REQ: compare list have two elements 
        '''
        key = 0
        value = 1
        # pop holder list
        pop_list = []
        # Go through every row of the Table
        for i in range(len(self._table[compare[key]])):
            # If the row value is not equal to the given value
            if((self._table[compare[key]])[i] != compare[value]):
                # Append that row number to the holder list
                pop_list.append(i)
        # Call pop_it to pop out the unwanted rows
        self.pop_it(pop_list)

    def key_greater(self, compare):
        '''(Table, list of str) -> NoneType
        Check which column value is not greater than the other column value and
        remove it.
        REQ: Must be a valid dictionary table object, containing at
        least two headers.
        REQ: compare list have two elements
        '''
        key1 = 0
        key2 = 1
        # Pop holder list
        pop_list = []
        # Go through every row of the Table
        for i in range(len(self._table[compare[key1]])):
            # Check if the row value of the first given column is smaller
            # or equal to the row value of the second given column
            if ((self._table[compare[key1]])[i] <= (
                                            self._table[compare[key2]])[i]):
                # If so append the row number to the holder list
                pop_list.append(i)
        # Call pop_it to pop out the unwanted rows
        self.pop_it(pop_list)

    def value_greater(self, compare):
        '''(Table, list of str) -> NoneType
        Check which column value is not greater than the given value and
        remove it.
        REQ: Must be a valid dictionary table object, containing at
        least one header.
        REQ: compare list have two elements
        '''
        key = 0
        value = 1
        # Pop holder list
        pop_list = []
        # Go through every row of the Table
        for i in range(len(self._table[compare[key]])):
            # Check if the row value of the first given column is smaller
            # or equal to the given value
            if((self._table[compare[key]])[i] <= compare[value]):
                # If so append the row number to the holder list
                pop_list.append(i)
        # Call pop_it to pop out the unwanted rows
        self.pop_it(pop_list)

    def pop_it(self, pop_list):
        '''(Table, list of int) -> NoneType
        Using the list of integers representing the index at which to
        remove the key from the dictionary, to remove the key from
        the dictionary representation of the table.
        REQ: Must be a valid dictionary table object, containing at
        least one header.
        REQ: pop list elements must be in range with the number of rows
        '''
        # Go through every column in the Table
        for key in self._table:
            # From the last row to the first
            for i in range(len(pop_list) - 1, -1, -1):
                # Pop out the unwanted rows
                self._table[key].pop(pop_list[i])


class Database():
    '''A class to represent a SQuEaL database'''
    def __init__(self):
        self._database = {}

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self._database = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._database

    def add_tables(self, table_name, table_info):
        '''(Database, str, Table) -> NoneType
        Add the key, which is name of the table, and the value, which is the
        dictionary representation of the Table object, to the dictionary
        representation of the Database object.
        '''
        # Add the Table object value to the table name key
        self._database[table_name] = table_info

    def get_table(self, key):
        '''(Database, str) -> Table
        Return the Table object in the database using the name of the table.
        REQ: Key must be in the database
        '''
        # Return the Table object according to the table key
        return self._database[key]
