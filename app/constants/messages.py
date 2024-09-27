def non_existing_slot(slot_type) -> str:
    return f"L'emplacement {slot_type.value} n'existe pas."


def non_compatible_slot(slot_type) -> str:
    return f"L'objet n'est pas compatible avec l'emplacement {slot_type.value}."


def nothing_equipped(slot_type) -> str:
    return f"Rien n'est équipé dans l'emplacement {slot_type.value}."


def not_enough_stat(stat) -> str:
    return f"Vous n'avez pas assez de {stat} pour utiliser cet item."


def empty_consumable(name):
    return f"Vous n'avez plus de {name}."
