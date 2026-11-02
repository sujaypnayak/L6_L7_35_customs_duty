
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# DUTY RATE - DECISION BRANCHES

def test_prohibited_category():
    with pytest.raises(ValueError):
        duty_rate("weapons", "US")


def test_non_prohibited_electronics():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_non_fta_branch():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta_branch():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_non_fta_branch():
    assert duty_rate("clothing", "US") == 0.12


def test_books_branch():
    assert duty_rate("books", "US") == 0


def test_unknown_category_branch():
    assert duty_rate("furniture", "US") == 0.15


# TOTAL DUTY - DECISION BRANCHES

def test_negative_value_branch():
    with pytest.raises(ValueError):
        total_duty("electronics", -100, "US", False)


def test_non_negative_value_branch():
    assert total_duty("electronics", 2000, "US", False) == 400


def test_gift_within_limit():
    assert total_duty("electronics", 5000, "US", True) == 0


def test_gift_above_limit():
    assert total_duty("electronics", 6000, "US", True) == 200


def test_gift_minimum_duty_branch():
    assert total_duty("electronics", 5100, "US", True) == 50


def test_gift_normal_duty_branch():
    assert total_duty("electronics", 6000, "US", True) == 200


def test_non_gift_within_exemption():
    assert total_duty("electronics", 1000, "US", False) == 0


def test_non_gift_above_exemption():
    assert total_duty("electronics", 2000, "US", False) == 400


def test_zero_duty_branch():
    assert total_duty("books", 2000, "US", False) == 0


# CLEARANCE CHANNEL - DECISION BRANCHES

def test_prohibited_item_refused():
    assert clearance_channel(1000, "weapons", True) == "refuse"


def test_allowed_item_continues():
    assert clearance_channel(1000, "electronics", True) == "green"


def test_value_above_100000():
    assert clearance_channel(150000, "electronics", True) == "inspect"


def test_value_not_above_100000():
    assert clearance_channel(30000, "electronics", False) == "inspect"


def test_missing_documents_inspection():
    assert clearance_channel(30000, "electronics", False) == "inspect"


def test_documents_available():
    assert clearance_channel(30000, "electronics", True) == "green"


def test_low_value_without_documents():
    assert clearance_channel(10000, "electronics", False) == "green"
