from typing import Callable, Optional
import time
from pyhazel.config import *
from dataclasses import dataclass
from io import TextIOWrapper
from functools import wraps
import time
import json

__all__ = [
    "HZ_PROFILE_BEGIN_SESSION",
    "HZ_PROFILE_END_SESSION",
    "HZ_PROFILE_SCOPE",
    "HZ_PROFILE_FUNCTION"
]

NANO_TO_MICRO_SECONDS_SCALE_FACTOR = 0.001


@dataclass
class ProfileResult:
    name: str
    start: int
    end: int
    thread_id: int


@dataclass
class InstrumentationSession:
    name: str


class Instrumentor:
    __instance = None

    def __init__(self) -> None:
        self.current_session: Optional[InstrumentationSession] = None
        self.fp: TextIOWrapper = None
        self.output: dict = {}
        self.profile_count: int = 0

    @classmethod
    def get(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def begin_session(self, name: str, filepath: str = "results.json"):
        self.fp = open(filepath, "w")
        self.write_header()
        self.current_session = InstrumentationSession(name)

    def end_session(self):
        self.write_footer()
        self.fp.close()
        self.current_session = None
        self.output = {}
        self.profile_count = 0

    def write_profile(self, result: ProfileResult):
        event = {
            "cat": "function",
            "dur": (result.end - result.start),
            "name": result.name,
            "ph": "X",
            "pid": 0,
            "tid": result.thread_id,
            "ts": result.start
        }
        self.output["traceEvents"].append(event)

    def write_header(self):
        self.output = {"otherData": {}, "traceEvents": []}

    def write_footer(self):
        json.dump(self.output, self.fp)


class InstrumentationTimer:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.start_time = time.perf_counter_ns() * NANO_TO_MICRO_SECONDS_SCALE_FACTOR

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        Instrumentor.get().write_profile(
            ProfileResult(
                name=self.name,
                start=self.start_time,
                end=time.perf_counter_ns() * NANO_TO_MICRO_SECONDS_SCALE_FACTOR,
                thread_id=0
            )
        )
        return True


# ==========
# Client API
# ==========
def HZ_PROFILE_BEGIN_SESSION(name: str, filepath: str):
    if not INSTRUMENTATION_ENABLED:
        return

    Instrumentor.get().begin_session(name, filepath)


def HZ_PROFILE_END_SESSION():
    if not INSTRUMENTATION_ENABLED:
        return

    Instrumentor.get().end_session()


def HZ_PROFILE_SCOPE(name: str):
    if not INSTRUMENTATION_ENABLED:
        return

    return InstrumentationTimer(name)


def HZ_PROFILE_FUNCTION(func: Callable):
    if not INSTRUMENTATION_ENABLED:
        return

    @wraps(func)
    def profiler(*args, **kwargs):
        with InstrumentationTimer(func.__qualname__):
            func(*args, **kwargs)

    return profiler
