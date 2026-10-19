"""Orchestration: load the recording, compute, report. The checks live in test_vitals.py."""
import vitals

readings = vitals.load_recording("data/recording.csv")
percent = vitals.percent_above(readings, limit_bpm=100)
print("above 100 bpm:", percent, "% of the valid time")
