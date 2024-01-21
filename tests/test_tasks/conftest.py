from typing import Iterator
from unittest.mock import patch

import pytest

BUILDS_FILE_CONTENT = """
builds:
- name: forward_interest
  tasks:
  - build_teal_leprechauns
  - coloring_aqua_centaurs
  - coloring_navy_golems
- name: reach_wind
  tasks:
  - bring_maroon_golems
  - bring_silver_orcs
  - build_blue_gorgons
  - coloring_aqua_golems
- name: repeating_build
- name: repeating_build
"""

TASKS_FILE_CONTENT = """
tasks:
- name: build_teal_leprechauns
  dependencies:
  - build_white_fairies
  - coloring_fuchsia_fairies
- name: coloring_fuchsia_fairies
  dependencies:
  - bring_aqua_humans
- name: bring_aqua_humans
  dependencies:
  - bring_aqua_leprechauns
- name: bring_aqua_leprechauns
  dependencies: []
- name: bring_gray_humans
  dependencies:
  - coloring_gray_humans
  - train_aqua_humans
  - train_fuchsia_humans
- name: bring_black_gnomes
  dependencies: []
- name: bring_black_golems
  dependencies: []
- name: bring_black_humans
  dependencies: []
- name: enable_teal_cyclops
  dependencies:
  - design_blue_cyclops
  - write_aqua_cyclops
- name: enable_teal_gnomes
  dependencies: []
"""


@pytest.fixture
def mock_builds_file_read() -> Iterator[None]:
    with patch("aiofiles.open") as mocker:
        mocker.return_value.__aenter__.return_value.read.return_value = (
            BUILDS_FILE_CONTENT
        )
        yield


@pytest.fixture
def mock_tasks_file_read() -> Iterator[None]:
    with patch("aiofiles.open") as mocker:
        mocker.return_value.__aenter__.return_value.read.return_value = (
            TASKS_FILE_CONTENT
        )
        yield


@pytest.fixture
def tasks_graph() -> dict:
    return {
        "build_teal_leprechauns": {"build_white_fairies", "coloring_fuchsia_fairies"},
        "enable_teal_gnomes": set(),
        "coloring_fuchsia_fairies": {"bring_aqua_humans"},
        "bring_aqua_humans": {"bring_aqua_leprechauns"},
        "bring_aqua_leprechauns": set(),
    }


@pytest.fixture
def tasks_cycle_graph() -> dict:
    return {
        "bring_aqua_humans": {"bring_aqua_leprechauns"},
        "bring_aqua_leprechauns": {"bring_aqua_humans"},
    }
