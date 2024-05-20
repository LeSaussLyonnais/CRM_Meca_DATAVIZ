from enum import Enum


class TimeInterval(Enum):
    five_secs = '5 secs'
    ten_secs = '10 secs'
    thirty_secs = '30 secs'
    one_min = '1 min'
    five_mins = '5 mins'
    one_hour = '1 hour'


class SetupStatus(Enum):
    active = 'Active'
    disabled = 'Disabled'