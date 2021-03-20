"""Config flow for rki_corona_stats integration."""
import logging
import CoronaParser from CoronaParser

import voluptuous as vol

from homeassistant import config_entries

from . import get_coordinator
from .const import DOMAIN, OPTION_TOTAL

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for rki_corona_stats."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    district = data[district]
    _LOGGER.debug(
        "validate_input:: DISTRICT: {}".format(district)
    )


    unique_id = district.lower()
    await self.async_set_unique_id(unique_id)
    self._abort_if_unique_id_configured()
    return self.async_create_entry(
        title="XYZ", data=user_input
    )



    _options = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        if user_input is not None:
            values = await validate_input(self.hass, user_input)
            if values is None:
                errors["base"] = "See logger execption"


        if self._options is None:
            self._options = {OPTION_TOTAL: "doNotSelect"}
            coordinator = await get_coordinator(self.hass)
            for county in sorted(coordinator.data.keys()):
                if county == OPTION_TOTAL:
                    continue
                self._options[county] = county

        if user_input is not None:
            await self.async_set_unique_id(user_input["county"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=self._options[user_input["county"]], data=user_input
            )

        _LOGGER.debug("Showing config form, options is {!r}".format(self._options))
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("county"): vol.In(self._options)
            }),
        )

    data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_DISTRICT, default="SK München"
                ): str,
            },
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input
    See if the given district can be resolved
    """
    district = data[district]
    _LOGGER.debug(
        "validate_input:: DISTRICT: {}".format(district)
    )

    coronaParser = CoronaParser()
    values = coronaParser.get_values(district)

    if values is None:
        if "(" in district and ")" in district or district == "Oldenburg" or "Mülheim" in district or "Aachen" in district or 'Landau' in district or "Ludwigshafen" in district or "Weinstraße" in district:
                _LOGGER.exception(f"API does not provide information about district {district}, please use an alternative")
                return None
        
        if "Berlin" in result:
            newDistrict = "SK Berlin {district}"
            values = coronaParser.get_values(newDistrict)
            if values is None:
                _LOGGER.exception(f"For Berlin you have to use the format 'SK Berlin <district>'. Couldn't find data for {district} and {newDistrict}")
                return None
        
        if "Offenbach" in result:
            if values is None:
                _LOGGER.exception(f"For Offenbach please use 'LK Offenbach'. Couldn't find data for {district}")
                return None

        _LOGGER.exception(f"Couldn't find data for {district}. Please use schmea 'LK <district>' or 'SK <district>'")
        return None

    return values

    
        
 
                




