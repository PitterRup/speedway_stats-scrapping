from collections import namedtuple


TeamCompositionRider = namedtuple('TeamCompositionRider', [
    'number',
    'name',
])


Heat = namedtuple('Heat', [
    'number',
    'winner_time',
    'rider_a',
    'rider_b',
    'rider_c',
    'rider_d',
])


HeatRider = namedtuple('HeatRider', [
    'warning',
    'name',
    'replaced_rider_name',
    'score',
])
