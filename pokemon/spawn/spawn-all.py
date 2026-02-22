import csv
import random

def run():

    pokemon_csv = r"C:\Users\sebas\Desktop\Stream Stuff\Pokemon System\pokemon_list.csv"

    # ---------- LOAD SPAWNABLE POKEMON ----------

    spawnable = []

    with open(pokemon_csv, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            if row["can_spawn"].lower() == "true" and row["is_mythic"].lower() != "true":
                weight = int(row["spawn_rate"]) if row["spawn_rate"] else 1
                spawnable.append((row, weight))

    if not spawnable:
        return "<div>No spawnable Pokémon found.</div>"

    # ---------- WEIGHTED RANDOM ----------

    rows = [r[0] for r in spawnable]
    weights = [r[1] for r in spawnable]

    chosen = random.choices(rows, weights=weights, k=1)[0]

    # ---------- BASIC DATA ----------

    number = chosen["number"]
    pokedex_number = chosen["pokedex_number"]
    name = chosen["name"]
    primary = chosen["primary_type"].lower()
    secondary = chosen["secondary_type"].lower() if chosen["secondary_type"] else None
    form = chosen["form"]
    size = chosen["size"].lower() if chosen["size"] else ""
    is_legendary = chosen["is_legendary"].lower() == "true"

    # ---------- DISPLAY TYPE LOGIC ----------

    if primary == "normal" and secondary:
        display_type = secondary
    else:
        display_type = primary

    # ---------- SPRITE URL ----------

    if form:
        sprite_id = f"{number}-{form}"
    else:
        sprite_id = number

    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{sprite_id}.png"

    # ---------- DEX DISPLAY ----------

    dex_display = str(pokedex_number).zfill(4)

    # ---------- TYPE ICONS ----------

    type_icons = []

    for t in [primary, secondary]:
        if t:
            type_icons.append(
                f'<img class="type-icon" src="https://i.ibb.co/{t.capitalize()}.png">'
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

    return html


print(run())