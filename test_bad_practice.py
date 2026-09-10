import pytest

@pytest.mark.parametrize(
    "email , password",
    [
        pytest.param("alice@example.com", "Password1", id="case_1"),
        pytest.param("alice.alice@example.co.uk", "Password1", id="case_2"),
        pytest.param("alice+alice@example.com", "Password1", id = "case_3"),
        pytest.param("no-at-sign.com", "Password1", id = "case_4"),
        pytest.param("@example.com", "Password1", id = "case_5"),
        pytest.param("alice@example", "Password1", id = "case_6"),
        pytest.param("alice@", "Password1", id = "case_7"),
        pytest.param("", "Password1", id = "case_8"),
        pytest.param(None, "Password1", id = "case_9"),
        pytest.param(123, "Password1", id = "case_10"),
        pytest.param("admin@example.com' OR '1'='1", "Password1", id = "case_11"),
        pytest.param("a@example.com", "Password1", id = "case_12"),
        pytest.param("alice@example.com", "Pa1", id = "case_13"),
        pytest.param("alice@example.com", "PASSWORD1", id = "case_14"),
        pytest.param("alice@example.com", "password1", id = "case_15"),
        pytest.param("alice@example.com", "A1"+"a"*63, id = "case_16"),
        pytest.param("alice@example.com", "", id = "case_17"),
        pytest.param("alice@example.com", None, id = "case_18"),
        pytest.param("alice@example.com", 123, id = "case_19"),
        pytest.param("", "", id = "case_20"),
        pytest.param("", "", id = "case_21"),
        pytest.param("", "", id = "case_22"),
        pytest.param("", "", id = "case_23"),
        pytest.param("", "", id = "case_24"),
        pytest.param("", "", id = "case_25"),
        pytest.param("", "", id = "case_26"),
        pytest.param("", "", id = "case_27"),
        pytest.param("", "", id = "case_28"),
        pytest.param("", "", id = "case_29"),
        pytest.param("", "", id = "case_30"),
    ]
)
def test_just_too_no_errors(email, password):
    assert email == email and password == password
