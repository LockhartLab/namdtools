from io import TextIOBase

import pandas as pd


# Read NAMD log file
def read_log(log_file):
    r"""
    Read NAMD log file.

    Parameters
    ----------
    fname : :obj:`str` or :obj:`TextIOBase`
        Path or file-like object for the NAMD log file.

    Returns
    -------
    DataFrame
    """

    # Initialize log info
    columns = None
    records = []

    # Read log from either a file-like object or a file path
    if isinstance(log_file, TextIOBase):
        buf = log_file
    else:
        buf = open(log_file, "r", encoding="utf-8")

    # Read through log file and extract energy records
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
        if len(records[0]) != 20:
            raise IOError("expecting 20 data elements in NAMD log file")
        columns = [
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
            "pressure",
            "gpressure",
            "volume",
            "pressavg",
            "gpressavg",
        ]

    # Return
    return pd.DataFrame(records, columns=columns).set_index(columns[0]).astype(float)
