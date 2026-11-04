import json
import pytest

@pytest.mark.javascript
def test_cart_stored_in_localstorage(catalog_page, cart_page):
    catalog_page.open()

    # Тест проверяет именно гостевую корзину в LocalStorage.
    cart_page.clear_localstorage_cart()
    catalog_page.refresh()

    start_cart_count = cart_page.get_localstorage_cart_count()

    catalog_page.add_product_to_cart_and_wait(
        0,
        start_cart_count + 1
    )

    local_storage_cart = catalog_page.driver.execute_script(
        "return localStorage.getItem('cart_items');"
    )

    assert local_storage_cart is not None, (
        "Корзина не найдена в LocalStorage"
    )

    cart_data = json.loads(local_storage_cart)

    # Учитываем quantity, а не количество записей в массиве.
    total_quantity = sum(
        int(item.get("quantity", 1))
        for item in cart_data
    )

    assert total_quantity == start_cart_count + 1, (
        f"Ожидалось {start_cart_count + 1} товаров, "
        f"получено {total_quantity}"
    )

    assert cart_page.header.get_cart_count() == total_quantity


@pytest.mark.javascript
def test_clear_localstorage_empties_cart(catalog_page, cart_page):
    catalog_page.open()

    # Начинаем с пустой гостевой корзины.
    cart_page.clear_localstorage_cart()
    catalog_page.refresh()

    assert cart_page.get_localstorage_cart_count() == 0

    # Добавляем товар.
    catalog_page.get_products()
    catalog_page.add_first_product_to_cart()

    cart_page.wait_for_cart_count(1)

    assert cart_page.get_localstorage_cart_count() == 1

    # Очищаем LocalStorage и перечитываем состояние приложения.
    cart_page.clear_localstorage_cart()
    catalog_page.refresh()

    assert cart_page.get_localstorage_cart_count() == 0
    assert cart_page.header.get_cart_count() == 0
