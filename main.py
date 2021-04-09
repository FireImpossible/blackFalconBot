from bot import *

INFO_DISPLAY_ENABLED = True
EVENTS_ENABLED = True
HELP_ENABLED = True
LEADERSHIP_ENABLED = True
MISCELLANEOUS_ENABLED = True

if INFO_DISPLAY_ENABLED:
    from info_display import *

if EVENTS_ENABLED:
    from events import *

if HELP_ENABLED:
    from help import *

if LEADERSHIP_ENABLED:
    from leadership import *

if MISCELLANEOUS_ENABLED:
    from miscellaneous import *


client.run(TOKEN)
