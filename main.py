import uiautomator2
import uiautomator2 as u2

from singleton_logger import logger
from auto_video_swipter import video_swipter
import time

####----------------------------------------汽水音乐-----------------------------------------------
def qisuiyinyue_kanguanggao(d:uiautomator2.Device):
    guanggao_flag = False

    if video_swipter.has_popup(d, "看广告膨胀领"):
        d.click(0.473, 0.687)
        guanggao_flag = True


    if video_swipter.claim_treasure_box(d, '开宝箱得金币') == False:  #领取宝箱
        logger.log('没发现宝箱')

        if video_swipter.claim_treasure_box(d, '看广告赚金币') == False:
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

        video_swipter.close_app(d, 'com.luna.music')


####----------------------------------------红果短剧-----------------------------------------------
def hongguoduanju_kuanju(d:uiautomator2.Device,max_count:int):

    d(text='首页').click()
    logger.log('进入首页看短剧')
    time.sleep(5)

    count = 0
    while count < max_count:
        d.swipe(500, 1500, 500, 100)
        logger.log("已执行向上滑动")
        time.sleep(18)
        count += 1
        logger.log('完成次数：' + str(count))


def hongguoduanju_kuanguanggao(d:uiautomator2.Device):

    d(text='赚钱').click()
    logger.log('进入赚钱界面')
    time.sleep(5)

    baoxiang = d.xpath('//*[@resource-id="com.phoenix.read:id/ase"]/android.widget.FrameLayout[1]/android.widget.ScrollView[2]/android.widget.HorizontalScrollView[1]/android.widget.LinearLayout[1]/android.view.ViewGroup[1]')
    if baoxiang.exists and video_swipter.has_popup(d, '开宝箱得金币'):
        baoxiang.click()
        time.sleep(3)
        logger.log('点击宝箱')
        if video_swipter.has_popup(d, '点击看视频最高再领'):
            d.click(0.494, 0.608)
            time.sleep(2)
            logger.log('点击看视频最高再领xxx金币按钮')
        else:
            return
    else:
        d.xpath(
            '//*[@resource-id="com.phoenix.read:id/ase"]/android.widget.FrameLayout[1]/android.widget.ScrollView[1]/android.widget.HorizontalScrollView[1]/android.widget.LinearLayout[1]/android.view.ViewGroup[3]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
        time.sleep(2)
        logger.log('点击 看视频赚海量金币')

    while True:

        while video_swipter.has_popup(d, '领取成功') == False:
            print('看广告中...')
            time.sleep(10)

        d.click(0.908, 0.065)
        time.sleep(2)
        print('点击 右上角 领取成功标签')

        elem_popu=d.xpath('//*[@resource-id="com.phoenix.read:id/cx4"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[2]')
        if elem_popu.exists:
            d.click(0.48, 0.549)
            time.sleep(2)
            print('点击 领取奖励按钮')

        elem_popu=d.xpath(
            '//*[@resource-id="com.phoenix.read:id/ase"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]')
        if elem_popu.exists:
            d.click(0.484, 0.625)
            time.sleep(2)
            print('点击 开心收下按钮')
            break






def hongguoduanju(d:uiautomator2.Device):

    if video_swipter.start_app(d, 'com.phoenix.read'):  # 红果短剧

        time.sleep(10)

        hongguoduanju_kuanju(d,10)
        hongguoduanju_kuanguanggao(d)

        video_swipter.close_app(d, 'com.phoenix.read')



if __name__ == "__main__":

    logger.log('启动脚本')
    d = u2.connect()
    logger.log(d.info)

    #qisuiyinyue(d) #汽水音乐
    #com.kuaishou.nebula 快手
    #com.phoenix.read 红果短剧
    for i in range(5):
        hongguoduanju_kuanguanggao(d)

    print(d.app_current())

















