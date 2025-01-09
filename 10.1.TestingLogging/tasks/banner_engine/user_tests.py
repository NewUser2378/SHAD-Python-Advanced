import random
from typing import List

import pytest

from .banner_engine import (
    BannerStat, Banner, BannerStorage, EpsilonGreedyBannerEngine, EmptyBannerStorageError
)

TEST_DEFAULT_CTR = 0.1


@pytest.fixture(scope="function")
def test_banners() -> List[Banner]:
    return [
        Banner("b1", cost=1, stat=BannerStat(10, 20)),
        Banner("b2", cost=250, stat=BannerStat(20, 20)),
        Banner("b3", cost=100, stat=BannerStat(0, 20)),
        Banner("b4", cost=100, stat=BannerStat(1, 20)),
    ]


@pytest.mark.parametrize("clicks, shows, expected_ctr", [
    (1, 1, 1.0),
    (20, 100, 0.2),
    (5, 100, 0.05),
    (0, 0, TEST_DEFAULT_CTR)
])
def test_banner_stat_ctr_value(clicks: int, shows: int, expected_ctr: float) -> None:
    stat = BannerStat(clicks, shows)
    assert stat.compute_ctr(TEST_DEFAULT_CTR) == expected_ctr


def test_empty_stat_compute_ctr_returns_default_ctr() -> None:
    stat = BannerStat(0, 0)
    assert stat.compute_ctr(TEST_DEFAULT_CTR) == TEST_DEFAULT_CTR


def test_banner_stat_add_show_lowers_ctr() -> None:
    stat = BannerStat(10, 20)
    old_ctr = stat.compute_ctr(TEST_DEFAULT_CTR)
    stat.add_show()
    assert stat.compute_ctr(TEST_DEFAULT_CTR) < old_ctr


def test_banner_stat_add_click_increases_ctr() -> None:
    stat = BannerStat(10, 20)
    old_ctr = stat.compute_ctr(TEST_DEFAULT_CTR)
    stat.add_click()
    assert stat.compute_ctr(TEST_DEFAULT_CTR) > old_ctr


def test_get_banner_with_highest_cpc_returns_banner_with_highest_cpc(test_banners: List[Banner]) -> None:
    storage = BannerStorage(test_banners, default_ctr=TEST_DEFAULT_CTR)
    highest_cpc_banner = storage.banner_with_highest_cpc()
    expected_banner = max(
        test_banners,
        key=lambda b: b.cost * b.stat.compute_ctr(TEST_DEFAULT_CTR)
    )
    assert highest_cpc_banner.banner_id == expected_banner.banner_id


def test_banner_engine_raise_empty_storage_exception_if_constructed_with_empty_storage() -> None:
    with pytest.raises(EmptyBannerStorageError):
        empty_storage = BannerStorage([])
        EpsilonGreedyBannerEngine(empty_storage, random_banner_probability=0.1)


def test_engine_send_click_not_fails_on_unknown_banner(test_banners: List[Banner]) -> None:
    storage = BannerStorage(test_banners)
    engine = EpsilonGreedyBannerEngine(storage, random_banner_probability=0.1)
    try:
        engine.send_click("unknown_banner")
    except Exception:
        pytest.fail("Engine should not fail on unknown banner ID.")


def test_engine_with_zero_random_probability_shows_banner_with_highest_cpc(test_banners: List[Banner]) -> None:
    storage = BannerStorage(test_banners)
    engine = EpsilonGreedyBannerEngine(storage, random_banner_probability=0.0)
    selected_banner_id = engine.show_banner()
    expected_banner = storage.banner_with_highest_cpc()
    assert selected_banner_id == expected_banner.banner_id


@pytest.mark.parametrize("expected_random_banner_id", ["b1", "b2", "b3", "b4"])
def test_engine_with_1_random_banner_probability_gets_random_banner(
        expected_random_banner_id: str,
        test_banners: List[Banner],
        monkeypatch: pytest.MonkeyPatch,
) -> None:
    def mock_random_choice(banner_ids: List[str]) -> str:
        return expected_random_banner_id

    monkeypatch.setattr(random, "choice", mock_random_choice)

    storage = BannerStorage(test_banners)
    engine = EpsilonGreedyBannerEngine(storage, random_banner_probability=1.0)
    banner_id = engine.show_banner()
    assert banner_id == expected_random_banner_id


def test_total_cost_equals_to_cost_of_clicked_banners(test_banners: List[Banner]) -> None:
    eng = EpsilonGreedyBannerEngine(BannerStorage(test_banners, TEST_DEFAULT_CTR), 0)
    cost = 0
    for banner in test_banners:
        eng.send_click(banner.banner_id)
        cost += banner.cost
    assert cost == eng.total_cost


def test_engine_show_increases_banner_show_stat(test_banners: List[Banner]) -> None:
    storage = BannerStorage(test_banners)
    engine = EpsilonGreedyBannerEngine(storage, random_banner_probability=0.1)

    initial_shows = {banner.banner_id: banner.stat.shows for banner in test_banners}

    banner_id = engine.show_banner()
    assert storage.get_banner(banner_id).stat.shows == initial_shows[banner_id] + 1


def test_engine_click_increases_banner_click_stat(test_banners: List[Banner]) -> None:
    storage = BannerStorage(test_banners)
    engine = EpsilonGreedyBannerEngine(storage, random_banner_probability=0.1)

    initial_clicks = {banner.banner_id: banner.stat.clicks for banner in test_banners}

    for banner in test_banners:
        engine.send_click(banner.banner_id)
        assert storage.get_banner(banner.banner_id).stat.clicks == initial_clicks[banner.banner_id] + 1
