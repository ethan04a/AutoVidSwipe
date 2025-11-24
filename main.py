import uiautomator2 as u2
from singleton_logger import logger
from singleton_screenshot import screenshoter


if __name__ == "__main__":

    logger.log('启动脚本')

    d = u2.connect()
    logger.log(d.info)

    d.press('home')
    screenshoter.capture_screen(d)



