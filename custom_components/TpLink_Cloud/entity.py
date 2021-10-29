"""BlueprintEntity class"""
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, NAME, VERSION, ATTRIBUTION

class TpLink_CloudEntity(Entity):

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.device

    @property
    def device_info(self):
        mydevice = self.client.sync_rtn_device(self.device)
        return {
            "identifiers": {(DOMAIN, self.device)},
            "name": mydevice["alias"],
            "model": mydevice["deviceModel"],
            "sw_version": mydevice["fwVer"],
            "manufacturer": NAME,
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }
