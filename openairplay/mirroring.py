
import plistlib
import asyncio
from typing import List
from enum import Flag
import ipaddress

import requests
import zeroconf
import pyatv
from pyatv.conf import AppleTV
from pyatv.support.rtsp import RtspSession
from pyatv.protocols.airplay.remote_control import RemoteControl as AirPlayRemoteControl

from . import log
from .utils import SimpleRepr
from .receiver_device import AirplayReceiver

class OpenAirPlayMirroringClient(SimpleRepr):
    def __init__(
            self,
            receiver: AirplayReceiver,
        ):
        self.receiver = receiver

    async def start(self):
        # pairing process
        log.debug(f"setup mirroring session with {self.receiver.name} ...")
        info = self.receiver._get_server_info()
        rc = self.receiver._get_pyatv_rtsp_session()
        # await rc.exchange(
        #     "POST", "/pair-setup",
        #     content_type="application/octet-stream",
        # )
