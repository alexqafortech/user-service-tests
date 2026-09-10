pytest -m smoke
...
test_validators.py::test_is_valid_email[invalid_double_dot_in_domain_QA1234] XFAIL [ 71%]
test_validators.py::test_is_valid_password[valid_standard] PASSED        [ 75%]
test_validators.py::test_is_valid_password[valid_min_length_8] PASSED    [ 78%]
test_validators.py::test_is_valid_password[valid_max_length_64] PASSED   [ 82%]
test_validators.py::test_is_valid_password[invalid_too_short_7] PASSED   [ 85%]
test_validators.py::test_is_valid_password[invalid_too_long_65] PASSED   [ 89%]
test_validators.py::test_is_valid_password[invalid_no_digit] PASSED      [ 92%]
test_validators.py::test_is_valid_password[invalid_no_uppercase] PASSED  [ 96%]
test_validators.py::test_is_valid_password[invalid_no_lowercase] PASSED  [100%]

================= 27 passed, 73 deselected, 1 xfailed in 0.08s =================

pytest -m regression
...
test_user_service_basic.py::test_register_with_short_password_raises_value_error PASSED [ 65%]
test_user_service_delete.py::test_delete_existing_user_makes_get_return_none PASSED [ 70%]
test_user_service_delete.py::test_delete_nonexistent_user_rises PASSED   [ 75%]
test_user_service_delete.py::test_delete_one_user_keeps_other PASSED     [ 80%]
test_user_service_lifecycle.py::test_user_service_count_increases_for_multiple_users PASSED [ 85%]
test_user_service_lifecycle.py::test_login_with_wrong_password_raises PASSED [ 90%]
test_user_service_lifecycle.py::test_login_with_nonexistent_email_raises PASSED [ 95%]
test_user_service_lifecycle.py::test_get_user_returns_none_for_unknown_email PASSED [100%]

====================== 20 passed, 81 deselected in 0.07s =======================

pytest -m "smoke or regression"
...
test_validators.py::test_is_valid_password[valid_standard] PASSED        [ 85%]
test_validators.py::test_is_valid_password[valid_min_length_8] PASSED    [ 87%]
test_validators.py::test_is_valid_password[valid_max_length_64] PASSED   [ 89%]
test_validators.py::test_is_valid_password[invalid_too_short_7] PASSED   [ 91%]
test_validators.py::test_is_valid_password[invalid_too_long_65] PASSED   [ 93%]
test_validators.py::test_is_valid_password[invalid_no_digit] PASSED      [ 95%]
test_validators.py::test_is_valid_password[invalid_no_uppercase] PASSED  [ 97%]
test_validators.py::test_is_valid_password[invalid_no_lowercase] PASSED  [100%]

================= 47 passed, 58 deselected, 1 xfailed in 0.14s =================


pytest -m "smoke and auth"
...
collected 101 items / 95 deselected / 6 selected                               

test_register_parametrized.py::test_register_with_valid_data_creates_user[standard] PASSED [ 16%]
test_register_parametrized.py::test_register_with_valid_data_creates_user[with_dots] PASSED [ 33%]
test_register_parametrized.py::test_register_with_valid_data_creates_user[with_plus_tag] PASSED [ 50%]
test_register_parametrized.py::test_register_with_valid_data_creates_user[short_email_min_pass] PASSED [ 66%]
test_user_service_lifecycle.py::test_user_service_count_increases_after_register PASSED [ 83%]
test_user_service_lifecycle.py::test_login_with_correct_credentials_returns_user PASSED [100%]

======================= 6 passed, 95 deselected in 0.05s =======================

pytest -m "not slow"
...
test_validators.py::test_is_valid_email[invalid_double_dot_in_domain_QA1234] XFAIL [ 89%]
test_validators.py::test_is_valid_password[valid_standard] PASSED        [ 90%]
test_validators.py::test_is_valid_password[valid_min_length_8] PASSED    [ 91%]
test_validators.py::test_is_valid_password[valid_max_length_64] PASSED   [ 92%]
test_validators.py::test_is_valid_password[invalid_too_short_7] PASSED   [ 93%]
test_validators.py::test_is_valid_password[invalid_too_long_65] PASSED   [ 94%]
test_validators.py::test_is_valid_password[invalid_no_digit] PASSED      [ 95%]
test_validators.py::test_is_valid_password[invalid_no_uppercase] PASSED  [ 96%]
test_validators.py::test_is_valid_password[invalid_no_lowercase] PASSED  [ 97%]
test_validators_env.py::test_default_max_password_length PASSED          [ 98%]
test_validators_env.py::test_max_password_length_from_env PASSED         [ 99%]
test_validators_env.py::test_max_password_length_isolated_between_tests PASSED [100%]

======================== 100 passed, 1 xfailed in 0.16s ========================

pytest -m storage
...
collected 101 items / 94 deselected / 7 selected                               

test_user_service_delete.py::test_delete_existing_user_removes_from_storage PASSED [ 14%]
test_user_service_delete.py::test_delete_existing_user_makes_get_return_none PASSED [ 28%]
test_user_service_delete.py::test_delete_nonexistent_user_rises PASSED   [ 42%]
test_user_service_delete.py::test_delete_one_user_keeps_other PASSED     [ 57%]
test_user_service_lifecycle.py::test_user_service_starts_empty PASSED    [ 71%]
test_user_service_lifecycle.py::test_get_user_returns_registered_user PASSED [ 85%]
test_user_service_lifecycle.py::test_get_user_returns_none_for_unknown_email PASSED [100%]

======================= 7 passed, 94 deselected in 0.05s =======================

Сравнение smoke vs regression

Smoke
Количество тестов: 28
Общее время прогона: 0.08s
Самые медленные тесты (топ-5)
1. test_register_parametrized.py::test_register_with_valid_data_creates_user[standard]
2. test_user_service_lifecycle.py::test_login_with_correct_credentials_returns_user
3. test_user_service_lifecycle.py::test_get_user_returns_registered_user
4. test_user_service_delete.py::test_delete_existing_user_removes_from_storage
5. test_register_parametrized.py::test_register_with_valid_data_creates_user[with_dots]

Regression
Количество тестов: 20
Общее время прогона: 0.08s
Самые медленные тесты (топ-5)
1. test_login_parametrized.py::test_login_with_invalid_credentials_raises[wrong_password]
2. test_user_service_lifecycle.py::test_login_with_nonexistent_email_raises
3. test_user_service_lifecycle.py::test_get_user_returns_none_for_unknown_email
4. test_user_service_delete.py::test_delete_existing_user_makes_get_return_none
5. test_login_parametrized.py::test_login_with_invalid_credentials_raises[lowercase_password]