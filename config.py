
# Pip imports
from dynaconf import Dynaconf


djsettings = Dynaconf(
    envvar_prefix="DJANGO",
    settings_files=['settings.env', '.secrets.env'],
    load_dotenv=True,
)
