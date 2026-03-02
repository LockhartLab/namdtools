import pandas as pd


# Read NAMD log file
def read_log(fname):
    r"""
    Read NAMD log file.

    Parameters
    ----------
    fname : :obj:`str`
        Name of NAMD log file.

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

    # What if our file doesn't contain ETITLE?
    # We can assume column headers based on what we know from NAMD
    if columns is None:
        n = len(records[0])
        base_columns = [
            "ts",
            "bond",
            "angle",
            "dihed",
            "imprp",
            "elect",
            "vdw",
            "boundary",
            "misc",
            "kinetic",
            "total",
            "temp",
            "potential",
            "total3",
            "tempavg",
        ]
        if n == 15:
            columns = base_columns
        elif n == 20:
            columns = base_columns + ["pressure", "gpressure", "volume", "pressavg", "gpressavg"]
        else:
            raise IOError(f"expecting 15 or 20 data elements in NAMD log file, got {n}")

    # Return
    return pd.DataFrame(records, columns=columns).set_index(columns[0]).astype(float)
