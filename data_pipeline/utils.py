import csv
import os
import numpy as np

def add_to_csv(csv_path, output_path, column, func, **kwargs):
    """
    Adds a new column to a CSV file and populates it with values computed by a given function.

    Args:
        csv_path (str): The path to the input CSV file.
        output_path (str): The path to the output CSV file.
        column (str): The name of the new column to be added.
        func (callable): The function used to compute the values for the new column.
        **kwargs: Additional keyword arguments to be passed to the function.

    Returns:
        None
    """
    with open(os.path.join(csv_path),'r') as csvinput:
        with open(os.path.join(output_path), 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n', delimiter=';')
            reader = csv.reader(csvinput, delimiter=';')

            all = []
            row = next(reader)
            row.append(column)
            all.append(row)

            for row in reader:
                row.append(func(row, **kwargs))
                all.append(row)

            writer.writerows(all)

def get_column_index(csv_path, column):
    """
    Return the index of a column in a CSV file.

    Args:
        csv_path (str): The path to the CSV file.
        column (str): The name of the column.

    Returns:
        int: The index of the column in the CSV file.
    """
    with open(os.path.join(csv_path),'r') as csvinput:
        reader = csv.reader(csvinput, delimiter=';')
        row = next(reader)
        return row.index(column)
    
def csv_to_array(csv_path):
    """
    Return the array representation of a CSV file.

    Args:
        csv_path (str): The path to the CSV file.

    Returns:
        list: The array representation of the CSV file.
    """
    with open(os.path.join(csv_path),'r') as csvinput:
        arr = [row for row in csv.reader(csvinput, delimiter=';')]
        return np.array(arr).reshape(-1, len(arr[0]))

def get_column_by_name(csv_array, column_name):
    """
    Returns a list of rows from `csv_array` that have a matching `column_name` in the first column.

    Parameters:
    - csv_array: a list of lists representing a CSV file, where each inner list represents a row of the CSV.
    - column_name: a string representing the name of the column to search for.

    Returns:
    - A list of rows from `csv_array` that have a matching `column
    """
    index = csv_array[0].index(column_name)
    return [row for row in csv_array if row[0] == column_name]