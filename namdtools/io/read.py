"""
read.py

language: Python3
author: C. Lockhart <chris@lockhartlab.org>
"""


class Log:
    def __init__(self):
        pass


# Read output from NAMD run
# Convert to object? Store raw output?
# TODO allow glob read
def read_log(fname):
    """
    Read output from NAMD.

    Parameters
    ----------
    fname : str
        Name of NAMD output file.

    Returns
    -------
    pandas.DataFrame
        Data from NAMD output.
    """

    # Import pandas if not already loaded
    import pandas as pd

    # Initialize DataFrame information
    columns = None
    records = []

    # Read through log file and extract energy records
    with open(fname, 'r') as stream:
        for line in stream.readlines():
            # Read first ETITLE
            if columns is None and line[:6] == 'ETITLE':
                columns = line.lower().split()[1:]

            # Save each energy record
            if line[:6] == 'ENERGY':
                records.append(line.split()[1:])

    # Return DataFrame
    return pd.DataFrame(records, columns=columns).set_index(columns[0])
