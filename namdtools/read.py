import pandas as pd


# Read output from NAMD run
def read_log(fname):
    r"""
    Read output from NAMD.

    Parameters
    ----------
    fname : str
        Name of NAMD output file.

    Returns
    -------
    DataFrame
    """

    # Initialize log info
    columns = None
    records = []

    # Read through log file and extract energy records
    with open(fname, "r") as buf:
        for line in buf:
            # Read first ETITLE
            if columns is None and line.startswith("ETITLE"):
                columns = line.lower().split()[1:]

            # Save each energy record
            if line.startswith("ENERGY"):
                records.append(line.split()[1:])

    # Return
    return pd.DataFrame(records, columns=columns).set_index(columns[0]).astype(float)

