
import pytest
from playwright.sync_api import expect, Error as PlaywrightError


def goto_with_network_retry(page, url, attempts=2):
    for attempt in range(attempts):
        try:
            page.goto(url, wait_until="domcontentloaded")
            return

        except PlaywrightError as error:
            if (
                "ERR_NETWORK_CHANGED" not in str(error)
                or attempt == attempts - 1
            ):
                raise


@pytest.mark.smoke
def test_login_page(page):
    goto_with_network_retry(page, "/login")

    assert "/login" in page.url
    assert "Вход" in page.title()


@pytest.mark.smoke
def test_catalog_page(page):
    goto_with_network_retry(page, "/catalog")

    assert page.locator(
        "div[id='products-grid'] > div"
    ).count() > 0


@pytest.mark.smoke
def test_cart_page(page):
    goto_with_network_retry(page, "/cart")

    assert "/cart" in page.url


@pytest.mark.smoke
def test_login_in_account(page):
    goto_with_network_retry(page, "/login")

    page.fill("input[name='email']", "test_user@shopmarket.ru")
    page.fill("input[name='password']", "Password123")
    page.click("button[id='login-btn']")

    heading = page.locator("h1")
    expect(heading).to_contain_text("Весенняя")
