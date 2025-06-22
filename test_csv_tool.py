import main
import pytest

mock_data = [
    {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
]


def test_filter_equal():
    result = main.filter_data(mock_data, "brand=apple")
    assert len(result) == 1
    assert result[0]["name"] == "iphone 15 pro"


def test_filter_greater():
    result = main.filter_data(mock_data, "price>500")
    assert len(result) == 2


def test_filter_less():
    result = main.filter_data(mock_data, "rating<4.5")
    assert len(result) == 1
    assert result[0]["name"] == "poco x5 pro"


def test_aggregate_avg():
    result = main.aggregate_data(mock_data, "price=avg")
    assert "avg" in result
    assert result["avg"][0] == pytest.approx(674.0)


def test_aggregate_min():
    result = main.aggregate_data(mock_data, "rating=min")
    assert "min" in result
    assert result["min"][0] == pytest.approx(4.4)


def test_aggregate_max():
    result = main.aggregate_data(mock_data, "rating=max")
    assert "max" in result
    assert result["max"][0] == pytest.approx(4.9)
