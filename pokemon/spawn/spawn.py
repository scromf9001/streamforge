import csv
import random
import json

def run():

    pokemon_csv = r"C:\Users\sebas\Desktop\Stream Stuff\Pokemon System\pokemon_list.csv"

    # ---------- LOAD SPAWNABLE POKEMON ----------

    spawnable = []

    with open(pokemon_csv, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row["can_spawn"].lower() == "yes":
                weight = int(row["spawn_rate"]) if row["spawn_rate"] else 1
                spawnable.append((row, weight))

    if not spawnable:
        return json.dumps({"html": "<div>No spawnable Pokémon found.</div>"})

    # ---------- WEIGHTED RANDOM ----------

    rows = [r[0] for r in spawnable]
    weights = [r[1] for r in spawnable]

    chosen = random.choices(rows, weights=weights, k=1)[0]

    # ---------- BASIC DATA ----------

    number = chosen["number"]
    pokedex_number = chosen["pokedex_number"]
    name = chosen["name"]

    name_api_sound_raw = chosen["name_api_sound"]
    if name_api_sound_raw and name_api_sound_raw.strip().lower() not in ["null", "none", "nan", ""]:
        name_api_sound = name_api_sound_raw.strip()
    else:
        name_api_sound = ""

    primary = chosen["primary_type"].strip().lower()

    raw_secondary = chosen["secondary_type"]
    if raw_secondary and raw_secondary.strip().lower() not in ["null", "none", "nan", ""]:
        secondary = raw_secondary.strip().lower()
    else:
        secondary = None

    form = chosen["form"]
    size = chosen["size"].lower().strip() if chosen["size"] else ""
    is_legendary = chosen["is_legendary"].strip().lower() == "true"

    # ---------- DISPLAY TYPE LOGIC ----------

    if primary == "normal" and secondary:
        display_type = secondary
    else:
        display_type = primary

    if not display_type:
        display_type = "normal"

    # ---------- SPRITE URL ----------

    sprite_id = number
    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{sprite_id}.png"

    # ---------- DEX DISPLAY ----------

    dex_display = str(pokedex_number).zfill(4)

    # ---------- TYPE ICONS ----------

    type_icons = []

    if primary:
        type_icons.append(
            f'<img class="type-icon" src="https://raw.githubusercontent.com/scromf9001/streamforge/refs/heads/main/pokemon/spawn/assets/{primary.capitalize()}.png">'
        )

    if secondary:
        type_icons.append(
            f'<img class="type-icon" src="https://raw.githubusercontent.com/scromf9001/streamforge/refs/heads/main/pokemon/spawn/assets/{secondary.capitalize()}.png">'
        )

    type_icons_html = "".join(type_icons)

    # ---------- CLASS BUILDING ----------

    classes = [f"{display_type}-theme"]

    if size == "large":
        classes.append("large-sprite")

    if is_legendary:
        classes.append("legendary")

    class_string = " ".join(classes)

    # ---------- RENDER HTML ----------

    html = f"""
<div id="maindiv" class="maindiv">
<div id="contentdiv" class="contentdiv">

<div class="spawn-card {class_string}">

    <div class="spawn-bg"></div>
    <div class="type-overlay"></div>

    <img class="pokemon-sprite"
        src="{sprite_url}">

    <div class="info-pill">
        <div class="pill-top">
            <div class="dex-section">
                <img class="mini-ball"
                    src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9_Ball_icon.svg/960px-Pok%C3%A9_Ball_icon.svg.png">
                <span class="dex-number">{dex_display}</span>
            </div>
            <div class="pokemon-name">{name}</div>
        </div>
        <div class="pill-bottom">
            {type_icons_html}
        </div>
    </div>

</div>

</div>
</div>
"""

    # ---------- RETURN JSON ----------

    result = {
        "html": html,
        "name": name,
        "name_api_sound": name_api_sound
    }

    return json.dumps(result)

print(run())