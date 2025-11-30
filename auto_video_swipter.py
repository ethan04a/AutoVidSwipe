# auto_video_swipter.py
from singleton_logger import logger
import time
import uiautomator2 as u2
from image_llm_client import call_qwen3_vl
import time
from PIL import Image
import ast
from singleton_screenshot import screenshoter


class AutoVideoSwipter:
    """单例模式自动刷视频模块（空实现，预留核心接口）"""
    _instance = None

    def __new__(cls):
        """单例模式核心：确保全局唯一实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def start_app(self,device: u2.Device,app_package: str = "") -> bool:
        """
        启动目标APP
        :param app_package: APP包名（如：com.example.video），为空则启动默认APP
        :return: bool - 启动成功返回True，失败返回False
        """

        if device.app_current()['package'] == app_package:
            logger.log(device.app_current())
            logger.log(f"📱 执行启动APP操作,发现目标应用正在运行，包名：{app_package or '默认APP'}")
            return True

        app_obj = device.app_start(app_package,wait=True)
        time.sleep(10)
        logger.log(device.app_current())
        logger.log(f"📱 执行启动APP操作，包名：{app_package or '默认APP'}")
        return True

    def close_app(self,device: u2.Device,app_package: str = "") -> bool:
        """
        关闭目标APP
        :param app_package: APP包名，为空则关闭当前活跃APP
        :return: bool - 关闭成功返回True，失败返回False
        """

        device.app_stop(app_package)
        # time.sleep(2)
        # device.drag(500,2638,500,1500,duration=7)
        # time.sleep(2)
        # device.click(0.487, 0.903)

        #device.app_clear(app_package)

        logger.log(f"🔌 执行关闭APP操作，包名：{app_package or '当前活跃APP'}")


        return True



    def swipe_ad(self, ad_duration: int = 5) -> bool:
        """
        刷广告（观看广告获取奖励）
        :param ad_duration: 预期广告时长（秒），用于等待广告播放完成
        :return: bool - 广告刷取成功返回True，失败返回False
        """
        logger.log(f"📺 执行刷广告操作，预期时长：{ad_duration}秒")
        # 空实现：后续可添加 等待广告播放+确认奖励 逻辑
        pass
        return True

    def swipe_video(self, swipe_count: int = 1, interval: float = 3.0) -> bool:
        """
        刷视频（自动滑动下一个）
        :param swipe_count: 刷视频次数（默认1次）
        :param interval: 每个视频停留时长（秒，默认3秒）
        :return: bool - 刷视频完成返回True，失败返回False
        """
        logger.log(f"🎬 执行刷视频操作，次数：{swipe_count}，单视频停留：{interval}秒")
        # 空实现：后续可添加 模拟上下滑动+停留 逻辑
        pass
        return True

    def swipe_novel(self, read_count: int = 1, page_turn_interval: float = 2.0) -> bool:
        """
        刷小说（自动翻页）
        :param read_count: 阅读章节/段落数（默认1）
        :param page_turn_interval: 翻页间隔（秒，默认2秒）
        :return: bool - 刷小说完成返回True，失败返回False
        """
        logger.log(f"📖 执行刷小说操作，阅读数量：{read_count}，翻页间隔：{page_turn_interval}秒")
        # 空实现：后续可添加 模拟左右翻页+停留 逻辑
        pass
        return True

    def has_popup(self,device: u2.Device,popup_flag: str) -> bool:

        img_path = screenshoter.capture_screen(device, "tmp", "tmp")

        prompt = '''图中是否有"'''+popup_flag+'''"字式，如果有回答"Yes",如果没有回答"No",不要回到其它内容。'''
        model = "qwen3-vl:4b-instruct"  # 默认4b-instruct 还有 qwen3-vl:4b   qwen3-vl:2b-instruct   qwen3-vl:latest
        response = call_qwen3_vl(prompt, [img_path], model=model)


        logger.log(f"🎁 执行判断弹窗操作："+popup_flag)
        logger.log(popup_flag+":"+response)

        if response.strip()== "Yes":
            return True
        else:
            return False


    def claim_treasure_box(self,device: u2.Device,flag_str:str) -> bool:
        """
        领取宝箱奖励
        :param flag_str: 宝箱的标志
        :return: bool - 领取成功返回True，无宝箱/领取失败返回False
        """

        displayWidth=device.info['displayWidth']
        displayHeight=device.info['displayHeight']

        img_path = screenshoter.capture_screen(device, "tmp", "tmp")
        #print(img_path)

        prompt = '''图中是否有"'''+flag_str+'''"完全相同切连续的字符串，如果有，给出文字它所在像素坐标范围,格式"[x1,y1,x2,y2]"，注意截图的左上角为[0,0],分辨率：1200x2640,如果没有或者判断不出来回答"None",不要回答别的内容。'''
        model = "qwen3-vl:4b-instruct"  # 默认4b-instruct 还有 qwen3-vl:4b   qwen3-vl:2b-instruct   qwen3-vl:latest
        response = call_qwen3_vl(prompt, [img_path], model=model)

        #print(response)
        logger.log(f"🎁 执行领取宝箱奖励操作:" + flag_str)
        logger.log(flag_str+":"+response)

        if response=="None":
            return False

        result_list = ast.literal_eval(response)

        #print(result_list)  # [1, 2, 3, 4]

        # Image.open(img_path).crop(
        #     (1200 * (result_list[0] / 1000.0), 2640 * (result_list[1] / 1000.0), 1200 * (result_list[2] / 1000.0),
        #      2640 * (result_list[3] / 1000.0))).show()


        x = int(displayWidth * ((result_list[0] + result_list[2]) / 1000.0)/2)
        y = int(displayHeight * ((result_list[1] + result_list[3]) / 1000.0)/2)
        #print(x,y)
        device.click(x,y)



        return True

    def get_gold_count(self) -> int:
        """
        获取当前金币数量
        :return: int - 当前金币数（无数据返回0）
        """
        logger.log(f"💰 执行获取金币数量操作")
        # 空实现：后续可添加 查找金币控件+读取数值 逻辑
        gold_count = 0  # 占位值
        logger.log(f"💰 当前金币数量：{gold_count}")
        return gold_count

    def force_exit_ad_mode(self) -> bool:
        """
        强制退出广告模式（跳过广告）
        :return: bool - 退出成功返回True，失败返回False
        """
        logger.log(f"🚫 执行强制退出广告模式操作")
        # 空实现：后续可添加 点击跳过按钮/返回键退出 逻辑
        pass
        return True

    def force_exit_live_mode(self) -> bool:
        """
        强制退出直播模式
        :return: bool - 退出成功返回True，失败返回False
        """
        logger.log(f"🚫 执行强制退出直播模式操作")
        # 空实现：后续可添加 点击关闭按钮/返回键退出 逻辑
        pass
        return True

    def force_exit_novel_mode(self) -> bool:
        """
        强制退出小说模式
        :return: bool - 退出成功返回True，失败返回False
        """
        logger.log(f"🚫 执行强制退出小说模式操作")
        # 空实现：后续可添加 点击返回按钮/关闭章节 逻辑
        pass
        return True


# 全局便捷访问实例（简化调用）
video_swipter = AutoVideoSwipter()