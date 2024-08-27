import time


def scrolldown(driver, deep):
    """Функция для скрола страницы"""
    for _ in range(deep):
        driver.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.5)
