import uiautomator2
import uiautomator2 as u2

from singleton_logger import logger
from auto_video_swipter import video_swipter
import time
import threading
import subprocess
import re

from singleton_screenshot import screenshoter
import datetime
import sys

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
        logger.log("警告：未找到 adb 命令，请确保 adb 已添加到系统环境变量")
    except Exception as e:
        # 处理其他未知异常
        logger.log(f"获取设备列表失败：{str(e)}")

    return devices


####----------------------------------------汽水音乐-----------------------------------------------
def qisuiyinyue_qufanka(d:uiautomator2.Device): #翻卡游戏

    if not video_swipter.has_popup(d,'翻卡赢金币'):
        d.swipe_ext('up')
        time.sleep(2)
        logger.log('没找到 翻卡赢金币游戏 向上翻')

    if video_swipter.claim_treasure_box(d, "翻卡赢金币"):
        time.sleep(2)
        logger.log('点击 翻卡赢金币')

        if d(resourceId="com.luna.music:id/navigation_tab_me").exists():
            logger.log('翻卡赢金币时间没到 点击无效 退出函数')
            return

        flag_count = 0
        while (video_swipter.has_popup(d, "看广告翻十位卡")
               or video_swipter.has_popup(d, "看广告翻百位卡")
               or video_swipter.has_popup(d, "看1个广告翻千位卡")):

            d.click(0.495, 0.524)

            time.sleep(5)

            if flag_count>10:
               logger.log('异常退出')
               break

            while d(textContains='秒后可领奖励，关闭，按钮').exists():
                time.sleep(1)
            if d(text="获得奖励，关闭，按钮").exists():
                d(text="获得奖励，关闭，按钮").click()
                time.sleep(2)
            else:
                flag_count+=1

        video_swipter.claim_treasure_box(d,'直接领取')
        logger.log('翻卡牌游戏结束')

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

    if d(resourceId="com.luna.music:id/c4p").exists():
        d(resourceId="com.luna.music:id/bq5").click()
        time.sleep(2)
        logger.log('退出直播界面')

    time.sleep(2)

    while guanggao_flag:
        while d(textContains="秒后可领奖励").exists():
            logger.log('看广告中...')
            time.sleep(1)

        if d(text="继续观看，关闭，按钮").exists():
            d(text='继续观看，关闭，按钮').click()
            logger.log('点击 继续观看广告')
            time.sleep(2)

        if d(text="继续观看").exists():
            d(text='继续观看').click()
            logger.log('点击 继续观看广告')
            time.sleep(2)

        if d(text="领取奖励").exists():
            d(text="领取奖励").click()
            logger.log('点击 领取奖励')
            time.sleep(2)

        if d(resourceId="com.luna.music:id/b+").exists():
            d(resourceId="com.luna.music:id/b+").click()
            logger.log('点击 关闭遮蔽弹窗')
            time.sleep(2)


        if not d(text='广告').exists():
            d.click(0.473, 0.552)
            logger.log('广告模式退出')
            break


def qisuiyinyue(d:uiautomator2.Device):

    if video_swipter.start_app(d, 'com.luna.music'):  # 汽水音乐

        time.sleep(10)

        # 汽水音乐
        # 开通会员畅听千万曲库 弹窗 一打开软件就有
        if video_swipter.has_popup(d,'开通会员畅听千万曲库'):
            d.click(0.897, 0.4) #关闭弹窗
            time.sleep(2)
            logger.log('开通会员畅听千万曲库')

        # 恭喜获得VIP听歌时常
        if video_swipter.has_popup(d,'恭喜获得VIP听歌时长'):
            d.click(0.494, 0.642) # 狠心离开位置
            time.sleep(2)
            logger.log('恭喜获得VIP听歌时长')

        target_element = d.xpath(
            '//*[@resource-id="com.luna.music:id/navigation_tab_commerce_coin"]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]')
        target_element.click()
        logger.log('进入福利界面')



        time.sleep(5)


        for i in range(1):
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
        if video_swipter.has_popup(d,'点击看视频最高再领'):
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

        while not video_swipter.has_popup(d,'领取成功'):
            logger.log('看广告中...')
            time.sleep(10)

        d.click(0.908, 0.065)
        time.sleep(2)
        logger.log('点击 右上角 领取成功标签')

        if video_swipter.has_popup(d,'领取奖励'):
            d.click(0.48, 0.549)
            time.sleep(2)
            logger.log('点击 领取奖励按钮')

        elif video_swipter.has_popup(d, '开心收下'):
            d.click(0.484, 0.625)
            time.sleep(2)
            logger.log('点击 开心收下按钮')
            break

        else:
            flag_count +=1
            if flag_count>10:
                flag = False


