from enalog import push_event, MissingRequiredData
import pytest

import requests
import requests_mock


def test_push_event_returns_missing_project_key_when_required_project_key_is_not_provided():
    with requests_mock.Mocker() as m:
        m.post("https://api.enalog.app/v1/events")

        api_token = "12345"
        event = {"name": "enalog", "push": True}

        with pytest.raises(MissingRequiredData) as e_info:
            res = push_event(api_token=api_token, event=event)

            assert e_info.message == "The project key(s) are missing from the event data"


def test_push_event_returns_missing_name_key_when_required_name_key_is_not_provided():
    with requests_mock.Mocker() as m:
        m.post("https://api.enalog.app/v1/events")

        api_token = "12345"
        event = {"project": "enalog", "push": True}

        with pytest.raises(MissingRequiredData) as e_info:
            res = push_event(api_token=api_token, event=event)

            assert e_info.message == "The name key(s) are missing from the event data"

def test_push_event_returns_missing_push_key_when_required_push_key_is_not_provided():
    with requests_mock.Mocker() as m:
        m.post("https://api.enalog.app/v1/events")

        api_token = "12345"
        event = {"project": "enalog", "name": "user-subscribed"}

        with pytest.raises(MissingRequiredData) as e_info:
            res = push_event(api_token=api_token, event=event)

            assert e_info.message == "The push key(s) are missing from the event data"



def test_push_event_returns_missing_keys_when_required_multiple_keys_is_not_provided():
    with requests_mock.Mocker() as m:
        m.post("https://api.enalog.app/v1/events")

        api_token = "12345"
        event = {"project": "enalog"}

        with pytest.raises(MissingRequiredData) as e_info:
            res = push_event(api_token=api_token, event=event)
            
            assert e_info.message == "The name, push key(s) are missing from the event data"


def test_push_event_returns_200_response_if_event_is_successful():
    with requests_mock.Mocker() as m:
        m.post("https://api.enalog.app/v1/events")

        api_token = "12345"
        event = {"project": "12345", "name": "enalog", "push": True}

        res = push_event(api_token=api_token, event=event)

        assert len(res) == 2

        assert "status_code" in res
        assert res["status_code"] == 200

        assert "message" in res
        assert res["message"] == "Event succesfully sent to EnaLog"


def test_push_event_returns_401_response_if_event_is_unauthenticated():
    with requests_mock.Mocker() as m:
        mocked_res = requests.Response()
        mocked_res.status_code = 401

        m.post(
            "https://api.enalog.app/v1/events",
            exc=requests.exceptions.HTTPError(response=mocked_res),
        )

        api_token = "12345"
        event = {"project": "12345", "name": "enalog", "push": True}

        res = push_event(api_token=api_token, event=event)

        assert len(res) == 2
        assert "status_code" in res
        assert res["status_code"] == 401
        assert "message" in res


def test_push_event_returns_404_response_if_event_is_unauthenticated():
    with requests_mock.Mocker() as m:
        mocked_res = requests.Response()
        mocked_res.status_code = 404

        m.post(
            "https://api.enalog.app/v1/events",
            exc=requests.exceptions.HTTPError(response=mocked_res),
        )

        api_token = "12345"
        event = {"project": "12345", "name": "enalog", "push": True}

        res = push_event(api_token=api_token, event=event)

        assert len(res) == 2
        assert "status_code" in res
        assert res["status_code"] == 404
        assert "message" in res
