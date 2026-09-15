from pathlib import Path

from namdtools import read_log, scan_log

FIXTURES = Path(__file__).parent / "fixtures"
SAMPLE_16FIELD = FIXTURES / "sample_16field.log"


def test_read_log_drops_etitle_by_default():
    df = read_log(str(SAMPLE_16FIELD))
    assert "etitle" not in df.columns


def test_read_log_keeps_etitle_when_requested():
    df = read_log(str(SAMPLE_16FIELD), drop_etitle=False)
    assert "etitle" in df.columns
    assert set(df["etitle"].to_list()) == {"ENERGY:"}


def test_read_log_columns():
    df = read_log(str(SAMPLE_16FIELD))
    assert set(df.columns) == {
        "fname",
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
    }


def test_read_log_values():
    # fields are parsed as strings, not numeric types
    df = read_log(str(SAMPLE_16FIELD))
    assert df["ts"].to_list() == ["0", "100"]
    assert df["bond"].to_list() == ["10.0000", "11.0000"]
    assert df["temp"].to_list() == ["300.0000", "301.0000"]
    assert df["potential"].to_list() == ["-100.0000", "-99.5000"]


def test_scan_log_returns_lazyframe():
    lf = scan_log(str(SAMPLE_16FIELD))
    assert lf.collect().equals(read_log(str(SAMPLE_16FIELD)))
