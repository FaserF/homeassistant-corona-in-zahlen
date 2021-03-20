"""The rki_corona_stats component."""

from datetime import timedelta
import logging
import re

import async_timeout
import asyncio
import bs4

from .CoronaParser import CoronaParser

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, OPTION_TOTAL
#from .config_flow import county
DISTRICT = "LK Ebersberg"

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

HYPHEN_PATTERN = re.compile(r"- (.)")

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the rki_corona_stats component."""
    # Make sure coordinator is initialized.
    coordinator = await get_coordinator(hass)

    async def handle_refresh(call):
        _LOGGER.info("Refreshing rki_corona_stats data...")
        await coordinator.async_refresh()
    
    hass.services.async_register(DOMAIN, "refresh", handle_refresh)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up rki_corona_stats from a config entry."""

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    return unload_ok


async def get_coordinator(hass):
    """Get the data update coordinator."""
    if DOMAIN in hass.data:
        return hass.data[DOMAIN]

    async def async_get_data():
        coronaParser = CoronaParser()
        data = coronaParser.get_value(DISTRICT)
        
        result = dict()

        if data is None:
            _LOGGER.exception("Could not process district {}".format(DISTRICT))
            return result

        result[DISTRICT] = dict(
                cases = data["cases"],
                deaths = data["deaths"],
                incidence = round(int(data["cases7_per_100k"]), 3)
                )
        
        return result

    hass.data[DOMAIN] = DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name=DOMAIN,
        update_method=async_get_data,
        update_interval=timedelta(hours=6),
    )
    await hass.data[DOMAIN].async_refresh()
    return hass.data[DOMAIN]


def parse_num(s, t=int):
    if len(s) and s != "-":
        return t(s.replace(".", "").replace(",", "."))
    return 0

def sanitize_county(county):
    """
    Sanitizes the county.

    The ministry sadly does some horrid stuff to their HTML
    and has implemented hyphenation manually, leading to
    some county names now being split in weird ways after
    extraction.

    The following replacements takes place:

      * "- <upper case letter>" -> "-<upper case letter>"
      * "- <lower case letter>" -> "<lower case letter>"
    
    Examples:

        >>> sanitize_county("LK Main-Kinzig- Kreis")
        <<< "LK Main-Kinzig-Kreis"
        >>> sanitize_county("LK Wetterau- kreis")
        <<< "LK Wetteraukreis"
        >>> sanitize_county("SK Frankfurt am Main")
        <<< "SK Frankfurt am Main"
    """

    def replace(m):
        letter = m.group(1)
        if letter.islower():
            return letter
        else:
            return "-{}".format(letter)

    return HYPHEN_PATTERN.sub(replace, county)

