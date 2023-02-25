from typing import Dict
import requests


def push_event(api_token: str, event: Dict) -> Dict:
    required_keys = ("project", "name", "push")
    if not all(key in event for key in required_keys):
        missing_keys = set(required_keys) - event.keys()
        
        missing_keys_res = {}
        
        for miss in missing_keys:
            missing_keys_res[miss] = f"{miss} key is missing from your event data"

        return missing_keys_res

    try:
        res = requests.post(
            "https://api.enalog.app/v1/events",
            data=event,
            headers={"Authorization": f"Bearer: {api_token}"},
        )

        if res.status_code == 200:
            return {"status_code": 200, "message": "Event succesfully sent to EnaLog"}
    except requests.exceptions.RequestException as ex:
        return {"status_code": ex.response.status_code, "message": ex.response.text}