def hongguoduanju(d:uiautomator2.Device):

    if video_swipter.start_app(d, 'com.phoenix.read'):  # 红果短剧

        time.sleep(10)

        hongguoduanju_kuanju(d,40)

        # 红果免费短剧
        # 到赚钱界面 弹窗 今日签到领
        # d.click(0.491, 0.636) #立即签到 按钮
        # 两秒以后
        # d.click(0.494, 0.761) #关闭弹窗

        # for i in range(5):
        #     hongguoduanju_kuanguanggao(d)

        video_swipter.close_app(d, 'com.phoenix.read')

####----------------------------------------快手极速版-----------------------------------------------
def kuaisoujisuban_kanguanggao(d:uiautomator2.Device):

    d(text='去赚钱').click()
    time.sleep(2)
    logger.log('进入到赚钱界面')

    # 到 去赚钱界面 弹窗 连续签到
    if video_swipter.has_popup(d,'连续签到'):
        d.click(0.236, 0.665) #直接领金币按钮
        time.sleep(3)
        logger.log('点击 直接领金币')
        # 弹出去看视频弹窗
        d.click(0.915, 0.157) #关闭弹窗
        time.sleep(3)
        logger.log('点击 关闭弹窗')

    if d(textStartsWith='去看广告得最高').exists():
        d(textStartsWith='去看广告得最高').click()
        time.sleep(2)
        logger.log('点击 去看广告得最高xxx金币 按钮')

    elif d(textStartsWith='点可领').exists():

        d(textStartsWith='点可领').click()
        time.sleep(2)
        logger.log('点击宝箱')

        if d(textStartsWith='去看广告得最高').exists():
            d(textStartsWith='去看广告得最高').click()
            time.sleep(2)
            logger.log('点击 去看广告得最高xxx金币 按钮')

    elif d(text="看广告得金币").exists():

        d(text="看广告得金币").click()
        time.sleep(2)
        logger.log('点击 看广告得金币')

        if d(text="去微信邀请好友").exists():
            d.click(0.922, 0.173)
            time.sleep(2)
            logger.log('点掉 去微信邀请好友')

    else:
        logger.log('界面异常')
        return

    while not d(resourceId="android:id/text1", text="去赚钱").exists(): #判断条件是是否回到赚钱界面

        while d(textContains='后可领取').exists():
            time.sleep(1)
            if d(resourceId="com.kuaishou.nebula:id/left_btn").exists():
                d(resourceId="com.kuaishou.nebula:id/left_btn").click()
                time.sleep(2)
            logger.log('看广告中...')

        if d(textContains='已成功领取').exists():
            d(textContains='已成功领取').click()
            time.sleep(2)

        if d(text="领取奖励").exists():
            d(text="领取奖励").click()
            time.sleep(2)

        if d(textContains='领取额外').exists():

            time.sleep(2)
            if d(description="close_view").exists():
                d(description="close_view").click()
                time.sleep(2)

            logger.log('关闭 领取额外奖励 弹窗')

        if d(resourceId="com.kuaishou.nebula:id/left_btn").exists():
            d(resourceId="com.kuaishou.nebula:id/left_btn").click()
            time.sleep(2)

        if d(text='更多直播').exists() or d(text='卖货频道').exists():
            time.sleep(35)
            d.swipe(0, 600, 1000, 600)
            logger.log('退出直播')

            if d(text='开心收下').exists():
                d(text='开心收下').click()
                time.sleep(2)
                d.swipe(0, 600, 1000, 600)
                logger.log('开心收下')

            time.sleep(3)
            if d(text='换一个广告').exists():
                d(text='换一个广告').click()
                logger.log('换一个广告')

def kuaisoujisuban_kanshipin(d:uiautomator2.Device,max_count:int):

    d(text='首页').click()
    logger.log('进入首页看视频')
    time.sleep(5)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('up', 0.5)
        logger.log("已执行向上滑动")
        time.sleep(20)
        count += 1
        logger.log('完成次数：' + str(count))

