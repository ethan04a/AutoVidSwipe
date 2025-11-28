import uiautomator2
import uiautomator2 as u2

from singleton_logger import logger
from auto_video_swipter import video_swipter
import time
import threading
import subprocess
import re

def get_adb_devices() -> list[str]:
    """
    调用 adb devices 命令，提取已连接设备的 IP:端口 字符串列表

    返回值：
        list[str]: 设备地址列表（格式如 ["192.168.31.55:41297", ...]），无设备时返回空列表
    """
    devices = []
    try:
        # 执行 adb devices 命令，捕获输出（忽略错误输出）
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        # 检查命令是否执行成功（返回码为0）
        if result.returncode != 0:
            return devices

        # 按行分割输出内容
        output_lines = result.stdout.strip().split("\n")

        # 正则表达式：匹配 IP:端口 格式（支持IPv4地址和任意端口号）
        device_pattern = re.compile(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})\s+device$")

        # 遍历输出行（跳过第一行标题）
        for line in output_lines[1:]:
            line = line.strip()
            if not line:
                continue  # 跳过空行

            # 匹配设备地址和状态（只保留状态为 device 的设备）
            match = device_pattern.match(line)
            if match:
                devices.append(match.group(1))

    except FileNotFoundError:
        # 处理 adb 命令未找到的情况
        print("警告：未找到 adb 命令，请确保 adb 已添加到系统环境变量")
    except Exception as e:
        # 处理其他未知异常
        print(f"获取设备列表失败：{str(e)}")

    return devices


####----------------------------------------汽水音乐-----------------------------------------------
def qisuiyinyue_qufanka(d:uiautomator2.Device): #翻卡游戏

    if not video_swipter.has_popup(d,'翻卡赢金币'):
        d.swipe_ext('up')
        time.sleep(2)
        print('没找到 翻卡赢金币游戏 向上翻')

    if not video_swipter.has_popup(d, '去翻卡'):
        print('没有找到去翻卡按钮')
        return

    if video_swipter.claim_treasure_box(d, "翻卡赢金币"):
        time.sleep(2)
        print('点击 翻卡赢金币')

        flag_count = 0
        while not video_swipter.has_popup(d, "直接领取"):

            if video_swipter.claim_treasure_box(d,'广告翻'):
                time.sleep(5)
                while d(textContain='秒后可领奖励，关闭，按钮').exists():
                    time.sleep(1)
                if d(text="获得奖励，关闭，按钮").exists():
                    d(text="获得奖励，关闭，按钮").click()
                    time.sleep(2)
            else:
                flag_count +=1
                print('异常计数器加1')
                if flag_count>10:
                    print('异常退出')
                    break

        video_swipter.claim_treasure_box(d,'直接领取')
        print('翻卡牌游戏结束')

def qisuiyinyue_kanguanggao(d:uiautomator2.Device):
    guanggao_flag = False

    if video_swipter.has_popup(d, "看广告膨胀领"):
        d.click(0.473, 0.687)
        guanggao_flag = True


    if not video_swipter.claim_treasure_box(d, '开宝箱得金币'):  #领取宝箱
        logger.log('没发现宝箱')

        if not video_swipter.has_popup(d, "我的资产"):
            d.swipe_ext('down')

        if not video_swipter.claim_treasure_box(d, '看广告赚金币'):
            logger.log('看广告赚金币 失败')
        else:
            logger.log('成功点击看广告赚金币')
            guanggao_flag = True
    else:
        guanggao_flag = True

    time.sleep(2)

    if d.xpath('//*[@resource-id="com.luna.music:id/uj"]/android.widget.FrameLayout[1]/com.lynx.tasm.behavior.ui.LynxFlattenUI[9]').exists:

        logger.log('进入逛街得金币界面')

        if d(text='返回按钮').exists():
            d(text="返回按钮").click()
            time.sleep(2)

        if d(text='坚持退出').exists():
            d(text="坚持退出").click()
            logger.log('从逛街得金币界面返回')

    if d.xpath('//*[@resource-id="com.luna.music:id/isq"]/android.widget.LinearLayout[1]').exists:

        logger.log('进入异常界面')
        d.xpath('//*[@resource-id="com.luna.music:id/isq"]/android.widget.LinearLayout[1]').click()
        time.sleep(2)
        logger.log('退出异常界面')

    if video_swipter.has_popup(d, "看广告膨胀领"):
        d.click(0.473, 0.687)
        guanggao_flag = True

    time.sleep(2)

    while guanggao_flag:
        while d(textContains="秒后可领奖励").exists():
            logger.log('看广告中...')
            time.sleep(1)

        if d(textContains="继续观看").exists():
            d(textContains='继续观看').click()
            logger.log('点击 继续观看广告')
            time.sleep(2)

        if d(text="领取奖励").exists():
            d(text="领取奖励").click()
            logger.log('点击 领取奖励')
            time.sleep(2)

        if d(text='广告').exists() == False:
            d.click(0.473, 0.552)
            print('广告模式退出')
            break


