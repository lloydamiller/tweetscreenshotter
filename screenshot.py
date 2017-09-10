from selenium import webdriver


def screenshot(url, filepath, resolution=[1024, 768]):
    driver = webdriver.PhantomJS()
    width, height = resolution[0], resolution[1]
    driver.set_window_size(width, height)

    print('[*] Loading webpage @ %s' % url)
    driver.get(url)

    print('[*] Saving screenshot to %s' % filepath)
    driver.save_screenshot(filepath)

    print('[*] Screenshot saved locally')
    return
