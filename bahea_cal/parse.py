import collections
import json
import re

import requests

collections.Callable = collections.abc.Callable  # noqa: E401

from bs4 import BeautifulSoup


class Team:
    def __init__(self, **kwargs):
        self.__typename = kwargs.pop("__typename")
        self.badgePng = kwargs.pop("badgePng")
        self.badgeSvg = kwargs.pop("badgeSvg")
        self.id = kwargs.pop("id")
        self.popularName = kwargs.pop("popularName")

    def __str__(self):
        return f"{self.popularName}"


class Championship:
    def __init__(self, **kwargs):
        self.__typename = kwargs.pop("__typename")
        self.name = kwargs.pop("name")

    def __str__(self):
        return f"{self.name}"


class MatchLocation:
    def __init__(self, **kwargs):
        self.__typename = kwargs.pop("__typename")
        self.name = kwargs.pop("name")
        self.popularName = kwargs.pop("popularName")

    def __str__(self):
        return f"{self.popularName}"


class Phase:
    def __init__(self, **kwargs):
        self.__typename = kwargs.pop("__typename")
        self.name = kwargs.pop("name")
        self.type = kwargs.pop("type")


class Scoreboard:
    def __init__(self, **kwargs):
        self.__typename = kwargs.pop("__typename")
        self.away = kwargs.pop("away")
        self.home = kwargs.pop("home")
        self.penalty = kwargs.pop("penalty")


class TRTransmission:
    def __init__(self, **kwargs):
        self.__typename = kwargs.pop("__typename")
        self.broadcastStatus = kwargs.pop("broadcastStatus")
        self.featuredVideo = kwargs.pop("featuredVideo")
        self.id = kwargs.pop("id")
        self.period = kwargs.pop("period")
        self.url = kwargs.pop("url")


class BroadcastStatus:
    def __init__(self, **kwargs):
        self.__typename = kwargs.pop("__typename")
        self.id = kwargs.pop("id")
        self.label = kwargs.pop("label")


class Period:
    def __init__(self, **kwargs):
        self.__typename = kwargs.pop("__typename")
        self.id = kwargs.pop("id")
        self.label = kwargs.pop("label")


class Match:
    def __init__(self, **kwargs):
        self.__typename = kwargs.pop("__typename")
        self.awayTeam = kwargs.pop("awayTeam")
        self.championship = kwargs.pop("championship")
        self.homeTeam = kwargs.pop("homeTeam")
        self.liveWatchSources = kwargs.pop("liveWatchSources")
        self.location = kwargs.pop("location")
        self.phase = kwargs.pop("phase")
        self.round = kwargs.pop("round")
        self.scoreboard = kwargs.pop("scoreboard")
        self.startDate = kwargs.pop("startDate")
        self.startHour = kwargs.pop("startHour")
        self.transmission = kwargs.pop("transmission")
        self.winner = kwargs.pop("winner")


class SoccerEvent:
    def __init__(self, **kwargs):
        self.match = kwargs.pop("match")


def instantiate_from_json(data):
    if isinstance(data, dict):
        typename = data.get("__typename")
        if typename == "Team":
            return Team(**data)
        elif typename == "Championship":
            return Championship(**data)
        elif typename == "MatchLocation":
            return MatchLocation(**data)
        elif typename == "Phase":
            return Phase(**data)
        elif typename == "Scoreboard":
            return Scoreboard(**data)
        elif typename == "TRTransmission":
            broadcastStatus = instantiate_from_json(data.pop("broadcastStatus"))
            period = instantiate_from_json(data.pop("period"))
            return TRTransmission(broadcastStatus=broadcastStatus, period=period, **data)
        elif typename == "BroadcastStatus":
            return BroadcastStatus(**data)
        elif typename == "Period":
            return Period(**data)
        elif typename == "Match":
            awayTeam = instantiate_from_json(data.pop("awayTeam"))
            championship = instantiate_from_json(data.pop("championship"))
            homeTeam = instantiate_from_json(data.pop("homeTeam"))
            location = instantiate_from_json(data.pop("location"))
            phase = instantiate_from_json(data.pop("phase"))
            scoreboard = instantiate_from_json(data.pop("scoreboard"))
            transmission = instantiate_from_json(data["transmission"]) if data["transmission"] else None
            data.pop("transmission")
            return Match(
                awayTeam=awayTeam,
                championship=championship,
                homeTeam=homeTeam,
                location=location,
                phase=phase,
                scoreboard=scoreboard,
                transmission=transmission,
                **data,
            )
        elif typename == "SoccerEvent":
            match = instantiate_from_json(data.pop("match"))
            return SoccerEvent(match=match)
    elif isinstance(data, list):
        return [instantiate_from_json(item) for item in data]
    return data


def parse():
    url = "https://ge.globo.com/ba/futebol/times/bahia/agenda-de-jogos-do-bahia/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    pattern = re.compile(r"window\.dataSportsSchedule = (\{.*?\});", re.DOTALL)

    js_object_str = ""
    for script in soup.find_all("script"):
        if script.string and pattern.search(script.string):
            js_object_str = pattern.search(script.string).group(1)
            break

    if js_object_str:
        js_object_str = js_object_str.replace("CHAMPIONSHIPS", '"CHAMPIONSHIPS"')
        js_object_str = js_object_str.replace("MULTISPORT", '"MULTISPORT"')
        js_object_str = js_object_str.replace("SCHEDULE_TEAM", '"SCHEDULE_TEAM"')
        js_object_str = js_object_str.replace("INFO_TEAM", '"INFO_TEAM"')

        try:
            parsed_data = json.loads(js_object_str)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        else:
            # past_events = instantiate_from_json(parsed_data["SCHEDULE_TEAM"]["teamAgenda"]["past"])
            past_events = []
            current_events = instantiate_from_json(parsed_data["SCHEDULE_TEAM"]["teamAgenda"]["now"])
            future_events = instantiate_from_json(parsed_data["SCHEDULE_TEAM"]["teamAgenda"]["future"])
            return past_events + current_events + future_events
    else:
        print("JavaScript object not found in the HTML content")
