from pathlib import Path

import pytest

from namdtools import read_log, scan_log

FIXTURES = Path(__file__).parent / "fixtures"
SAMPLE_16FIELD = FIXTURES / "sample_16field.log"
SAMPLE_21FIELD = FIXTURES / "sample_21field.log"
SAMPLE_BAD_FIELD_COUNT = FIXTURES / "sample_bad_field_count.log"


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
    df = read_log(str(SAMPLE_16FIELD))
    assert df["ts"].to_list() == [0, 100]
    assert df["bond"].to_list() == pytest.approx([10.0, 11.0])
    assert df["temp"].to_list() == pytest.approx([300.0, 301.0])
    assert df["potential"].to_list() == pytest.approx([-100.0, -99.5])


def test_scan_log_returns_lazyframe():
    lf = scan_log(str(SAMPLE_16FIELD))
    assert lf.collect().equals(read_log(str(SAMPLE_16FIELD)))


def test_read_log_21field_columns():
    df = read_log(str(SAMPLE_21FIELD))
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
        "pressure",
        "gpressure",
        "volume",
        "pressavg",
        "gpressavg",
    }


def test_read_log_21field_values():
    df = read_log(str(SAMPLE_21FIELD))
    assert df["ts"].to_list() == [0, 100]
    assert df["volume"].to_list() == pytest.approx([123456.0, 123457.0])


def test_read_log_rejects_unexpected_field_count():
    with pytest.raises(ValueError, match="unexpected number of ENERGY fields"):
        read_log(str(SAMPLE_BAD_FIELD_COUNT))