def kuaisoujisuban(d:uiautomator2.Device):

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

        # 快手极速版
        if d(text='邀请2个新用户必得').exists:
            d.click(0.491, 0.701)



        kuaisoujisuban_kanshipin(d,30)

        for i in range(30):
            kuaisoujisuban_kanguanggao(d)


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

        # 河马剧场  到赚钱界面  连续签到得金币
        # d.click(0.498, 0.668) #立即签到按钮
        # d.click(0.498,0.668) #看小视频最高再领xxx金币 按钮
        # d.click(0.858, 0.205) #弹窗左上角关闭图标

        hemajuchang_kanshipin(d,50)


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

        time.sleep(15)

        if video_swipter.has_popup(d,'番茄畅听用户专属福利'):
            d.click(0.497, 0.741)  # 放弃奖励不再提醒
            time.sleep(2)
            logger.log('点掉 番茄畅听用户专属福利')

        # 番茄畅听 一进界面 昨日收益弹窗  昨日受益超过99%用户弹窗
        if video_swipter.has_popup(d,'昨日收益超过'):
            d(text='放弃奖励，不再提醒').click()  # 放弃奖励不再提醒
            time.sleep(2)
            logger.log('点掉 昨日收益超过99%用户弹窗')

        # 去 领现金 的界面 -> 今日签到领
        # d.click(0.265, 0.641) #立即签到 按钮 过两秒以后再点关闭弹窗按钮
        # d.click(0.487, 0.756) #弹窗关闭按钮

        fanqiechangting_kanshipin(d,50)


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

        # 西瓜视频
        # 赚界面 弹窗 评价并签到
        # d.click(0.487, 0.599) #评价并签到 按钮
        # 过两秒
        # d.click(0.498, 0.732) #关闭弹窗按钮
        # 弹窗 获得开宝箱奖励
        # d.click(0.48, 0.698) #开心收下按钮
        # 弹窗 恭喜获得预约金币
        # d.click(0.487, 0.801) #关闭弹窗

        xiguashipin_kanshipin(d,50)


        video_swipter.close_app(d, 'com.ss.android.article.video')
#-----------------------------------------抖音极速版--------------------------------------------------
def douyinjisuban_kanguanggao(d:uiautomator2.Device):

    if d.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/root_view"]/android.widget.FrameLayout[4]').exists:
        d.click(0.49, 0.964)
        time.sleep(2)
        logger.log('去赚钱')

    d.swipe_ext('down',1)
    time.sleep(2)
    logger.log('向下翻')

    flag = False
    if d(description="开宝箱得金币").exists():
        d(description="开宝箱得金币").click()
        time.sleep(2)
        logger.log('开宝箱')
        flag = True
    else:
        for i in range(10):
            if not d(description="每5分钟完成一次广告任务，单日最高可赚20000金币").exists():
                d.swipe_ext('up',0.1)
                time.sleep(1)
            else:
                d(description="每5分钟完成一次广告任务，单日最高可赚20000金币").click()
                time.sleep(2)
                flag = True


    if d(description="金币").exists():
        d.click(0.53, 0.559)
        time.sleep(2)
        logger.log('看广告')

    while flag:

        if d(description="更多").exists():
            logger.log('未正常进入广告模式')
            break

        while not d(description="领取成功，关闭，按钮").exists():
            time.sleep(1)
            logger.log('看广告中...')
            if d(resourceId="com.ss.android.ugc.aweme.lite:id/tv_title").exists():
                d.click(0.05, 0.079)
                time.sleep(2)
                logger.log('退出 应用外联广告页')

        time.sleep(2)

        if d(description="领取成功，关闭，按钮").exists():
            d(description="领取成功，关闭，按钮").click()
            time.sleep(3)
            logger.log('点击 领取奖励按钮')

        if video_swipter.has_popup(d,'再看一个视频额外获得'):
            d.click(0.53, 0.559)
            time.sleep(2)
            logger.log('点击 领取奖励 弹窗按钮')

        if d(description="金币").exists():
            d.click(0.796, 0.358)
            time.sleep(2)
            logger.log('退出广告模式')
            break

    d.swipe_ext('right',0.7)
    time.sleep(2)
    logger.log('退出赚钱模式')


