import fpathlib.ext.polars as pl

# Read NAMD log file
def read_log(source, drop_etitle=True):
    return scan_log(source, drop_etitle).collect()

# Scan NAMD log file
def scan_log(source, drop_etitle=True):
    r"""
    Scan NAMD log file.

    Parameters
    ----------
    source : :obj:`str`
        Name of NAMD log file. 
    drop_etitle : :obj:`bool`
        Drop the first column of the log file, which is the title of the energy term. (Default: True).

    Returns
    -------
    DataFrame
    """

    # Read in logs in `source`
    lf = pl.scan_txt(
        source,
        separator=r"\s+",
        filter_expr=pl.col("line").str.starts_with("ENERGY"),
    )

    lf0 = lf
    if len(source) > 1:
        lf0 = pl.scan_txt(
            source[0],
            separator=r"\s+",
            filter_expr=pl.col("line").str.starts_with("ENERGY"),
        )

    # Change fields to appropriate header values
    columns = [
            "etitle",
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
    fields = lf0.select(pl.col("^field_.*$")).collect_schema().names()
    n_fields = len(fields)
    if n_fields == 16:
        columns = columns[:16]
    lf = lf.rename(dict(zip(fields, columns)))

    # Drop etitle?
    if drop_etitle:
        lf = lf.drop("etitle")

    # Return
    return lf
