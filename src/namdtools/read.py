from fpathlib import iexpand_fpath, is_expandable
import fpathlib.ext.polars as pl
from glob import iglob


# Read NAMD log file
def read_log(source, drop_etitle=True):
    return scan_log(source, drop_etitle).collect()

# Scan NAMD log file
def scan_log(source, drop_etitle=True, validate_schema=True):
    r"""
    Scan NAMD log file.

    Parameters
    ----------
    source : :obj:`str`
        Name of NAMD log file.
    drop_etitle : :obj:`bool`
        Drop the first column of the log file, which is the title of the energy term. (Default: True).
    validate_schema : :obj:`bool`
        Validate the schema of the log file. (Default: True).

    Returns
    -------
    DataFrame
    """

    # Is `source` expandable or globable?
    first_source = None
    if is_expandable(source):
        first_source = next(iexpand_fpath(source), None)
    else:
        first_source = next(iglob(source), None)

    # Scan `source`
    lf = pl.scan_txt(
        source,
        separator=r"\s+",
        filter_expr=pl.col("line").str.starts_with("ENERGY"),
        validate_schema=validate_schema,
    )

    # Scan `first_source` if it exists
    lf0 = lf
    if first_source:
        lf0 = pl.scan_txt(
            first_source,
            separator=r"\s+",
            filter_expr=pl.col("line").str.starts_with("ENERGY"),
            validate_schema=validate_schema,
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
    fields = lf0.head(1).select(pl.col("^field_.*$")).collect(engine="streaming").schema.names()
    n_fields = len(fields)
    if n_fields == 16:
        columns = columns[:16]
    elif n_fields != 21:
        msg = f"unexpected number of ENERGY fields: {n_fields} (expected 16 or 21)"
        raise ValueError(msg)
    lf = lf.rename(dict(zip(fields, columns)))

    # Drop etitle?
    if drop_etitle:
        lf = lf.drop("etitle")

    # Return
    return lf
