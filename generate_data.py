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
3. Makes ONE of the suspects a "coordinator" -> they call outside
   contacts more than the rest of the group, which should make them
   stand out as a "bridge" number in the analysis (the one connecting
   the suspect operation to the outside world).
4. Makes ONE normal number a "social hub" -> lots of different normal
   people call this one number a lot (like a shop or a shared contact),
   so our "top hub numbers" result has a believable, non-suspicious
   example too, not just suspects.
5. Saves everything into a file called call_records.csv (a spreadsheet)
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
NUM_COORDINATOR_CALLS = 55       # extra calls from the coordinator to outside contacts
NUM_HUB_CALLS = 160              # calls FROM many different normal people TO our planted social hub
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


def add_call(records, caller, callee, duration_range):
    records.append({
        "caller": caller,
        "callee": callee,
        "timestamp": random_timestamp().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_sec": random.randint(*duration_range),
        "tower_id": random_tower(),
    })


# Step 1: create our pool of fake phone numbers
normal_numbers = [random_phone_number() for _ in range(NUM_NORMAL_PEOPLE)]
suspect_numbers = [random_phone_number() for _ in range(NUM_SUSPECT_PEOPLE)]

# pick one suspect to be the "coordinator" (bridges the group to outsiders)
coordinator = suspect_numbers[0]

# pick one normal number to be the "social hub" (naturally popular, not suspicious)
social_hub = normal_numbers[0]

records = []

# Step 2: generate "normal" background call traffic
for _ in range(NUM_NORMAL_CALLS):
    caller, callee = random.sample(normal_numbers, 2)
    add_call(records, caller, callee, (5, 600))

# Step 3: generate the "suspect group" calls
# these calls happen ONLY between our 6 suspect numbers, and there are
# a lot of them relative to the group size -> this creates a dense,
# tightly-connected cluster in the graph that should stand out clearly
for _ in range(NUM_SUSPECT_CALLS):
    caller, callee = random.sample(suspect_numbers, 2)
    add_call(records, caller, callee, (10, 300))

# Step 4: the coordinator calls a WIDE spread of normal people, more
# than any other suspect does. This should push their "bridge" (betweenness)
# score up, since they're the one connecting the tight suspect cluster to
# the rest of the network.
outside_contacts = random.sample(normal_numbers, 15)
for _ in range(NUM_COORDINATOR_CALLS):
    callee = random.choice(outside_contacts)
    add_call(records, coordinator, callee, (5, 200))

# Step 5: a FEW other suspects also call normal people sometimes (keeps
# the data realistic, real suspects don't ONLY call each other)
for _ in range(30):
    caller = random.choice(suspect_numbers[1:])  # everyone except the coordinator
    callee = random.choice(normal_numbers)
    add_call(records, caller, callee, (5, 200))

# Step 6: the social hub gets called by lots of DIFFERENT normal people,
# this is what makes them a "hub" by degree centrality, a believable
# non-suspicious example (like a popular shop or shared community contact)
callers_to_hub = [n for n in normal_numbers if n != social_hub]
for _ in range(NUM_HUB_CALLS):
    caller = random.choice(callers_to_hub)
    add_call(records, caller, social_hub, (20, 400))

# Step 7: shuffle everything so it's not neatly grouped in the file
# (real data wouldn't come pre-sorted by "suspect" or "not suspect")
random.shuffle(records)

# Step 8: write it all out to a CSV file (a spreadsheet file)
output_path = "data/call_records.csv"
with open(output_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["caller", "callee", "timestamp", "duration_sec", "tower_id"])
    writer.writeheader()
    writer.writerows(records)

print(f"Done! Created {len(records)} fake call records.")
print(f"Saved to: {output_path}")
print(f"\nSuspect group: {suspect_numbers}")
print(f"Coordinator (should show up as a top 'bridge' number): {coordinator}")
print(f"Social hub (should show up as a top 'hub' number, but is NOT a suspect): {social_hub}")
print("\n(You won't tell your tool about any of this, the tool should FIND these patterns on its own.)")
