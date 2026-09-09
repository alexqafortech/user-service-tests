(venv) user@user-MS-7C51:~/user-service-tests$ pytest -v
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.4.2, pluggy-1.6.0 -- /home/user/user-service-tests/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/user-service-tests
collected 18 items                                                             

test_validators.py::test_email_valid_simple PASSED                       [  5%]
test_validators.py::test_email_valid_with_dots PASSED                    [ 11%]
test_validators.py::test_email_valid_with_plus PASSED                    [ 16%]
test_validators.py::test_email_invalid_no_at_sign PASSED                 [ 22%]
test_validators.py::test_email_invalid_no_local_part PASSED              [ 27%]
test_validators.py::test_email_invalid_no_domain PASSED                  [ 33%]
test_validators.py::test_email_invalid_no_tld PASSED                     [ 38%]
test_validators.py::test_email_invalid_empty_string PASSED               [ 44%]
test_validators.py::test_email_invalid_none PASSED                       [ 50%]
test_validators.py::test_email_invalid_not_a_string PASSED               [ 55%]
test_validators.py::test_password_valid_standard PASSED                  [ 61%]
test_validators.py::test_password_valid_minimum_length PASSED            [ 66%]
test_validators.py::test_password_invalid_too_short PASSED               [ 72%]
test_validators.py::test_password_invalid_too_long PASSED                [ 77%]
test_validators.py::test_password_invalid_no_digit PASSED                [ 83%]
test_validators.py::test_password_invalid_no_uppercase PASSED            [ 88%]
test_validators.py::test_password_invalid_no_lowercase PASSED            [ 94%]
test_validators.py::test_password_invalid_empty PASSED                   [100%]

============================== 18 passed in 0.03s ==============================

(venv) user@user-MS-7C51:~/user-service-tests$ pytest -v -k "email"
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.4.2, pluggy-1.6.0 -- /home/user/user-service-tests/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/user-service-tests
collected 18 items / 8 deselected / 10 selected                                

test_validators.py::test_email_valid_simple PASSED                       [ 10%]
test_validators.py::test_email_valid_with_dots PASSED                    [ 20%]
test_validators.py::test_email_valid_with_plus PASSED                    [ 30%]
test_validators.py::test_email_invalid_no_at_sign PASSED                 [ 40%]
test_validators.py::test_email_invalid_no_local_part PASSED              [ 50%]
test_validators.py::test_email_invalid_no_domain PASSED                  [ 60%]
test_validators.py::test_email_invalid_no_tld PASSED                     [ 70%]
test_validators.py::test_email_invalid_empty_string PASSED               [ 80%]
test_validators.py::test_email_invalid_none PASSED                       [ 90%]
test_validators.py::test_email_invalid_not_a_string PASSED               [100%]

======================= 10 passed, 8 deselected in 0.02s =======================

(venv) user@user-MS-7C51:~/user-service-tests$ pytest -v -k "password and not email"
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.4.2, pluggy-1.6.0 -- /home/user/user-service-tests/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/user-service-tests
collected 18 items / 10 deselected / 8 selected                                

test_validators.py::test_password_valid_standard PASSED                  [ 12%]
test_validators.py::test_password_valid_minimum_length PASSED            [ 25%]
test_validators.py::test_password_invalid_too_short PASSED               [ 37%]
test_validators.py::test_password_invalid_too_long PASSED                [ 50%]
test_validators.py::test_password_invalid_no_digit PASSED                [ 62%]
test_validators.py::test_password_invalid_no_uppercase PASSED            [ 75%]
test_validators.py::test_password_invalid_no_lowercase PASSED            [ 87%]
test_validators.py::test_password_invalid_empty PASSED                   [100%]

======================= 8 passed, 10 deselected in 0.02s =======================

(venv) user@user-MS-7C51:~/user-service-tests$ pytest -v test_validators.py::test_password_invalid_too_short
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.4.2, pluggy-1.6.0 -- /home/user/user-service-tests/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/user-service-tests
collected 1 item                                                               

test_validators.py::test_password_invalid_too_short PASSED               [100%]

============================== 1 passed in 0.01s ===============================

(venv) user@user-MS-7C51:~/user-service-tests$ pytest -v -x
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-8.4.2, pluggy-1.6.0 -- /home/user/user-service-tests/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/user-service-tests
collected 18 items                                                             

test_validators.py::test_email_valid_simple PASSED                       [  5%]
test_validators.py::test_email_valid_with_dots PASSED                    [ 11%]
test_validators.py::test_email_valid_with_plus PASSED                    [ 16%]
test_validators.py::test_email_invalid_no_at_sign PASSED                 [ 22%]
test_validators.py::test_email_invalid_no_local_part PASSED              [ 27%]
test_validators.py::test_email_invalid_no_domain PASSED                  [ 33%]
test_validators.py::test_email_invalid_no_tld PASSED                     [ 38%]
test_validators.py::test_email_invalid_empty_string PASSED               [ 44%]
test_validators.py::test_email_invalid_none PASSED                       [ 50%]
test_validators.py::test_email_invalid_not_a_string PASSED               [ 55%]
test_validators.py::test_password_valid_standard PASSED                  [ 61%]
test_validators.py::test_password_valid_minimum_length PASSED            [ 66%]
test_validators.py::test_password_invalid_too_short PASSED               [ 72%]
test_validators.py::test_password_invalid_too_long PASSED                [ 77%]
test_validators.py::test_password_invalid_no_digit PASSED                [ 83%]
test_validators.py::test_password_invalid_no_uppercase PASSED            [ 88%]
test_validators.py::test_password_invalid_no_lowercase PASSED            [ 94%]
test_validators.py::test_password_invalid_empty PASSED                   [100%]

============================== 18 passed in 0.03s ==============================
