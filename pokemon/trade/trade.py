import csv
import json

# =====================================================
# CONFIG
# =====================================================

CSV_PATH = r"C:\Users\sebas\Desktop\Stream Stuff\Pokemon System\pokemon_list.csv"

# MixItUp identifiers
user_a_display = "$userdisplayname"
user_b_display = "$targetuserdisplayname"
pokemon_a_raw = "$itemname"
pokemon_b_raw = "$targetitemname"


# =====================================================
# HELPERS
# =====================================================

def clean_arg(raw):
    s = raw.strip()
    if not s or s.startswith("$"):
        return ""
    return s.lower()


def load_data():
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def find_pokemon(data, search_name):
    for row in data:
        if row["name"].strip().lower() == search_name:
            return row
    return None


def requires_trade(row):
    return (
        row["item_required"] == "Yes" and
        row["requirement"] == "Trade"
    )


def build_type_icons(primary, secondary):
    icons = f'<img class="type-icon" src="https://raw.githubusercontent.com/scromf9001/streamforge/refs/heads/main/pokemon/spawn/assets/{primary}.png">'
    if secondary and secondary != "Null":
        icons += f'<img class="type-icon" src="https://raw.githubusercontent.com/scromf9001/streamforge/refs/heads/main/pokemon/spawn/assets/{secondary}.png">'
    return icons


def render_spawn_card(name, number, pokedex_number,
                      primary_type, secondary_type,
                      size, is_legendary,
                      evolving=False,
                      flash_mode=None,
                      display_username=None):

    type_class = f"{primary_type.lower()}-theme"
    legendary_class = " legendary" if str(is_legendary).upper() == "TRUE" else ""
    size_class = " large-sprite" if size == "large" else ""
    evolving_class = " evolving" if evolving else ""

    type_icons = build_type_icons(primary_type, secondary_type)

    owner_html = f'<div class="card-owner">{display_username}</div>' if display_username else ""

    if flash_mode == "animate":
        flash_div = '<div class="evolution-flash flash-animate"></div>'
    elif flash_mode == "fadeout":
        flash_div = '<div class="evolution-flash flash-fadeout"></div>'
    else:
        flash_div = ""

    return f"""
<div id="maindiv" class="maindiv">
<div id="contentdiv" class="contentdiv">

<div class="spawn-card {type_class}{legendary_class}{size_class}{evolving_class}">
    {owner_html}
    <div class="spawn-bg"></div>
    <div class="type-overlay"></div>
    {flash_div}

    <img class="pokemon-sprite"
         src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{number}.png">

    <div class="info-pill">
        <div class="pill-top">
            <div class="dex-section">
                <img class="mini-ball"
                     src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9_Ball_icon.svg/960px-Pok%C3%A9_Ball_icon.svg.png">
                <span class="dex-number">{pokedex_number}</span>
            </div>
            <div class="pokemon-name">{name}</div>
        </div>
        <div class="pill-bottom">
            {type_icons}
        </div>
    </div>

</div>
</div>
</div>
"""


# =====================================================
# MAIN
# =====================================================

def run():

    data = load_data()

    pokemon_a_name = clean_arg(pokemon_a_raw)
    pokemon_b_name = clean_arg(pokemon_b_raw)

    if not pokemon_a_name or not pokemon_b_name:
        return {
            "status": "error",
            "result_type": None,
            "messages": {
                "start": None,
                "complete": None,
                "error_message": "Invalid trade input."
            }
        }

    row_a = find_pokemon(data, pokemon_a_name)
    row_b = find_pokemon(data, pokemon_b_name)

    if not row_a or not row_b:
        return {
            "status": "error",
            "result_type": None,
            "messages": {
                "start": None,
                "complete": None,
                "error_message": "One or both Pokémon not found."
            }
        }

    # Resolve evolution rows
    evo_a = find_pokemon(data, row_a["evolution"].strip().lower()) if row_a["evolution"] else None
    evo_b = find_pokemon(data, row_b["evolution"].strip().lower()) if row_b["evolution"] else None

    a_trade = requires_trade(row_a)
    b_trade = requires_trade(row_b)

    # =====================================================
    # DETERMINE RESULT TYPE
    # =====================================================

    if a_trade and b_trade:
        result_type = "trade_evolution_success"
        final_left = evo_b
        final_right = evo_a

    elif a_trade or b_trade:
        result_type = "trade_evolution_failed_requirement"
        final_left = row_b
        final_right = row_a

    else:
        result_type = "normal_trade"
        final_left = row_b
        final_right = row_a

    # =====================================================
    # RENDER START CARDS
    # =====================================================

    rendered_html_left_start = render_spawn_card(
        row_a["name"],
        row_a["number"],
        row_a["pokedex_number"],
        row_a["primary_type"],
        row_a["secondary_type"],
        row_a["size"],
        row_a["is_legendary"],
        evolving=False,
        flash_mode="animate",
        display_username=user_a_display
    )

    rendered_html_right_start = render_spawn_card(
        row_b["name"],
        row_b["number"],
        row_b["pokedex_number"],
        row_b["primary_type"],
        row_b["secondary_type"],
        row_b["size"],
        row_b["is_legendary"],
        evolving=False,
        flash_mode="animate",
        display_username=user_b_display
    )

    # =====================================================
    # RENDER FINAL CARDS
    # =====================================================

    rendered_html_left_complete = render_spawn_card(
        final_left["name"],
        final_left["number"],
        final_left["pokedex_number"],
        final_left["primary_type"],
        final_left["secondary_type"],
        final_left["size"],
        final_left["is_legendary"],
        evolving=False,
        flash_mode="fadeout",
        display_username=user_a_display
    )

    rendered_html_right_complete = render_spawn_card(
        final_right["name"],
        final_right["number"],
        final_right["pokedex_number"],
        final_right["primary_type"],
        final_right["secondary_type"],
        final_right["size"],
        final_right["is_legendary"],
        evolving=False,
        flash_mode="fadeout",
        display_username=user_b_display
    )

    # =====================================================
    # RETURN CONTRACT
    # =====================================================

    return {
        "status": "success",
        "result_type": result_type,

        "messages": {
            "start": f"🔄 @{user_a_display} and @{user_b_display} are trading!",
            "complete": "Trade complete.",
            "error_message": "Both Pokémon must require trade to evolve." if result_type == "trade_evolution_failed_requirement" else None
        },

        "pokemon_a_before": row_a["name"],
        "pokemon_b_before": row_b["name"],
        "pokemon_a_after": final_left["name"],
        "pokemon_b_after": final_right["name"],

        "special_identifiers": {
            "pokemon_a_original_sp": row_a["name_api_sound"],
            "pokemon_b_original_sp": row_b["name_api_sound"],
            "pokemon_a_final_sp": final_left["name_api_sound"],
            "pokemon_b_final_sp": final_right["name_api_sound"]
        },

        "rendered_html_left_start": rendered_html_left_start,
        "rendered_html_right_start": rendered_html_right_start,
        "rendered_html_left_complete": rendered_html_left_complete,
        "rendered_html_right_complete": rendered_html_right_complete
    }


print(json.dumps(run()))