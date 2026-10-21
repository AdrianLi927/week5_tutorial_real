"""Orchestration: load the recording, compute, report. The checks live in test_vitals.py."""
import vitals

readings = vitals.load_recording("data/recording.csv")
percent = vitals.percent_above(readings, limit_bpm=100)
print("above 100 bpm:", percent, "% of the valid time")

# written by myself
zarr_readings = vitals.load_subject_readings("data/ward4.zarr", "S01")
zarr_percent = vitals.percent_above(zarr_readings, limit_bpm=100)
print("above 100 bpm:", zarr_percent, "% of the valid time")

