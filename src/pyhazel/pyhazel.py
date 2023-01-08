from .application import Application
from .debug.instrumentor import *


def pyhazel(app_factory: type[Application]):
    HZ_PROFILE_BEGIN_SESSION("Startup", "HazelProfile-Startup.json")
    app = app_factory()
    HZ_PROFILE_END_SESSION()

    HZ_PROFILE_BEGIN_SESSION("Runtime", "HazelProfile-Runtime.json")
    app.run()
    HZ_PROFILE_END_SESSION()

    HZ_PROFILE_BEGIN_SESSION("Shutdown", "HazelProfile-Shutdown.json")
    app.destroy()
    HZ_PROFILE_END_SESSION()
