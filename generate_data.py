"""
generate_data.py

This script creates FAKE phone call records (like what a telecom company
would hand over to police during an investigation) so we have something
to test our tool with, since we don't have real data.

What it does:
1. Creates a pool of "normal" phone numbers that call each other
   randomly, every now and then -> this is just background noise.
2. Creates a small "suspect group" of phone numbers that call EACH OTHER
   a lot more often than normal people do -> this is the group our tool
   should be able to spot automatically later.
3. Saves everything into a file called call_records.csv (a spreadsheet)
   inside the data/ folder.
"""

import csv
import random
from datetime import datetime, timedelta

# ---- SETTINGS (feel free to change these numbers later) ----
NUM_NORMAL_PEOPLE = 60          # how many "regular" phone numbers exist
NUM_SUSPECT_PEOPLE = 6           # how many people are in our planted suspect group
NUM_NORMAL_CALLS = 1800          # total random background calls
NUM_SUSPECT_CALLS = 250          # calls just between the suspect group (this is the pattern we want visible)
NUM_TOWERS = 15                  # fake cell tower IDs, just for realism
DAYS_RANGE = 30                  # spread calls across the last 30 days

random.seed(42)  # keeps the "random" data the same every time we run this, easier for testing


def random_phone_number():
    """Makes a fake Indian-style 10 digit phone number, e.g. 9876543210"""
    return "9" + "".join(str(random.randint(0, 9)) for _ in range(9))


def random_timestamp():
    """Picks a random date/time within the last DAYS_RANGE days."""
    now = datetime.now()
    random_days_ago = random.uniform(0, DAYS_RANGE)
    return now - timedelta(days=random_days_ago)


def random_tower():
    return f"TWR-{random.randint(1, NUM_TOWERS):03d}"


# Step 1: create our pool of fake phone numbers
normal_numbers = [random_phone_number() for _ in range(NUM_NORMAL_PEOPLE)]
suspect_numbers = [random_phone_number() for _ in range(NUM_SUSPECT_PEOPLE)]

records = []

# Step 2: generate "normal" background call traffic
# these calls are between random pairs of normal people, nothing special
for _ in range(NUM_NORMAL_CALLS):
    caller, callee = random.sample(normal_numbers, 2)  # pick 2 different random people
    records.append({
        "caller": caller,
        "callee": callee,
        "timestamp": random_timestamp().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_sec": random.randint(5, 600),   # call length between 5 sec and 10 min
        "tower_id": random_tower(),
    })

# Step 3: generate the "suspect group" calls
# these calls happen ONLY between our 6 suspect numbers, and there are
# a lot of them relative to the group size -> this creates a dense,
# tightly-connected cluster in the graph that should stand out clearly
for _ in range(NUM_SUSPECT_CALLS):
    caller, callee = random.sample(suspect_numbers, 2)
    records.append({
        "caller": caller,
        "callee": callee,
        "timestamp": random_timestamp().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_sec": random.randint(10, 300),
        "tower_id": random_tower(),
    })

# Step 4: also add a FEW calls from suspects to normal people
# (real suspects don't ONLY call each other, they call normal contacts too
# sometimes - this makes the fake data feel a bit more realistic)
for _ in range(40):
    caller = random.choice(suspect_numbers)
    callee = random.choice(normal_numbers)
    records.append({
        "caller": caller,
        "callee": callee,
        "timestamp": random_timestamp().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_sec": random.randint(5, 200),
        "tower_id": random_tower(),
    })

# Step 5: shuffle everything so it's not neatly grouped in the file
# (real data wouldn't come pre-sorted by "suspect" or "not suspect")
random.shuffle(records)

# Step 6: write it all out to a CSV file (a spreadsheet file)
output_path = "data/call_records.csv"
with open(output_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["caller", "callee", "timestamp", "duration_sec", "tower_id"])
    writer.writeheader()
    writer.writerows(records)

print(f"Done! Created {len(records)} fake call records.")
print(f"Saved to: {output_path}")
print(f"\nHint: the suspect group phone numbers are: {suspect_numbers}")
print("(You won't tell your tool about this list - the tool should FIND this group on its own later.)")
