# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

import requests
import json

from api_app.exceptions import AnalyzerRunException
from api_app.analyzers_manager import classes

from tests.mock_utils import if_mock_connections, patch, MockResponse


class ThreatFox(classes.ObservableAnalyzer):
    base_url: str = "https://threatfox-api.abuse.ch/api/v1/"

    def run(self):
        payload = {"query": "search_ioc", "search_term": self.observable_name}

        try:
            response = requests.post(self.base_url, data=json.dumps(payload))
            response.raise_for_status()
        except requests.RequestException as e:
            raise AnalyzerRunException(e)

        result = response.json()
        return result

    @classmethod
    def _monkeypatch(cls):
        patches = [
            if_mock_connections(
                patch(
                    "requests.post",
                    return_value=MockResponse({}, 200),
                ),
            )
        ]
        return super()._monkeypatch(patches=patches)
