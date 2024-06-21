from enum import Enum


class TimeInterval(Enum):
    five_secs = '5 secs'


class SetupStatus(Enum):
    active = 'Active'
    disabled = 'Disabled'