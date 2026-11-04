import time

def test_full_purchase_flow(
    login_page,
    catalog_page,
    cart_page,
    orders_page
):
    # 1. Авторизация
    login_page.open()
    login_page.login(
        "test_user@shopmarket.ru",
        "Password123"
    )

    # 2. Открываем каталог
    catalog_page.open()

    # 3. Запоминаем исходное количество товаров
    start_count = catalog_page.header.get_cart_count()
    time.sleep(1)
    # 4. Добавляем товар и ждём обновления счётчика
    catalog_page.add_product_to_cart_and_wait(
        0,
        start_count + 1
    )

    # 5. Открываем корзину
    cart_page.open()
    cart_page.refresh()

    # 6. Проверяем, что корзина не пустая
    cart_items = cart_page.wait_for_items_count(1)

    assert cart_items >= 1, (
        f"Корзина пустая. Количество товаров: {cart_items}"
    )

    # 7. Получаем исходную сумму
    start_sum = cart_page.get_total()

    # 8. Применяем промокод
    cart_page.apply_promo_and_wait(
        code="SAVE20",
        old_total=start_sum
    )

    # 9. Проверяем наличие скидки
    discount = cart_page.get_discount()

    assert discount, "Скидка по промокоду не применилась"

    # 10. Проверяем изменение итоговой суммы
    final_sum = cart_page.get_total()

    assert start_sum != final_sum, (
        f"Сумма не изменилась после применения промокода. "
        f"До: {start_sum}, после: {final_sum}"
    )

    # 11. Оформляем заказ
    result_orders_page = cart_page.checkout()

    # 12. Проверяем переход на страницу заказов
    assert "/orders" in result_orders_page.driver.current_url, (
        f"После оформления заказа открылась неправильная страница: "
        f"{result_orders_page.driver.current_url}"
    )

    # 13. Проверяем появление заказа
    result_orders_page.wait_until(
        lambda driver: len(
            driver.find_elements(*result_orders_page.ORDER_STATUS)
        ) >= 1,
        timeout=5
    )

    assert result_orders_page.get_order_count() >= 1