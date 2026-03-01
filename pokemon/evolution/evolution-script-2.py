import json

SUCCESS_SOUND = r"C:\Users\sebas\Desktop\Stream Stuff\Pokemon System\Sounds\Evolution fanfare.MP3"
FAILURE_SOUND = r"C:\Users\sebas\Desktop\Stream Stuff\Pokemon System\Sounds\failed evolution.wav"

FRIENDSHIP_REQUIRED = 600


# =====================================================
# HELPERS
# =====================================================

def normalize_item(name):
    if not name:
        return None
    return name.lower().replace(" ", "")


def build_type_icons(primary, secondary):
    icons = f'<img class="type-icon" src="https://raw.githubusercontent.com/scromf9001/streamforge/refs/heads/main/pokemon/spawn/assets/{primary}.png">'
    if secondary and secondary != "Null":
        icons += f'<img class="type-icon" src="https://raw.githubusercontent.com/scromf9001/streamforge/refs/heads/main/pokemon/spawn/assets/{secondary}.png">'
    return icons

def sanitize_sprite_number(number):
    try:
        return str(int(float(number)))
    except (ValueError, TypeError):
        return str(number)

def render_spawn_card(name, number, pokedex_number,
                      primary_type, secondary_type,
                      size, is_legendary,
                      evolving=False,
                      flash_mode=None,
                      display_username=None):

    # secondary type as main if primary type is normal
    visual_primary = primary_type
    visual_secondary = secondary_type

    if primary_type and primary_type.lower() == "normal":
        if secondary_type and secondary_type.lower() not in ["null", "none", ""]:
            visual_primary = secondary_type
            visual_secondary = None  # Avoid double icon duplication

    type_class = f"{visual_primary.lower()}-theme"

    legendary_class = " legendary" if str(is_legendary).upper() == "TRUE" else ""
    size_class = " large-sprite" if size == "large" else ""
    evolving_class = " evolving" if evolving else ""
    sprite_number = sanitize_sprite_number(number)

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
         src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{sprite_number}.png"

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

    data = json.loads(r'''$scriptresult''')

    # =====================================================
    # FINAL ERRORS FROM SCRIPT 1
    # =====================================================
    if data["stage"] == "final":

        error_code = data["error_code"]
        base_name = data.get("base_name")

        if error_code == "POKEMON_NOT_FOUND":
            error_message = "MissingNo spotted! Make sure you use the correct spelling!"
        elif error_code == "NO_EVOLUTION_AVAILABLE":
            error_message = f"Huh? {base_name} doesn't have an evolution!"
        elif error_code == "EVOLUTION_DATA_MISSING":
            error_message = "Evolution data is missing from the Pokédex."
        else:
            error_message = f"Unhandled error: {error_code}"

        return {
            "status": "error",
            "error_code": error_code,
            "result_type": None,
            "messages": {
                "start": None,
                "complete": None,
                "error_message": error_message
            },
            "sound_url": FAILURE_SOUND,
            "base_pokemon": None,
            "evolved_pokemon": None,
            "special_identifiers": None,
            "requirement_data": None,
            "rendered_html_start": None,
            "rendered_html_complete": None
        }

    # =====================================================
    # LOAD VALUES
    # =====================================================

    base_name = data["base_name"]
    evo_name = data["evo_name"]

    user_quantity = int(data["user_quantity"])
    required_quantity = int(data["required_quantity"])

    user_item_quantity = int(data["user_item_quantity"])
    user_friendship = int(data["user_friendship"])

    requirement_type = data["requirement_type"]
    requirement_display_name = data["requirement_display_name"]

    evolutionline = data["evolutionline"]
    itemsp = normalize_item(requirement_display_name)

    inventory_identifier = None

    # =====================================================
    # BASE STRUCTURE OBJECTS
    # =====================================================

    base_pokemon = {
        "name": base_name,
        "number": data["base_number"],
        "pokedex_number": data["base_pokedex_number"],
        "primary_type": data["base_primary_type"],
        "secondary_type": data["base_secondary_type"],
        "size": data["base_size"],
        "is_legendary": data["base_is_legendary"]
    }

    evolved_pokemon = {
        "name": evo_name,
        "number": data["evo_number"],
        "pokedex_number": data["evo_pokedex_number"],
        "primary_type": data["evo_primary_type"],
        "secondary_type": data["evo_secondary_type"],
        "size": data["evo_size"],
        "is_legendary": data["evo_is_legendary"]
    }

    # =====================================================
    # QUANTITY CHECK
    # =====================================================

    if user_quantity < required_quantity:
        return {
            "status": "error",
            "error_code": "INSUFFICIENT_QUANTITY",
            "result_type": None,
            "messages": {
                "start": None,
                "complete": None,
                "error_message": f"Huh? @$username's {base_name} cannot evolve! Make sure you have enough {base_name} by using !pokedex pokemonname."
            },
            "sound_url": FAILURE_SOUND,
            "base_pokemon": base_pokemon,
            "evolved_pokemon": evolved_pokemon,
            "special_identifiers": None,
            "requirement_data": None,
            "rendered_html_start": None,
            "rendered_html_complete": None
        }

    # =====================================================
    # REQUIREMENT CHECKS
    # =====================================================

    if requirement_type == "trade":
        return {
            "status": "error",
            "error_code": "REQUIREMENT_TRADE",
            "result_type": None,
            "messages": {
                "start": None,
                "complete": None,
                "error_message": f"Huh? @$username's {base_name} can only evolve through trade. Use !trade to exchange 3 {base_name} with another user."
            },
            "sound_url": FAILURE_SOUND,
            "base_pokemon": base_pokemon,
            "evolved_pokemon": evolved_pokemon,
            "special_identifiers": None,
            "requirement_data": None,
            "rendered_html_start": None,
            "rendered_html_complete": None
        }

    if requirement_type == "friendship":

        inventory_identifier = f"$userpokefriendship{evolutionline}"

        if user_friendship < FRIENDSHIP_REQUIRED:
            return {
                "status": "error",
                "error_code": "REQUIREMENT_FRIENDSHIP_NOT_ENOUGH",
                "result_type": None,
                "messages": {
                    "start": None,
                    "complete": None,
                    "error_message": f"Huh? @$username's {base_name} cannot evolve! Deepen your bond by spending time with them using !buddy."
                },
                "sound_url": FAILURE_SOUND,
                "base_pokemon": base_pokemon,
                "evolved_pokemon": evolved_pokemon,
                "special_identifiers": None,
                "requirement_data": None,
                "rendered_html_start": None,
                "rendered_html_complete": None
            }

        result_type = "friendship"
        start_msg = f"What? @$username's {base_name} is evolving! Your friendship is strong enough."

    elif requirement_type == "item":

        inventory_identifier = f"$userpokebag{itemsp}"

        if user_item_quantity < 1:
            return {
                "status": "error",
                "error_code": "ITEM_REQUIRED_BUT_MISSING",
                "result_type": None,
                "messages": {
                    "start": None,
                    "complete": None,
                    "error_message": f"Huh? @$username's {base_name} cannot evolve! A {requirement_display_name} is required."
                },
                "sound_url": FAILURE_SOUND,
                "base_pokemon": base_pokemon,
                "evolved_pokemon": evolved_pokemon,
                "special_identifiers": None,
                "requirement_data": None,
                "rendered_html_start": None,
                "rendered_html_complete": None
            }

        result_type = "item"
        start_msg = f"What? @$username's {base_name} is evolving with a {requirement_display_name}!"

    else:
        result_type = "normal"
        start_msg = f"What? @$username's {base_name} is evolving!"

    # =====================================================
    # SUCCESS
    # =====================================================

    display_username = data["display_username"]
    complete_msg = f"Congratulations! @$username's {base_name} evolved into {evo_name}!"

    html_start = render_spawn_card(
        base_name,
        data["base_number"],
        data["base_pokedex_number"],
        data["base_primary_type"],
        data["base_secondary_type"],
        data["base_size"],
        data["base_is_legendary"],
        evolving=True,
        flash_mode="animate",
        display_username=display_username
    )

    html_complete = render_spawn_card(
        evo_name,
        data["evo_number"],
        data["evo_pokedex_number"],
        data["evo_primary_type"],
        data["evo_secondary_type"],
        data["evo_size"],
        data["evo_is_legendary"],
        evolving=False,
        flash_mode="fadeout",
        display_username=display_username
    )

    return {
        "status": "success",
        "error_code": None,
        "result_type": result_type,
        "messages": {
            "start": start_msg,
            "complete": complete_msg,
            "error_message": None
        },
        "sound_url": SUCCESS_SOUND,
        "base_pokemon": base_pokemon,
        "evolved_pokemon": evolved_pokemon,
        "special_identifiers": {
            "basepokemonsp": data["basepokemonsp"],
            "evolutionsp": data["evolutionsp"],
            "inventory_identifier": inventory_identifier,
            "itemsp": itemsp,
            "evolutionline": evolutionline
        },
        "requirement_data": {
            "requirement_type": requirement_type,
            "requirement_display_name": requirement_display_name,
            "required_pokemon_quantity": required_quantity,
            "user_pokemon_quantity": user_quantity,
            "required_friendship": FRIENDSHIP_REQUIRED if requirement_type == "friendship" else None,
            "user_friendship": user_friendship if requirement_type == "friendship" else None,
            "user_item_quantity": user_item_quantity if requirement_type == "item" else None
        },
        "rendered_html_start": html_start,
        "rendered_html_complete": html_complete
    }


print(json.dumps(run()))