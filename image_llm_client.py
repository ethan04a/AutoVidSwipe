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



# # 1. 定义图片路径和文本提示
# image_path = "C:/developer/pythonproj/AutoVidSwipe/screenshots/2025-11-25_03-24-07.png"  # 替换为你的图片绝对路径（Windows："C:\\Users\\xxx\\test.png"）
# #prompt = '''图中顶部是否有"xxx金币"字样和"xxx元"字样，xxx是具体数字，如果没有回答或判断不出来回答"None"，如果有就回答"金币收益xxx金币;现金收益xxx元",这里的xxx是具体数字,不要回答别的内容。'''  # 你的文本指令
# prompt = '''图中是否有"点可领710金币"字式，如果有，给出文字它所在像素坐标范围,格式"[x1,y1,x2,y2]"，注意截图的左上角为[0,0],分辨率：1200x2640,如果没有或者判断不出来回答"None",不要回答别的内容。'''
# # 2. 工具函数：读取本地图片并转换为 Base64 编码（Ollama 要求无前缀）
# def image_to_base64(image_path):
#     if not os.path.exists(image_path):
#         raise FileNotFoundError(f"图片路径不存在：{image_path}")
#     # 读取图片二进制数据
#     with open(image_path, "rb") as f:
#         img_bytes = f.read()
#     # 编码为 Base64 字符串（去掉前缀）
#     return base64.b64encode(img_bytes).decode("utf-8")
#
# # 3. 生成 Base64 编码的图片
# img_base64 = image_to_base64(image_path)
#
# # 4. 调用 Qwen3-VL 模型（核心：通过 images 参数传图片）
# resp = ollama.generate(
#     model="qwen3-vl:4b-instruct",  # 模型名（与你之前一致）
#     prompt=prompt,            # 文本提示（描述你要模型做的事）
#     images=[img_base64]       # 图片列表（支持多张，如 [img1, img2]）
# ).response
#
# print("模型响应：")
# print(resp)

    # from PIL import Image
    # Image.open("C:/developer/pythonproj/AutoVidSwipe/screenshots/2025-11-25_03-24-07.png").crop((1200*0.773, 2640*0.846,1200*0.950,2640*0.864)).show()