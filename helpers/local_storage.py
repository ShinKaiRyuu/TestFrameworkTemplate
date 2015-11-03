def check_browser_support_storage(driver):
    try:
        return driver.execute_script("return 'localStorage' in window && window['localStorage'] !== null;")
    except Exception:
        return False

def get_storage(driver):
    return driver.execute_script("return window.localStorage")

def set_storage_item(driver, key, value):
    driver.execute_script('return window.localStorage.setItem("{0}", "{1}");'.format(key, value))

def get_storage_item(driver, key):
    return driver.execute_script('return window.localStorage.getItem("{0}");'.format(key))

def delete_storage_item(driver, key):
    return driver.execute_script('return window.localStorage.removeItem("{0}");'.format(key))

def clear_storage(driver):
    return driver.execute_script('return window.localStorage.clear();')
