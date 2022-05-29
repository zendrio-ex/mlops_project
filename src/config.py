# unused
from dynaconf import Dynaconf

settings = Dynaconf(
    environments=True,
    load_dotenv=True,
    envvar_prefix="DYNACONF",
    settings_files=['src/settings.json', 'src/settings.local.json'],
)
