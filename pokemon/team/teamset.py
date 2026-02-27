import json
import os

STATE_FILE = r"C:\Users\sebas\Desktop\Stream Stuff\streamforge\pokemon\team\active_team.json"

SPRITE_BASE = "https://img.pokemondb.net/sprites/firered-leafgreen/normal/{}.png"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def run():

    slot = "$arg1text"
    pokemon_name = "$arg2text"

    # Validate slot
    if not slot.isdigit():
        return {"status": "error", "message": "Invalid slot"}

    slot = str(int(slot))

    if int(slot) < 1 or int(slot) > 6:
        return {"status": "error", "message": "Slot must be 1-6"}

    if not pokemon_name:
        return {"status": "error", "message": "No Pokemon name provided"}

    pokemon_slug = pokemon_name.strip().lower()

    state = load_state()

    state[slot] = {
        "name": pokemon_slug,
        "sprite": SPRITE_BASE.format(pokemon_slug)
    }

    save_state(state)

    return {
        "status": "success",
        "slot": slot,
        "pokemon": pokemon_slug
    }

print(json.dumps(run()))