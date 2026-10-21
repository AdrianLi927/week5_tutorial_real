# PROMPT (final version used, sent in a new chat, without vitals.py):
# I am testing a module called vitals with pytest. Write the bodies of the
# test functions below. Use only the expected values I give in each
# docstring; do not compute them, do not import anything except pytest and
# vitals, and do not change the names.
import pytest
import vitals


def test_load_reads_every_line():
    """data/recording.csv has 10 readings; the third one is a dropped sample (0)."""
    readings = vitals.load_recording("data/recording.csv")
    assert len(readings) == 10
    assert readings[2] == 0


def test_load_hand_written_gaps():
    """data/two_gaps.csv was written by hand: [120, 0, 0, 90]."""
    assert vitals.load_recording("data/two_gaps.csv") == [120, 0, 0, 90]


def test_load_missing_file():
    """A file that is not there must fail loudly."""
    with pytest.raises(FileNotFoundError):
        vitals.load_recording("data/no_such_file.csv")


def test_known_file_20_6():
    """Made by make_fixtures.py: 20 readings, 6 above 100 -> 30.0 %."""
    readings = vitals.load_recording("data/known_20_6.csv")
    assert vitals.percent_above(readings, limit_bpm=100) == pytest.approx(30.0)


def test_known_file_all_above():
    """Made by make_fixtures.py: 10 readings, all above 100 -> 100.0 %."""
    readings = vitals.load_recording("data/known_10_10.csv")
    assert vitals.percent_above(readings, limit_bpm=100) == pytest.approx(100.0)


def test_exactly_on_the_limit():
    """A reading exactly on the limit does not count as above."""
    assert vitals.percent_above([100, 100], limit_bpm=100) == pytest.approx(0.0)


def test_empty_recording_is_refused():
    """No valid readings -> ValueError, as the prompt says."""
    with pytest.raises(ValueError):
        vitals.percent_above([0, 0, 0], limit_bpm=100)
 
 # written myself manually       
def test_zarr_readings_same():
    """Tests if readings that came from the csv and the zarr readers are equal (patient id S01)"""
    csv_readings = vitals.load_recording("data/recording.csv")
    zarr_readings = vitals.load_subject_readings("data/ward4.zarr", "S01")
    assert csv_readings == zarr_readings
    
 # written myself manually
def test_zarr_readings_length():
    """Tests if the length of readings from S02 is as expected"""
    EXPECTED = 15
    zarr_readings = vitals.load_subject_readings("data/ward4.zarr", "S02")
    assert len(zarr_readings) == EXPECTED
