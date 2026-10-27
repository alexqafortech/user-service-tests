import pytest


@pytest.mark.navigation
def test_user_menu_navigate_to_profile(login_page, main_page, profile_page, parallel_user_registered):
    login_page.open()

    login_page.login(
        parallel_user_registered["email"],
        parallel_user_registered["password"]
    )

    main_page.open_user_profile()
    main_page.wait_for_url_contains("/profile")

    assert profile_page.is_loaded()

