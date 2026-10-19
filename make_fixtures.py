"""Run once: writes the files whose answer we know by construction."""
import vitals

vitals.make_recording_file("data/known_20_6.csv", n_total=20, n_above=6, limit_bpm=100)
vitals.make_recording_file("data/known_10_10.csv", n_total=10, n_above=10, limit_bpm=100)
print("fixtures written to data/")