def qisuiyinyue(d:uiautomator2.Device):

    if video_swipter.start_app(d, 'com.luna.music'):  # 汽水音乐

        time.sleep(10)

        target_element = d.xpath(
            '//*[@resource-id="com.luna.music:id/navigation_tab_commerce_coin"]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]')
        target_element.click()

        logger.log('进入福利界面')
        time.sleep(5)

        for i in range(5):
            qisuiyinyue_kanguanggao(d)
            qisuiyinyue_qufanka(d)

        video_swipter.close_app(d, 'com.luna.music')


####----------------------------------------红果短剧-----------------------------------------------
def hongguoduanju_kuanju(d:uiautomator2.Device,max_count:int):

    d(text='剧场').click()
    logger.log('进入短剧看视频')
    time.sleep(5)

    d.click(0.254, 0.355)
    logger.log('选剧')
    time.sleep(2)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('up', 0.5)
        logger.log("已执行向上滑动")
        time.sleep(40)
        count += 1
        logger.log('完成次数：' + str(count))


def hongguoduanju_kuanguanggao(d:uiautomator2.Device):

    d(text='赚钱').click()
    logger.log('进入赚钱界面')
    time.sleep(5)

    flag = False
    if video_swipter.claim_treasure_box(d, '开宝箱得金币'):
        time.sleep(3)
        logger.log('点击宝箱')
        if video_swipter.has_popup(d, '点击看视频最高再领'):
            d.click(0.494, 0.608)
            time.sleep(2)
            flag = True
            logger.log('点击看视频最高再领xxx金币按钮')
        else:
            return
    else:
        if video_swipter.claim_treasure_box(d, '看视频赚海量金币'):
            time.sleep(2)
            logger.log('点击 看视频赚海量金币')
            flag = True

    flag_count = 0
    while flag:

        while not video_swipter.has_popup(d, '领取成功'):
            print('看广告中...')
            time.sleep(10)

        d.click(0.908, 0.065)
        time.sleep(2)
        print('点击 右上角 领取成功标签')

        if video_swipter.has_popup(d, '领取奖励'):
            d.click(0.48, 0.549)
            time.sleep(2)
            print('点击 领取奖励按钮')

        elif video_swipter.has_popup(d, '开心收下'):
            d.click(0.484, 0.625)
            time.sleep(2)
            print('点击 开心收下按钮')
            break

        else:
            flag_count +=1
            if flag_count>10:
                flag = False


def hongguoduanju(d:uiautomator2.Device):

    if video_swipter.start_app(d, 'com.phoenix.read'):  # 红果短剧

        time.sleep(10)

        #hongguoduanju_kuanju(d,30)
        for i in range(5):
            hongguoduanju_kuanguanggao(d)

        video_swipter.close_app(d, 'com.phoenix.read')

