import json
import os

STATE_FILE = r"C:\Users\sebas\Desktop\Stream Stuff\Pokemon System\active_team.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def run():

    slot = "$arg2text"

    if not slot.isdigit():
        return {"status": "error"}

    slot = str(int(slot))

    state = load_state()

    if slot in state:
        del state[slot]

    save_state(state)

    return {"status": "cleared", "slot": slot}

print(json.dumps(run()))