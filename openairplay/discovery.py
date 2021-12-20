#!/usr/bin/env python3

import sys
import asyncio

import zeroconf
import zeroconf.asyncio
from zeroconf.asyncio import AsyncServiceInfo
from zeroconf import ServiceStateChange
from PyQt5.QtCore import QObject, pyqtSignal

from . import log, utils
from .receiver_device import AirplayReceiver, AirplayFeatures


# global airplayReceivers
# airplayReceivers = []
#
# global discoveryStarted
# discoveryStarted = False

# global DEBUG
# DEBUG = True

# browser = None

class AirplayServiceListener(QObject):
    receiver_added = pyqtSignal([AirplayReceiver])
    receiver_removed = pyqtSignal([AirplayReceiver])

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        super().__init__()

    def start(self):
        self.ZC = zeroconf.asyncio.AsyncZeroconf()
        self.browser = zeroconf.asyncio.AsyncServiceBrowser(
            self.ZC.zeroconf,
            "_airplay._tcp.local.",
            # self,
            handlers=[self.async_on_service_state_change],
        )
        self.devices = {}

    def async_on_service_state_change(
            self,
            zeroconf: zeroconf.Zeroconf,
            service_type: str,
            name: str,
            state_change: ServiceStateChange,
        ):
        log.debug(f"Service {name} changed state: {state_change}")
        task = asyncio.ensure_future(self.on_service_state_change(
            zeroconf, service_type, name, state_change))
        # task.result()

    async def on_service_state_change(self, zc, service_type, name, change):
        # log.debug(f"in async: state change handler")
        if change == ServiceStateChange.Added:
            await self.add_service(zc, service_type, name)
        elif change == ServiceStateChange.Updated:
            await self.update_service(zc, service_type, name)
        elif change == ServiceStateChange.Removed:
            await self.remove_service(zc, service_type, name)
        return None

    async def remove_service(self, zeroconf, service_type, name):
        # airplayReceivers.remove(name)
        if name not in self.devices:
            log.warn(f"Device '{name}' not known, cannot remove service.")
            return
        log.debug(f"Airplay receiver '{name}' removed")
        self.receiver_removed.emit(self.devices[name])
        self.devices[name] = None # permit other references to persist

    async def add_service(self, zeroconf, service_type, name):
        log.debug(f"Adding device '{name}' of type {service_type} ...")
        # info = zeroconf.get_service_info(type, name)
        info = AsyncServiceInfo(service_type, name)
        discovered = await info.async_request(zeroconf, 5000)
        if not discovered:
            log.warn(f"{name} did not respond to a discovery request in time")
        # airplayReceivers.append(name)
        self.devices[name] = AirplayReceiver(
            name, info, loop=self.loop,
        )
        log.debug(f"Airplay receiver '{name}' added, constructed: {self.devices[name]}")
        self.receiver_added.emit(self.devices[name])

        log.debug(f"Receiver addresses: {self.devices[name]._get_ip_addresses()}")

    async def update_service(self, zeroconf, type, name):
        # info = zeroconf.get_service_info(type, name)
        info = AsyncServiceInfo(type, name)
        await info.async_request(zeroconf, 5000)
        if name not in self.devices:
            log.warn(f"Device '{name}' not known, cannot update service.")
            return
        self.devices[name].update_service_info(info)
        log.debug(f"Airplay receiver '{name}' service updated: {self.devices[name]}")

    async def quit(self):
        await self.browser.async_cancel()
        await self.ZC.async_close()
        log.debug("Closed ZC browser")
