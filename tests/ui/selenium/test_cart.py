import pytest
import time

@pytest.mark.cart
def test_add_to_cart_increases_counter_lambda(catalog_page):
    catalog_page.open()

    products = catalog_page.get_products()
    start_cart_value = catalog_page.header.get_cart_count()

    for index in range(3):
        expected_value = start_cart_value + index + 1

        catalog_page.add_product_to_cart_and_wait(
            index,
            expected_value
        )

        actual_value = catalog_page.header.get_cart_count()
        assert actual_value == expected_value, (
            f"Ожидалось {expected_value} товаров, "
            f"получено {actual_value}"
        )

@pytest.mark.cart
def test_add_three_products_to_cart(catalog_page):
    catalog_page.open()

    start_count = catalog_page.header.get_cart_count()

    for index in range(3):
        expected_count = start_count + index + 1

        catalog_page.add_product_to_cart_and_wait(
            index,
            expected_count
        )

    assert catalog_page.header.get_cart_count() == start_count + 3

@pytest.mark.cart
def test_cart_page_shows_added_products(catalog_page, cart_page):
    catalog_page.open()

    start_cart_value = catalog_page.header.get_cart_count()

    catalog_page.add_product_to_cart_and_wait(
        0,
        start_cart_value + 1
    )

    cart_page.open()

    items_count = cart_page.get_items_count()

    assert items_count == 1, (
        f"Ожидался 1 товар в корзине, получено {items_count}"
    )
