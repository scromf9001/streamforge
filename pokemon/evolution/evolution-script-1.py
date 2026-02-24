import csv
import json

# ==============================
# CONFIG
# ==============================

arg1 = "$arg1text"
arg2 = "$arg2text"
display_username = "$userdisplayname"

CSV_PATH = r"C:\Users\sebas\Desktop\Stream Stuff\Pokemon System\pokemon_list.csv"

DEFAULT_QUANTITY_REQUIRED = 3


# ==============================
# HELPERS
# ==============================

def normalize_loose(text):
    return (
        text.lower()
        .replace(".", "")
        .replace("'", "")
        .replace("(", "")
        .replace(")", "")
        .replace(" ", "")
    )


def normalize_item(name):
    if not name:
        return None
    return name.lower().replace(" ", "")


def load_data():
    with open(CSV_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_pokemon(data, arg1, arg2):

    if not arg2 or arg2.strip() == "" or arg2.strip().startswith("$arg"):
        raw_input = arg1
    else:
        raw_input = f"{arg1} {arg2}"

    strict = raw_input.strip().lower()
    loose = normalize_loose(raw_input)

    for row in data:
        if row["name"].strip().lower() == strict:
            return row
        if normalize_loose(row["name_api_sound"]) == loose:
            return row

    return None


# ==============================
# MAIN
# ==============================

def run():

    data = load_data()

    base_row = find_pokemon(data, arg1, arg2)

    # ------------------------------
    # SPELLING ERROR
    # ------------------------------
    if not base_row:
        return {
            "stage": "final",
            "status": "error",
            "error_code": "POKEMON_NOT_FOUND"
        }

    # ------------------------------
    # NO EVOLUTION
    # ------------------------------
    if not base_row["evolution"]:
        return {
            "stage": "final",
            "status": "error",
            "error_code": "NO_EVOLUTION_AVAILABLE",
            "base_name": base_row["name"]
        }

    # ------------------------------
    # FIND EVOLUTION ROW
    # ------------------------------
    evo_row = None
    for row in data:
        if row["name"].strip().lower() == base_row["evolution"].strip().lower():
            evo_row = row
            break

    if not evo_row:
        return {
            "stage": "final",
            "status": "error",
            "error_code": "EVOLUTION_DATA_MISSING"
        }

    # ------------------------------
    # CORE VALUES
    # ------------------------------
    basepokemonsp = base_row["name_api_sound"]
    evolutionsp = evo_row["name_api_sound"]

    evolutionline = base_row["evolution_line_id"]

    required_quantity = int(base_row["quantity_required"] or DEFAULT_QUANTITY_REQUIRED)

    # ------------------------------
    # REQUIREMENT RESOLUTION
    # ------------------------------
    requirement_type = "none"
    requirement_display_name = None
    itemsp = None

    user_quantity = "$userpokedex" + basepokemonsp
    user_item_quantity = 0
    user_friendship = 0

    if base_row["item_required"] == "Yes":

        requirement = base_row["requirement"]

        if requirement == "Trade":
            requirement_type = "trade"

        elif requirement == "Friendship":
            requirement_type = "friendship"
            user_friendship = "$userpokefriendship" + str(evolutionline)

        else:
            requirement_type = "item"
            requirement_display_name = requirement
            itemsp = normalize_item(requirement)
            user_item_quantity = "$userpokebag" + itemsp

    # ------------------------------
    # RETURN COMPLETE METADATA
    # ------------------------------

    return {
        "display_username": display_username,
        "stage": "resolve",
        "status": "continue",

        # ----- Base Pokémon -----
        "base_name": base_row["name"],
        "basepokemonsp": basepokemonsp,
        "base_number": base_row["number"],
        "base_pokedex_number": base_row["pokedex_number"],
        "base_primary_type": base_row["primary_type"],
        "base_secondary_type": base_row["secondary_type"],
        "base_size": base_row["size"],
        "base_is_legendary": base_row["is_legendary"],

        # ----- Evolution Pokémon -----
        "evo_name": evo_row["name"],
        "evo_number": evo_row["number"],
        "evo_pokedex_number": evo_row["pokedex_number"],
        "evo_primary_type": evo_row["primary_type"],
        "evo_secondary_type": evo_row["secondary_type"],
        "evo_size": evo_row["size"],
        "evo_is_legendary": evo_row["is_legendary"],
        "evolutionsp": evolutionsp,

        # ----- Evolution Line -----
        "evolutionline": evolutionline,

        # ----- Requirement -----
        "required_quantity": required_quantity,
        "requirement_type": requirement_type,
        "requirement_display_name": requirement_display_name,
        "itemsp": itemsp,

        # ----- Inventory (Literal Identifiers) -----
        "user_quantity": user_quantity,
        "user_item_quantity": user_item_quantity,
        "user_friendship": user_friendship
    }


print(json.dumps(run()))