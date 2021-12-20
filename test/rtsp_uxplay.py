
from openairplay.rtsp_client import RTSPClient


client = RTSPClient("rtsp://localhost:37126")

client._connect_socket()
print(client._make_request(
    "GET", "/info",
    headers={
        "X-Apple-ProtocolVersion": 0,
    },
))
