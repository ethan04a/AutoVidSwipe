# singleton_screenshot.py
import sys
import os
import time
from datetime import datetime
from PIL import Image
# 导入之前封装的日志单例模块（确保路径可访问）
from singleton_logger import logger


class SingletonScreenshot:
    """单例模式 uiautomator2 截图模块"""
    _instance = None

    def __new__(cls):
        """单例核心：确保全局仅一个实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def capture_screen(
            self,
            device,
            save_dir: str = "screenshots"
    ) -> str:
        """
        uiautomator2 截图并保存本地（带时间戳+分辨率验证）

        :param device: u2设备对象（uiautomator2.connect() 返回的实例）
        :param save_dir: 保存文件夹路径（默认：当前目录/screenshots）
        :return: 截图完整保存路径
        """
        # 1. 创建保存文件夹（不存在则创建）
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            logger.log(f"📂 文件夹不存在，已创建：{save_dir}")

        # 2. 生成带时间戳的文件名（精确到秒，避免重复）
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        img_name = f"{timestamp}.png"
        img_path = os.path.abspath(os.path.join(save_dir, img_name))  # 绝对路径

        try:
            # 3. 调用u2设备截图并保存（默认无压缩）
            device.screenshot().save(img_path)

            # 4. 验证截图与手机分辨率一致性
            with Image.open(img_path) as img:
                img_width, img_height = img.size
            phone_width, phone_height = device.window_size()  # 获取手机实际分辨率

            # 5. 日志输出（使用单例日志模块）
            logger.log("✅ 截图成功！")
            logger.log(f"📁 保存路径：{img_path}")
            logger.log(f"📊 手机分辨率：{phone_width}x{phone_height}")
            logger.log(f"📊 截图分辨率：{img_width}x{img_height}")

            # 6. 延迟3秒（保留原逻辑）
            time.sleep(3)

            return img_path

        except Exception as e:
            logger.log(f"❌ 截图失败！错误信息：{str(e)}", file=sys.stderr)
            raise  # 抛出异常，让调用方处理（或根据需求修改为返回None）


# 提供全局便捷访问实例（简化调用）
screenshoter = SingletonScreenshot()