
import plistlib

# from pyatv.protocols.airplay

from openairplay.rtsp_client import RTSPClient


client = RTSPClient("rtsp://localhost:37126")

client._connect_socket()
r = client._make_request(
    "GET", "/info",
    headers={
        "X-Apple-ProtocolVersion": 0,
    },
)

info = plistlib.loads(r.content)
print(f"Got server information: {info}")
