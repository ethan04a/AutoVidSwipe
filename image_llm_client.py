# image_llm_client.py
import os
import base64
import ollama

class Qwen3VLClient:
    """Qwen3-VL 模型调用单例客户端（简化版）"""
    _instance = None

    def __new__(cls):
        # 简单单例实现（无多线程锁）
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.default_model = "qwen3-vl:4b-instruct"
        return cls._instance

    def _image_to_base64(self, image_path: str) -> str:
        """图片转 Base64（仅保留路径存在性校验）"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片路径不存在：{image_path}")

        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def generate_response(self, prompt: str, image_paths: list[str] = None, model: str = None) -> str:
        """
        图文混合交互（支持纯文本/单张/多张图片）
        Args:
            prompt: 提示词
            image_paths: 图片路径列表（可选，None/空列表则为纯文本交互）
            model: 自定义模型名称（可选）
        Returns:
            模型响应文本
        """
        if not prompt:
            raise ValueError("提示词不能为空")

        # 处理图片（无图片则传递空列表）
        img_base64_list = []
        if image_paths:
            img_base64_list = [self._image_to_base64(path) for path in image_paths]

        target_model = model or self.default_model
        try:
            # 无图片时不传递 images 参数（或传递空列表均可）
            response = ollama.generate(
                model=target_model,
                prompt=prompt,
                images=img_base64_list if img_base64_list else None
            )
            return response.response.strip()
        except ollama.Error as e:
            raise RuntimeError(f"模型调用失败：{str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"处理失败：{str(e)}") from e

    def ask(self, prompt: str, model: str = None) -> str:
        return self.generate_response(prompt=prompt, image_paths=None, model=model)

# 单例实例（模块导入时初始化）
qwen3_vl_client = Qwen3VLClient()

# 简化调用函数（直接使用单例）
def call_qwen3_vl(prompt: str, image_paths: list[str]=None, model: str = None) -> str:
    return qwen3_vl_client.generate_response(prompt, image_paths, model)