def douyinjisuban_kushipin(d:uiautomator2.Device,max_count:int):

    if d.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/root_view"]/android.widget.FrameLayout[1]').exists:
        d.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/root_view"]/android.widget.FrameLayout[1]').click()
        logger.log('进入看视频')
        time.sleep(5)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('up',0.5)
        logger.log("已执行向上滑动")
        time.sleep(20)
        count += 1
        logger.log('完成次数：' + str(count))

def douyinjisuban(d:uiautomator2.Device):

    if video_swipter.start_app(d, 'com.ss.android.ugc.aweme.lite'):  # 抖音极速版

        time.sleep(10)

        # 抖音极速版
        # 到赚钱按钮
        # 弹窗 连续签到赚大钱
        if video_swipter.has_popup(d,'连续签到赚大钱'):
            d.click(0.484, 0.605)  # 签到领
            time.sleep(2)
            d.click(0.798, 0.331)  # 关闭弹窗位置
            time.sleep(2)
            logger.log('连续签到赚大钱')

        if video_swipter.has_popup(d,'立即签到领'):
            d.click(0.491, 0.889) #立即签到领 按钮位置
            time.sleep(2)
            d.click(0.929, 0.288)  # 关闭按钮
            logger.log('立即签到领')

        if video_swipter.has_popup(d,'马上打开'):
            d.click(0.505, 0.828)  # 关闭弹窗
            time.sleep(2)
            logger.log('马上打开')


        douyinjisuban_kushipin(d,50)  #抖音刷视频

        douyinjisuban_kanguanggao(d) #抖音看广告


        video_swipter.close_app(d, 'com.ss.android.ugc.aweme.lite')
#-----------------------------------------悟空浏览器--------------------------------------------------
def wukongliulanqi_kushipin(d:uiautomator2.Device,max_count:int):

    if d(text='视频').exists:
        d(text='视频').click()
        logger.log('进入看视频')
        time.sleep(5)

        if d(description="短剧").exists:
            d(description="短剧").click()
            logger.log('进入看短剧')
            time.sleep(5)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('up',0.5)
        logger.log("已执行向上滑动")
        time.sleep(40)

        if count==2:
            if d(resourceId="com.cat.readall:id/gh5").exists:
                d(resourceId="com.cat.readall:id/gh5").click()
                logger.log('进入看短剧模式')
                time.sleep(2)

        count += 1
        logger.log('完成次数：' + str(count))

    if d(resourceId="com.cat.readall:id/dms").exists():
        d(resourceId="com.cat.readall:id/dms").click()
        time.sleep(2)
        logger.log('退出看短剧模式')


def wukongliulanqi(d:uiautomator2.Device):
    if video_swipter.start_app(d, 'com.cat.readall'):  # 悟空浏览器

        time.sleep(10)
        # 悟空浏览器
        # 去赚钱界面
        # 今日签到领弹窗
        # d.click(0.303, 0.698) #立即领取按钮
        # 两秒以后
        # d.click(0.869, 0.312) #关闭弹窗

        wukongliulanqi_kushipin(d,20)


        video_swipter.close_app(d, 'com.cat.readall')
#------------------------------------番茄免费小说----------------------------------------------------
def fanqiemianfeixiaosuo_duxiaosuo(d:uiautomator2.Device,max_count:int):

    if d(text='书架').exists:
        d(text='书架').click()
        logger.log('进入书架频')
        time.sleep(5)

        d.click(0.158, 0.243)
        time.sleep(2)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('left',0.5)
        logger.log("已执行左滑动")
        time.sleep(20)

        count += 1
        logger.log('完成次数：' + str(count))

    d.swipe_ext('left')
    d.swipe_ext('left')
    logger.log('退出看短剧模式')



def fanqiemianfeixiaosuo(d:uiautomator2.Device):


    if video_swipter.start_app(d, 'com.dragon.read'):  # 悟空浏览器

        time.sleep(10)
        # 番茄免费小说
        # 一进软件 就有 立即领取弹窗
        if video_swipter.has_popup(d,'立即领取'):
            d.click(0.494, 0.631) #立即领取 按钮
            time.sleep(3)
            logger.log('立即领取')
            d.click(0.491, 0.777) #关闭弹窗
            time.sleep(2)
            logger.log('关闭弹窗')

        fanqiemianfeixiaosuo_duxiaosuo(d,50)


        video_swipter.close_app(d, 'com.dragon.read')