####----------------------------------------快手极速版-----------------------------------------------
def kuaisoujisuban_kanshipin(d:uiautomator2.Device,max_count:int):

    d(text='首页').click()
    logger.log('进入首页看视频')
    time.sleep(5)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('up', 0.5)
        logger.log("已执行向上滑动")
        time.sleep(40)
        count += 1
        logger.log('完成次数：' + str(count))

def kuaisoujisuban(d:uiautomator2.Device):

    d.press("volume_mute") #静音
    time.sleep(4)

    if video_swipter.start_app(d, 'com.kuaishou.nebula'):  # 红果短剧

        time.sleep(10)

        if d(text='同意并继续').exists():
            d(text='同意并继续').click()
            time.sleep(2)
            logger.log('出现协议弹窗，已经点掉')

        if d(text='允许').exists():
            d(text='允许').click()
            time.sleep(2)
            logger.log('通知权限弹窗，已经点掉')


        kuaisoujisuban_kanshipin(d,30)


        video_swipter.close_app(d, 'com.kuaishou.nebula')

####----------------------------------------河马剧场-----------------------------------------------
def hemajuchang_kanshipin(d:uiautomator2.Device,max_count:int):

    d(text='剧场').click()
    logger.log('进入剧场看视频')
    time.sleep(5)

    d.click(d.info['displayWidth']/2, d.info['displayHeight']/2)
    logger.log('选剧')
    time.sleep(2)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('up', 0.5)
        logger.log("已执行向上滑动")
        time.sleep(40)
        count += 1
        logger.log('完成次数：' + str(count))

def hemajuchang(d:uiautomator2.Device):
    if video_swipter.start_app(d, 'com.dz.hmjc'):  # 红果短剧

        time.sleep(10)

        hemajuchang_kanshipin(d,30)


        video_swipter.close_app(d, 'com.dz.hmjc')

####----------------------------------------番茄畅听-----------------------------------------------
def fanqiechangting_kanshipin(d:uiautomator2.Device,max_count:int):

    d(text='短剧').click()
    logger.log('进入短剧看视频')
    time.sleep(5)

    d.click(0.254, 0.655)
    logger.log('选剧')
    time.sleep(2)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('up', 0.5)
        logger.log("已执行向上滑动")
        time.sleep(40)
        count += 1
        logger.log('完成次数：' + str(count))

def fanqiechangting(d:uiautomator2.Device):
    if video_swipter.start_app(d, 'com.xs.fm'):  # 番茄畅听

        time.sleep(10)

        fanqiechangting_kanshipin(d,30)


        video_swipter.close_app(d, 'com.xs.fm')

####----------------------------------------西瓜视频-----------------------------------------------
def xiguashipin_kanshipin(d:uiautomator2.Device,max_count:int):


    if d(text='免费短剧').exists():
        d(resourceId="com.ss.android.article.video:id/+", text='免费短剧').click()
    else:
        d(resourceId="com.ss.android.article.video:id/+", text="短剧").click()


    logger.log('进入短剧看视频')
    time.sleep(5)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('up',0.5)
        logger.log("已执行向上滑动")
        time.sleep(40)
        count += 1
        logger.log('完成次数：' + str(count))

def xiguashipin(d:uiautomator2.Device):
    if video_swipter.start_app(d, 'com.ss.android.article.video'):  # 西瓜视频

        time.sleep(10)

        xiguashipin_kanshipin(d,30)


        video_swipter.close_app(d, 'com.ss.android.article.video')


def xishuashua(d:uiautomator2.Device):


    fanqiechangting(d) #番茄畅听

    kuaisoujisuban(d) #快手极速版

    hemajuchang(d) #河马剧场

    xiguashipin(d)  # 西瓜视频

    qisuiyinyue(d) # 汽水音乐

    hongguoduanju(d) #红果短剧



if __name__ == "__main__":

    logger.log('启动脚本！')

    devices_list = get_adb_devices()
    thread_list = []

    for device_name in devices_list:
        d = u2.connect(device_name)
        logger.log(d.info)
        t = threading.Thread(target=xishuashua, args=(d,))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    # d = u2.connect()
    # print(d.info)

    print('脚本执行完成！')

















