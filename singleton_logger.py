# singleton_logger.py
import sys
from datetime import datetime


class SingletonLogger:
    """单例模式日志类：替代print，同时输出到控制台和log.txt"""
    _instance = None

    def __new__(cls):
        """单例模式核心：确保全局仅一个实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, *args, **kwargs):
        """
        替代print的日志方法：
        1. 保留print所有功能（控制台输出）
        2. 自动追加内容到log.txt（无文件则创建）
        3. 包含精确到秒的时间戳
        4. 支持中文编码（utf-8）
        """
        # 1. 保留控制台输出（完全复用print的参数和行为）
        print(*args, **kwargs)

        # 2. 处理日志内容和时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 复用print的默认分隔符和结尾符
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        # 转换所有参数为字符串并拼接（与print输出一致）
        log_content = sep.join(map(str, args)) + end

        # 3. 写入日志文件（追加模式，utf-8编码防中文乱码）
        try:
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {log_content}")
        except Exception as e:
            # 写入失败时，仅在控制台 stderr 提示（不影响原功能）
            print(f"⚠️  日志写入失败：{str(e)}", file=sys.stderr)


# 提供全局便捷访问实例（可选，简化使用）
logger = SingletonLogger()