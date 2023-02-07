from typing import Dict
import requests


def push(api_token: str, event: Dict) -> Dict:
    res = requests.post(
        "https://api.enalog.app/v1/events",
        data=event,
        headers={"Authorization": f"Bearer: {api_token}"},
    )

    if res.status_code == 200:
        return {"status_code": 200, "message": "Event succesfully sent to EnaLog"}
