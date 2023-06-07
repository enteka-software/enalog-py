from typing import Dict, Union
from os import environ
import requests
from requests.exceptions import HTTPError, RequestException


class MissingRequiredData(Exception):
    """Thrown when required keys are missing from the data object"""

    pass


def push_event(api_token: str, event: Dict) -> Dict:
    required_keys = ("project", "name", "push")
    if not all(key in event for key in required_keys):
        missing_keys = set(required_keys) - event.keys()

        missing_keys_res = ""

        last_items = list(missing_keys)[-1]

        for miss in missing_keys:
            if miss == last_items:
                missing_keys_res += f"{miss}"
            else:
                missing_keys_res += f"{miss}, "

        raise MissingRequiredData(
            f"The {missing_keys_res} key(s) are missing from the event data"
        )

    try:
        res = requests.post(
            "https://api.enalog.app/v1/events",
            json=event,
            headers={"Authorization": f"Bearer {api_token}"},
        )

        res.raise_for_status()

        if res.status_code == 200:
            return {"status_code": 200, "message": "Event succesfully sent to EnaLog"}
    except requests.exceptions.HTTPError as ex:
        return {"status_code": ex.response.status_code, "message": ex.response.text}
    except requests.exceptions.RequestException as ex:
        return {"status_code": "500", "message": "Internal server error"}


class EnaLog:
    def __init__(self, api_token: Union[str, None] = None) -> None:
        if api_token is not None:
            self.api_token = api_token
        else:
            self.api_token = environ.get("ENALOG_API_TOKEN", "")

    def push_event(self, event: Dict) -> Dict:
        required_keys = ("project", "name", "push")
        if not all(key in event for key in required_keys):
            missing_keys = set(required_keys) - event.keys()

            missing_keys_res = ""

            last_items = list(missing_keys)[-1]

            for miss in missing_keys:
                if miss == last_items:
                    missing_keys_res += f"{miss}"
                else:
                    missing_keys_res += f"{miss}, "

            raise MissingRequiredData(
                f"The {missing_keys_res} key(s) are missing from the event data"
            )

        try:
            res = requests.post(
                "https://api.enalog.app/v1/events",
                json=event,
                headers={"Authorization": f"Bearer {self.api_token}"},
            )

            res.raise_for_status()

            if res.status_code == 200:
                return {
                    "status_code": 200,
                    "message": "Event succesfully sent to EnaLog",
                }
        except requests.exceptions.HTTPError as ex:
            raise HTTPError(ex)
        except requests.exceptions.RequestException as ex:
            raise RequestException(ex)

    def check_feature(self, feature: str, user_id: str) -> Union[bool, str]:
        try:
            res = requests.post(
                "https://api.enalog.app/v1/feature-flags",
                json={"name": feature, "user_id": user_id},
                headers={"Authorization": f"Bearer {self.api_token}"},
            )

            res.raise_for_status()

            if res.status_code == 200:
                data = res.json()

                if data["flag_type"] == "Boolean":
                    if data["variant"] == "a-variant":
                        return True
                    else:
                        return False
        except requests.exceptions.HTTPError as ex:
            raise HTTPError(ex)
        except requests.exceptions.RequestException as ex:
            raise RequestException(ex)
