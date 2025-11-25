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
            save_dir: str = "screenshots",
            img_name: str = None  # 新增：可选图片名称参数
    ) -> str:
        """
        uiautomator2 截图并保存本地（支持指定图片名+时间戳 fallback+分辨率验证）

        :param device: u2设备对象（uiautomator2.connect() 返回的实例）
        :param save_dir: 保存文件夹路径（默认：当前目录/screenshots）
        :param img_name: 自定义图片名称（可选，不带后缀则自动补充 .png；未指定则用时间戳）
        :return: 截图完整保存路径
        """
        # 1. 创建保存文件夹（不存在则创建）
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            logger.log(f"📂 文件夹不存在，已创建：{save_dir}")

        # 2. 生成图片名称（优先使用自定义名称，无则用时间戳）
        if img_name:
            # 处理后缀：如果不带 .png 则自动补充
            if not img_name.endswith(".png"):
                img_name += ".png"
        else:
            # 原有逻辑：时间戳命名（精确到秒，避免重复）
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            img_name = f"{timestamp}.png"

        # 拼接完整保存路径（绝对路径）
        img_path = os.path.abspath(os.path.join(save_dir, img_name))

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
            raise  # 抛出异常，让调用方处理


# 提供全局便捷访问实例（简化调用）
screenshoter = SingletonScreenshot()