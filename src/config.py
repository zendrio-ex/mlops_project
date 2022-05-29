# unused
from dynaconf import Dynaconf

settings = Dynaconf(
    environments=True,
    load_dotenv=True,
    envvar_prefix="DYNACONF",
    settings_files=['settings.json', 'settings.local.json'],
)
