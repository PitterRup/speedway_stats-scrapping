from collections import namedtuple

TeamCompositionRider = namedtuple("TeamCompositionRider", ["number", "name"])


Heat = namedtuple(
    "Heat", [
        "number", "winner_time", "rider_a", "rider_b", "rider_c", "rider_d", "finished"
    ]
)


InterpretedHeat = namedtuple(
    "InterpretedHeat",
    list(Heat._fields)
)


HeatRider = namedtuple(
    "HeatRider", ["name", "replaced_rider_name", "score", "helmet_color", "warning", "defect", "fall", "exclusion"]
)


InterpretedHeatRider = namedtuple(
    "InterpretedHeatRider",
    list(HeatRider._fields) + [
        'number',
        'team',
    ]
)


TeamRider = namedtuple(
    "TeamRider", [
        "firstname",
        "surname",
        "birthdate",
        "country",
    ]
)