#-----------------------------------------百度极速版-----------------------------------------------------------
def baidujisuban_kanshipin(d:uiautomator2.Device,max_count:int):

    if d(text='短剧').exists:
        d(text='短剧').click()
        logger.log('进入看短剧')
        time.sleep(5)

        if d.xpath('//*[@resource-id="com.baidu.searchbox.lite:id/video_flow_cmp_list"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').exists:
            d.xpath(
                '//*[@resource-id="com.baidu.searchbox.lite:id/video_flow_cmp_list"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]').click()
            time.sleep(2)

    count = 0
    while count < max_count:
        #d.swipe(500, 1500, 500, 100)
        d.swipe_ext('up',0.8)
        logger.log("已执行上滑动")
        time.sleep(20)

        count += 1
        logger.log('完成次数：' + str(count))

    d.swipe_ext('right')
    time.sleep(2)

    if d(text='百度').exists:
        d(text='百度').click()
        logger.log('回到首页')
        time.sleep(2)


def baidujisuban(d:uiautomator2.Device):

    logger.log(d.app_current())

    if video_swipter.start_app(d, 'com.baidu.searchbox.lite'):  #百度极速版

        # 百度极速版
        # 一进软件 去阅读赚赚更多
        if video_swipter.has_popup(d,'去阅读赚赚更多'):
            d.click(0.773, 0.415) #关闭弹窗
            time.sleep(2)
            logger.log('点掉 去阅读赚赚更多')

        # 专属现金福利弹窗
        if video_swipter.has_popup(d,'专属现金福'):
            d.click(0.848, 0.267) #关闭弹窗
            time.sleep(2)
            logger.log('点掉 专属现金福')

        # 直接领取弹窗
        if video_swipter.has_popup(d,'直接领取'):
            d.click(0.282, 0.724) #直接领取 按钮
            time.sleep(2)
            d.click(0.855, 0.179)  # 关闭弹窗
            time.sleep(2)
            logger.log('点掉 专属现金福')

        baidujisuban_kanshipin(d,50)

        video_swipter.close_app(d, 'com.baidu.searchbox.lite')  #百度极速版




def xishuashua(d:uiautomator2.Device):

    # d.screen_on()
    # time.sleep(2)
    #
    # if d.app_current()['package']=='com.ximalaya.ting.android':
    #     d.swipe_ext('right',0.8)
    #     time.sleep(2)
    #     logger.log('喜马拉雅正在运行')
    #
    # d.swipe_ext('up',0.5)
    # time.sleep(2)
    #
    d.press('volume_up')
    time.sleep(2)
    d.press("volume_mute") #静音
    time.sleep(4)

    for i in range(2):

        try:
            hemajuchang(d) #河马剧场
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        try:
            fanqiechangting(d) #番茄畅听
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        try:
            xiguashipin(d)  # 西瓜视频
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        try:
            baidujisuban(d) #百度极速版
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        try:
            kuaisoujisuban(d) #快手极速版
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        try:
            fanqiemianfeixiaosuo(d) #番茄免费小说
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        try:
            douyinjisuban(d) #抖音极速版
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        try:
            qisuiyinyue(d) # 汽水音乐
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        try:
            hongguoduanju(d) #红果短剧
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        try:
            wukongliulanqi(d) #悟空浏览器
        except Exception as e:
            logger.log('发生异常:'+str(e))
            logger.log(screenshoter.capture_screen(d))

        d.app_stop_all()
        time.sleep(2)
        d.drag(500,2638,500,1500,duration=7)
        time.sleep(2)
        d.click(0.487, 0.903)
        time.sleep(2)
        d.screen_off()

def force_shutdown_windows():
    try:
        # 直接执行强制关机命令，无任何提示和确认
        subprocess.run(
            ["shutdown", "/p"],
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        logger.log(f"关机命令执行失败：{e.stderr}")
        sys.exit(1)
    except Exception as e:
        logger.log(f"未知错误：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":


    # target_time = datetime.datetime.strptime("2025-12-1 03:00:00", "%Y-%m-%d %H:%M:%S")
    # now = datetime.datetime.now()
    # time_diff = (target_time - now).total_seconds()
    # logger.log(f"距离任务执行还有：{time_diff:.0f}秒（{time_diff/3600:.1f}小时）")
    # time.sleep(time_diff)

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
    # logger.log(d.info)

    logger.log('脚本执行完成！')
    #force_shutdown_windows()

















