import pytest

@pytest.mark.admin
def test_admin_table_shows_users(admin_page):
    admin_page.open()
    items = admin_page.find_all(admin_page.USERS_TABLE)
    assert len(items) > 5

@pytest.mark.admin
def test_find_user_row_by_login (admin_page):
    admin_page.open()
    item = admin_page.get_text(admin_page.ITEM)
    assert item == "test_user@shopmarket.ru"

@pytest.mark.admin
def test_block_active_user(admin_page, request):
    current_browser = request.node.callspec.params.get("driver")

    if current_browser != "chrome":
        pytest.skip("Необходимо только одно выполнение")

    admin_page.open()

    status = admin_page.get_text(admin_page.TEXT_BLOCK_LOCATOR)

    # Если пользователь заблокирован — сначала разблокируем
    if status == "Заблокирован":
        admin_page.click(admin_page.UNBLOCK_USER)
        admin_page.reload_page()

    # Блокируем активного пользователя
    admin_page.click(admin_page.BLOCK_USER)
    admin_page.alert_accept()
    admin_page.reload_page()

    new_status = admin_page.get_text(admin_page.TEXT_BLOCK_LOCATOR)

    assert new_status == "Заблокирован"

    admin_page.reload_data_base()
