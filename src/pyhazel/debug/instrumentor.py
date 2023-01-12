from typing import Callable, Optional
import time
from pyhazel.config import *
from dataclasses import dataclass
from io import TextIOWrapper
from functools import wraps
from threading import Lock
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
        self.mutex = Lock()

    @classmethod
    def get(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def begin_session(self, name: str, filepath: str = "results.json"):
        with self.mutex:
            if self.current_session is not None:
                # If there is already a current session, then close it before beginning new one.
                # Subsequent profiling output meant for the original session will end up in the
                # newly opened session instead.  That's better than having badly formatted
                # profiling output.
                print(
                    f"Instrumentor::BeginSession('{name}') when session '{self.current_session.name}' already open.")
            else:
                self.fp = open(filepath, "w")
                self.current_session = InstrumentationSession(name)
                self.write_header()

    def end_session(self):
        with self.mutex:
            self.__internal_end_session()

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

        with self.mutex:
            if self.current_session is not None:
                self.output["traceEvents"].append(event)

    def write_header(self):
        self.output = {"otherData": {}, "traceEvents": []}

    def write_footer(self):
        json.dump(self.output, self.fp)

    def __internal_end_session(self):
        if self.current_session is not None:
            self.write_footer()
            self.fp.close()
            self.current_session = None
            self.output = {}


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


class NullInstrumentationTimer:
    def __init__(self) -> None:
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
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
    if INSTRUMENTATION_ENABLED:
        return InstrumentationTimer(name)
    else:
        return NullInstrumentationTimer()


def HZ_PROFILE_FUNCTION(func: Callable):
    @wraps(func)
    def profiler(*args, **kwargs):
        if INSTRUMENTATION_ENABLED:
            with InstrumentationTimer(func.__qualname__):
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return profiler
