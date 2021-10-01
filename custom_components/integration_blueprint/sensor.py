"""Sensor platform for TpLink_Cloud."""
from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .entity import TpLink_Cloud


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([IntegrationBlueprintSensor(coordinator, entry)])


class IntegrationBlueprintSensor(TpLink_Cloud):
    """TpLink_Cloud Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("body")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON
