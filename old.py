import uiautomator2 as u2
import time
import os
import sys
from datetime import datetime
import pytesseract
from PIL import Image, ImageFilter, ImageOps
from typing import Tuple, Optional, Union

config = (
    "—psm 3 —oem 3"  # 强制单行识别（比 psm 6 更严格锁定单行）
    "-c preserve_interword_spaces=0 "
    "-c chinese_layout=1 "
    "-c chinese_segmentation=1 "  # 中文分词（核心）
    "-c textord_old_xheight=1 "  # 优化小字体
    "-c textord_space_size_limit=5 "  # 更小的空格限制（单行文本字符更密集）
    "-c min_characters_to_try=4 "
)



def log_print(*args, **kwargs):
    """
    替代print的日志函数：
    1. 保留print的所有功能（控制台输出）
    2. 自动将内容追加到本地log.txt（无文件则创建）
    3. 日志包含时间戳（精确到秒）
    4. 支持中文编码（避免乱码）
    """
    # 1. 先执行print，保留控制台输出功能
    print(*args, **kwargs)

    # 2. 处理日志内容：拼接参数（与print输出一致）+ 时间戳
    # 获取当前时间戳（格式：2025-11-15 14:35:22）
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 拼接日志内容（处理不同类型参数，如字符串、数字、对象等）
    # 参考print的默认分隔符（sep=' '）和结尾符（end='\n'）
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    log_content = sep.join(map(str, args)) + end

    # 3. 写入log.txt（追加模式，自动创建文件，utf-8编码防中文乱码）
    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            # 日志格式：[时间戳] 内容
            f.write(f"[{timestamp}] {log_content}")
    except Exception as e:
        # 若写入失败，控制台提示（不影响原print功能）
        print(f"⚠️  日志写入失败：{str(e)}", file=sys.stderr)

def capture_screen_with_timestamp(device, save_dir="screenshots"):
    """
    uiautomator2 截图并保存本地
    :param device: u2设备对象
    :param save_dir: 保存文件夹路径（默认当前目录下的screenshots文件夹）
    :return: 保存的图片路径
    """
    # 1. 创建保存文件夹（若不存在）
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 2. 生成精确到秒的日期时间文件名（格式：2025-11-15_14-30-25.png）
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    img_name = f"{timestamp}.png"
    img_path = os.path.join(save_dir, img_name)  # 完整保存路径

    # 3. 截图并保存（默认无压缩，分辨率与手机一致）
    # screenshot() 方法默认返回PIL.Image对象，save() 保存到本地
    device.screenshot().save(img_path)

    # 4. 验证截图分辨率（可选，用于确认与手机分辨率一致）
    from PIL import Image
    with Image.open(img_path) as img:
        img_width, img_height = img.size
    phone_width, phone_height = device.window_size()  # 获取手机分辨率
    log_print(f"✅ 截图成功！")
    log_print(f"📁 保存路径：{img_path}")
    log_print(f"📊 手机分辨率：{phone_width}x{phone_height}")
    log_print(f"📊 截图分辨率：{img_width}x{img_height}")
    time.sleep(3)
    return img_path

#打开app
def go_into_app(device,app_name):
    app_icon = device(text=app_name)
    if app_icon.click_exists(timeout=5):
        log_print(app_name + '打开成功')
    else:
        log_print(app_name + '打开失败')
    time.sleep(3)

#打开应用种的项目
def click_bottom_item(device,item_name):
    if device(text=item_name).click_exists(timeout=5):
        log_print(f"成功点击「{item_name}」按钮")
    else:
        log_print(f"未找到「{item_name}」按钮或按钮不可点击")
    time.sleep(3)

#向上滑动
def swipe_up(device):
    device.swipe(500, 1500, 500, 100)
    log_print("已执行向上滑动")
    time.sleep(18)

#返回桌面
def go_back_desktop(device):
    device.press("home")
    log_print('返回桌面')
    time.sleep(3)


#红果免费短剧
def HonGuoDuanju(device,max_count):
    app_name = '红果免费短剧'
    timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
    log_print('-----------------------------------'+timestamp+' '+app_name+' 开始-----------------------------------')
    go_into_app(device,app_name)
    click_bottom_item(device,'首页')

    count = 0
    while count < max_count:
        swipe_up(device)
        count +=1
        log_print('完成次数：'+str(count))

    #capture_screen_with_timestamp(d)
    go_back_desktop(device)
    timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
    log_print('-----------------------------------'+timestamp+' '+app_name+' 结束-----------------------------------')
    log_print('\n\n')

#快手极速版
def kuaishoujisuban(device,max_count):
    app_name = '快手极速版'
    timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
    log_print('-----------------------------------'+timestamp+' '+app_name+' 开始-----------------------------------')
    go_into_app(device,app_name)
    click_bottom_item(device,'首页')

    count = 0
    while count < max_count:
        swipe_up(device)
        count +=1
        log_print('完成次数：'+str(count))

    #capture_screen_with_timestamp(d)
    go_back_desktop(device)
    timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
    log_print('-----------------------------------'+timestamp+' '+app_name+' 结束-----------------------------------')
    log_print('\n\n')



def find_text_coordinate(image_path: str,target_text: str,region:Optional[tuple[int, int, int, int]] = None) -> Optional[Tuple[int, int, int, int]]:

    try:
        img = Image.open(image_path).crop(region)
        if region!=None :
            img = img.crop(region)
        else:
            region=tuple([0,0,1080,2400])
    except Exception as e:
        raise ValueError(f"无法读取图片：{image_path}（错误：{str(e)}）")

    offset=0;
    flag=-1


    while region[1]+offset < region[3]:

        offset_3 =region[1] + offset+ 100
        if offset_3>region[3] :
            offset_3 = region[3]

        img = Image.open(image_path).crop((region[0], region[1] + offset, region[2], offset_3))

        readStr = pytesseract.image_to_string(img, lang='chi_sim+en', config=config)
        print(readStr)
        flag=readStr.replace(" ", "").find(target_text)
        if flag!=-1:
            break
        else:
            offset+=100


    if flag==-1:
        print('没找到字符串：'+target_text)
        return None

    print("找到字符串："+target_text)


    result = pytesseract.image_to_data(
        img,
        lang='chi_sim',
        output_type=pytesseract.Output.DICT,
        config=config
    )
    # 提取所有关键信息（文本+位置）
    texts = result['text']
    lefts = result['left']  # 文本左上角x坐标
    tops = result['top']  # 文本左上角y坐标
    widths = result['width']  # 文本宽度
    heights = result['height']  # 文本高度
    confidences = result['conf']  # 识别置信度（-1 表示无）
    found=tuple()
    # 按索引遍历，关联文本和位置信息
    for i in range(len(texts)):
        text = texts[i].strip()
        if text and result:

            # 获取位置信息
            left = lefts[i]
            top = tops[i]+offset+region[1]
            width = widths[i]
            height = heights[i]
            confidence = confidences[i]

            # 打印结果（可根据需求存储或处理）
            # print(f"""
            # 中文文本：{text}
            # 位置：左上角({left}, {top})，宽{width}，高{height}
            # 置信度：{confidence}
            # """)

            if text==target_text[0] or text==target_text[1] or text==target_text[0]+target_text[1]:
                found=found+(left,top,width,height)


    return found



#测试代码（中文专属配置）
# if __name__ == "__main__":
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#
#     d = u2.connect()
#
#     test_image = capture_screen_with_timestamp(d)
#     test_text = '点可领'
#     region = (0, 1900, 1080, 2400)  # 核心：(x1, y1, x2, y2)，需替换为你的目标区域坐标
#
#     coords = find_text_coordinate(image_path=test_image,target_text=test_text,region =region)
#     print(coords)
#
#     if coords!=None:
#        d.click(coords[0], coords[1])

def kuaishoujisuban_kanGuangGao(device,max_count):

    app_name = '快手极速版'
    timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
    log_print('-----------------------------------'+timestamp+' '+app_name+' 开始-----------------------------------')
    go_into_app(device,app_name)



    while True:
        # 设定超时时间：30分钟 = 30 * 60 秒
        TIMEOUT = 30 * 60
        start_time = time.time()  # 记录循环开始时间戳

        click_bottom_item(device, '去赚钱')
        time.sleep(3)
        device.click(1000,2100)
        time.sleep(5)

        if time.time() - start_time >= TIMEOUT:
            log_print("已运行30分钟，退出循环")

            go_back_desktop(device)
            timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
            log_print(
                '-----------------------------------' + timestamp + ' ' + app_name + ' 结束-----------------------------------')
            log_print('\n\n')
            return

        while True:

            is_exist = device(textStartsWith="去看广告").exists()
            if is_exist:
                device(textStartsWith="去看广告得最高").click()
                log_print("进入看广告状态")
                break
            else:
                log_print('未成功进入看广告状态 重新尝试')
                click_bottom_item(d, '去赚钱')

                if d(text='更多直播').exists():
                    log_print("进入看直播状态")
                    break

                if d(text='卖货频道').exists():
                    log_print("进入看直播状态")
                    break

                time.sleep(3)
                for i in range(6):
                    if d(text='看广告得金币').exists():
                        d(text='看广告得金币').click()
                        break
                    else:
                        d.swipe(500, 600, 500, 200)
                time.sleep(3)
                if d.xpath('//*[contains(@text,"可领取")]').exists:
                    time.sleep(7)
                    log_print("进入看广告状态")
                    break

            if time.time() - start_time >= TIMEOUT:
                log_print("已运行30分钟，退出循环")

                go_back_desktop(device)
                timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
                log_print(
                    '-----------------------------------' + timestamp + ' ' + app_name + ' 结束-----------------------------------')
                log_print('\n\n')
                return

        while True:

            is_exist = device(textStartsWith="已成功领取").exists()
            if is_exist:
                device(textStartsWith="已成功领取").click()
                time.sleep(3)
                log_print('广告结束点击x')

            if d(text='更多直播').exists() or d(text='卖货频道').exists():
                time.sleep(30)
                d.swipe(0, 600, 1000, 600)
                log_print('退出直播')

                if d(text='开心收下').exists():
                    d(text='开心收下').click()
                    time.sleep(2)
                    d.swipe(0, 600, 1000, 600)
                    log_print('开心收下')

                time.sleep(3)

                if d(text='换一个广告').exists():
                    d(text='换一个广告').click()
                    log_print('换一个广告')

                else:
                    if d(text='首页').exists() and d(text='去赚钱').exists():

                        go_back_desktop(device)
                        timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
                        log_print(
                            '-----------------------------------' + timestamp + ' ' + app_name + ' 结束-----------------------------------')
                        log_print('\n\n')
                        return


            is_exist = device(textStartsWith="领取奖励").exists()
            if is_exist:
                device(textStartsWith="领取奖励").click()
                time.sleep(22)

            else:
                is_exist = device(textStartsWith="领取额外金币").exists()
                if is_exist:
                    device.click(825,915) #关闭"本次有额外xxx金币"弹窗
                    time.sleep(3)
                    log_print('关闭"本次有额外xxx金币"弹窗成功')

                    go_back_desktop(device)
                    timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
                    log_print(
                        '-----------------------------------' + timestamp + ' ' + app_name + ' 结束-----------------------------------')
                    log_print('\n\n')
                    return

            if time.time() - start_time >= TIMEOUT:
                log_print("已运行30分钟，退出循环")

                go_back_desktop(device)
                timestamp = datetime.now().strftime("%Y-%m-%d %H：%M：%S")
                log_print(
                    '-----------------------------------' + timestamp + ' ' + app_name + ' 结束-----------------------------------')
                log_print('\n\n')
                return


##主程序
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    d = u2.connect()
    # print(d.app_current()['package'])  #com.luna.music
    # print(d.app_current()['activity']) #com.luna.biz.main.main.MainActivity
    # print(d.app_current()['pid']) #29690

    #d.app_start('com.luna.music','com.luna.biz.main.main.MainActivity')
    #d.app_stop('com.luna.music')

    #d.screen_on()
    #d.swipe(500, 2580, 500, 800)

    #d.swipe_ext('up', scale=0.6)
    #d.swipe_ext('down', scale=0.6)
    #d.swipe_ext('left', scale=0.6)
    #d.swipe_ext('right', scale=0.6)

    #d(textContains='看广告得金币', className='android.widget.TextView').click()
    #d(textContains='点可领', className='android.widget.Button').click()
    #print(d(textContains='看视频赚金币').info)
    #print(d.info)





    while True:
        HonGuoDuanju(d,30)
        kuaishoujisuban(d, 5)
        kuaishoujisuban_kanGuangGao(d,10)

    # print(d(textContains='去赚钱')[0].info)
    # print(d(text='我').info)
    # print(d(text='我').child())

    #d.xpath('//android.webkit.WebView/android.view.View[2]/android.view.View[1]/android.view.View[1]').click()













