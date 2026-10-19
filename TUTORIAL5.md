# Tutorial 5 — The same night, from the study

Last week's project reads the wristband's CSV file. The ward now keeps every recording in a Zarr study, `data/ward4.zarr`, and the night you know (S01) is in it.

**Your goal:** one new step in `vitals.py` that reads a subject's heart rates from the study, so that every step you already have works on it unchanged. Then **package the project** and prove that it works somewhere else, starting from nothing.

There is no skeleton. The steps say *what* to do, not how.

## 1. Set up

- This zip is last week's project, plus `data/ward4.zarr`. Unzip it into a new folder, open the folder in VS Code, create the `.venv`, select the interpreter.
- `python -m pip install pytest zarr`
- Run `python -m pytest`. Do not go on until it says **7 passed**.

## 2. Look first

In the VS Code explorer, open `data/ward4.zarr`, then `S01`, then `hr_bpm`. Open the two `zarr.json` files you find on the way. Do not ask an assistant yet.

Write down, at the bottom of this file:

- the device of S01, its units, and the time between two readings;
- how many readings S01 has, and how many S02 has — and where in the file you found that number.

## 3. SPECIFY the new step

In `vitals.py`, below `load_recording`, write the signature

```python
def load_subject_readings(store_path, subject_id: str) -> list:
```

and above it a `# PROMPT` block with the prompt you are going to send. It must give back **exactly what `load_recording` gives** for the same night: the same type, the same units, the same treatment of dropped samples. Decide in the prompt, at least:

- which version of zarr (the one you installed: zarr 3);
- how the store is opened — it is raw data;
- where the heart rates are inside the store;
- what comes back, and in which type (a list, or a numpy array?);
- what happens if the subject is not in the study.

## 4. Write the checks before the body

In `test_vitals.py`, below the existing tests, two new test functions, each with a name starting `test_` and a docstring that says what goes in, what must come out, and where that value came from:

- S01 from the study gives **the same list** as `load_recording("data/recording.csv")`;
- S02 has the number of readings you read in its `zarr.json` in step 2.

Every new body is `assert False, "body not written yet"`. Run `python -m pytest`: the two new tests must be red. The bodies may then come from an assistant, in a **new chat**, without `vitals.py`.

## 5. Order the body, and run

Send your `# PROMPT`, put the body under your signature, and run `python -m pytest` until it says **9 passed**. If something fails, decide which of the four it is **before** asking for a fix: the specification, the call, the body, or the file — or, new this week, the **environment** (the wrong version of a package).

Then add two lines to `main.py`: load S01 from the study, and print its percentage above 100 bpm. It must be the same 42.9 as the CSV.

## 6. Package it

Write `requirements.txt`: one line per package this project needs, with the versions it was written for.

Now prove that the project works without your laptop's history:

1. Zip the project folder **without** `.venv`.
2. Unzip it into a **new, empty folder** somewhere else.
3. Open that folder in VS Code, create a new `.venv`, select the interpreter.
4. `python -m pip install -r requirements.txt` — and nothing else.
5. `python -m pytest`, then `python main.py`.

If anything fails in the new folder, write down what, and which of the five it is, then fix it **in the original project** and repeat from 1. This is exactly what the marker does with your Assignment 5.

Then start Assignment 5.

---

## What I found in step 2

- S01: device: wristband, units: bpm, one reading every 15 s
- S01 has 10 readings; S02 has 15 readings; I found it in SXX/hr_bpm/zarr.json -> shape

## What failed in step 6 (if anything)

-
