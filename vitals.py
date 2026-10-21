"""Steps for heart-rate recordings. Definitions only: importing this file prints nothing."""

from typing import cast

import zarr


# PROMPT (final version used):
# Write a Python function load_recording(path) that reads a heart-rate file
# exported by the wearable. Lines starting with '#' are notes from the device
# and are skipped. The first other line is the header 'time_s,hr_bpm'.
# Every line after it is a time in seconds and a heart rate in bpm,
# separated by a comma. An empty heart rate means a dropped sample:
# return it as 0, because that is what percent_above expects.
# Return the heart rates as a list of floats, in file order.
# Open the file with encoding="utf-8". If the file does not exist, let the
# FileNotFoundError happen. Type hints and a docstring stating the units.
# Plain Python, no packages.
def load_recording(path) -> list:
    """Load heart rates (bpm) from a wearable export file.

    Lines starting with '#' are skipped, as is the 'time_s,hr_bpm' header.
    An empty heart-rate field is a dropped sample and is returned as 0.0.
    Returns a list of floats in bpm, in the order they appear in the file.
    """
    readings_bpm = []
    header_seen = False
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            if not header_seen:
                header_seen = True
                continue
            time_text, hr_text = line.split(",")
            if hr_text == "":
                readings_bpm.append(0.0)
            else:
                readings_bpm.append(float(hr_text))
    return readings_bpm

# PROMPT (final version used):
# Help implement this function `load_subject_readings(store_path, subject_id: str) -> list:`
# The readings, unlike in `load_recordings`, will take data from the `data/ward4.zarr` folder (using zarr 3) with `store_path` being `data/ward4.zarr` and `subject_id` being the folder names S01 S02 ect
# Inspect the zarr folder data structure and return it in the same format as in `load_recording` (so a list[float])
# Raise a `ValueError` for subjects not in the `data/ward4.zarr` folder
# Add docstrings mentioning each variable
# Dont run any tests yet when implementing, that will come later
# Make no mistakes.
def load_subject_readings(store_path, subject_id: str) -> list:
    """Load a subject's heart rates in bpm from a Zarr 3 study.

    Args:
        store_path: Path to the read-only Zarr study store.
        subject_id: Subject group name, such as ``S01``.

    Returns:
        A list of the subject's heart-rate readings as floats in bpm.

    Raises:
        ValueError: If subject_id is not present in the study.
    """
    study = zarr.open_group(store=store_path, mode="r")
    if subject_id not in study:
        raise ValueError(f"subject not found: {subject_id}")
    readings_bpm = cast(list[float], study[f"{subject_id}/hr_bpm"][:])
    return [float(reading) for reading in readings_bpm]


# PROMPT (final version used, week 3):
# Write a Python function percent_above(readings, limit_bpm).
# readings is a list of heart rates in bpm; a reading of 0 means a dropped
# sample and anything above 250 bpm is an artefact — neither is part of the
# recording. limit_bpm is the limit in bpm; a reading exactly equal to it
# does not count as above. Return the percentage of the remaining readings
# that are above the limit, rounded to one decimal. If there are no valid
# readings, raise a ValueError. Type hints and a docstring stating the units.
# Plain Python, no packages.
def percent_above(readings: list, limit_bpm: float) -> float:
    """Percentage (0-100, one decimal) of the valid readings above limit_bpm.

    Readings of 0 (dropped samples) and above 250 bpm (artefacts) are ignored.
    A reading exactly equal to limit_bpm does not count as above.
    Raises ValueError if there are no valid readings.
    """
    valid = 0
    above = 0
    for hr in readings:
        if hr != 0 and hr <= 250:
            valid = valid + 1
            if hr > limit_bpm:
                above = above + 1
    if valid == 0:
        raise ValueError("no valid readings")
    return round(100 * above / valid, 1)


# PROMPT (final version used):
# Write a Python function make_recording_file(path, n_total, n_above, limit_bpm)
# that writes a heart-rate file in exactly the same format as the wearable:
# one line '# made by make_recording_file', then the header 'time_s,hr_bpm',
# then n_total lines 'time,heart rate', with times 0, 15, 30, ... seconds.
# The first n_above heart rates are limit_bpm + 10; the others are
# limit_bpm - 10. Write whole numbers. No dropped samples, no artefacts.
# Raise ValueError if n_above > n_total. Open with encoding="utf-8".
# Type hints and a docstring. Plain Python, no packages.
def make_recording_file(path, n_total: int, n_above: int, limit_bpm: float) -> None:
    """Write a wearable-format file of n_total readings, n_above above limit_bpm.

    Readings above the limit are limit_bpm + 10 bpm, the rest limit_bpm - 10 bpm,
    one every 15 s. The answer of percent_above on it is known by construction:
    100 * n_above / n_total.
    """
    if n_above > n_total:
        raise ValueError("n_above cannot be larger than n_total")
    with open(path, "w", encoding="utf-8") as file:
        file.write("# made by make_recording_file\n")
        file.write("time_s,hr_bpm\n")
        for i in range(n_total):
            if i < n_above:
                hr_bpm = limit_bpm + 10
            else:
                hr_bpm = limit_bpm - 10
            file.write(f"{i * 15},{hr_bpm:.0f}\n")
