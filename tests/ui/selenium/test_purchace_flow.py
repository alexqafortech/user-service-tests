def test_full_purchase_flow(
    login_page, catalog_page, cart_page, orders_page
):
    login_page.open()
    login_page.login("test_user@shopmarket.ru", "Password123")

    catalog_page.open()

    # Добавление товара
    catalog_page.add_product_to_cart(1)

    cart_count = catalog_page.wait_for_cart_count(1)
    assert cart_count == 1

    # Корзина
    cart_page.open()

    cart_items = cart_page.wait_for_items_count(1)
    assert cart_items >= 1

    start_summ = cart_page.get_total()

    # Промокод
    cart_page.apply_promo_and_wait("SAVE20", start_summ)

    assert cart_page.get_discount()

    final_summ = cart_page.get_total()
    assert start_summ != final_summ

    # Оформление заказа
    orders_page = cart_page.checkout()
    orders_page.open()

    assert orders_page.get_order_count() >= 1