import uiautomator2 as u2
from singleton_logger import logger
from singleton_screenshot import screenshoter
from auto_video_swipter import video_swipter
from image_llm_client import call_qwen3_vl
import time
from PIL import Image
import ast

def test01():
    d = u2.connect()
    logger.log(d.info)

    img_path=screenshoter.capture_screen(d,"tmp","tmp")
    print(img_path)

    #prompt='''图中顶部是否有"xxx金币"字样和"xxx元"字样，xxx是具体数字，如果没有回答或判断不出来回答"None"，如果有就回答"金币收益xxx金币;现金收益xxx元",这里的xxx是具体数字,不要回答别的内容。'''
    prompt='''图中是否有"看广告赚金币"字式，如果有，给出文字它所在像素坐标范围,格式"[x1,y1,x2,y2]"，注意截图的左上角为[0,0],分辨率：1200x2640,如果没有或者判断不出来回答"None",不要回答别的内容。'''
    model="qwen3-vl:4b-instruct"  #默认4b-instruct 还有 qwen3-vl:4b   qwen3-vl:2b-instruct   qwen3-vl:latest
    response = call_qwen3_vl(prompt, [img_path], model=model)

    print(response)

    result_list = ast.literal_eval(response)

    print(result_list)  # [1, 2, 3, 4]

    Image.open(img_path).crop((1200*(result_list[0]/1000.0), 2640*(result_list[1]/1000.0),1200*(result_list[2]/1000.0),2640*(result_list[3]/1000.0))).show()

def test02():
    logger.log('启动脚本')
    d = u2.connect()
    logger.log(d.info)

    # target_element = d(textContains='领金币').get_text()
    # print(target_element)
    package_name =d.app_current()['package']
    print(package_name)
    video_swipter.close_app(d,package_name)



if __name__ == "__main__":

    logger.log('启动脚本')
    d = u2.connect()
    logger.log(d.info)

    # if video_swipter.start_app(d,'com.luna.music'):#汽水音乐
    #
    #     target_element = d.xpath('//*[@resource-id="com.luna.music:id/navigation_tab_commerce_coin"]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]')
    #     while not target_element.exists:
    #         logger.log('目标元素等待中...')
    #         time.sleep(1)
    #
    #     target_element.click()
    #     logger.log('进入福利界面')
    #
    #     #d.click(0.828, 0.512) #领金币按钮
    #
    #     time.sleep(1)
    #     #d.click(0.49, 0.674) #看广告膨胀领金币按钮
    #
    #
    #
    #     logger.log('----END----')















