from enum import Enum
from enum import auto


class Platform(Enum):
    HZ_PLATFORM_WINDOWS = auto()


# =========
# Constants
# =========
INSTRUMENTATION_ENABLED = True
DEBUG = True
PLATFORM = Platform.HZ_PLATFORM_WINDOWS
