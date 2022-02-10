"""酷狗音乐分类下载器
方法调用过程：
运行TK程序后展示支持的所有分类信息（radio）
1、根据用户输入的音乐ID和分类名称获取该分类列表，默认每页20条
2、根据分类音乐列表获得音乐下载地址
3、请求下载地址保存音乐到本地（保存位置用户配置）
"""
import time
from tkinter import *
from tkinter import scrolledtext
import os
import threading
import requests
import re
import json
from tkinter.filedialog import askdirectory

LOG_LINE_NUM = 0


class MY_GUI:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.radio = "KTV必点曲73，中国潮音1661，唱作人21294，乐队无限公司1144，新声请指教1138，音浪合伙人1086，明日之子1064，创造营20191046，这！就是原创1034，蒙面唱将猜猜猜996" \
                     "，中国新说唱978，创造101964，嗨，唱起来！969，歌手953，网络红歌2，中文经典5，伤感网络情歌268，最爱成名曲63，点歌台1660，酷狗热歌1，中国好声音1076，那年MP3里的歌693" \
                     "，店铺175，老情歌276，热评10W+歌曲974，世界级热门单曲839，情歌对唱61，酷狗新歌4，中国有嘻哈911，我是歌手627，厉害了!我的歌877，围炉音乐会858，中文DJ3，抖音最火DJ1094" \
                     "，由你音乐榜991，国创ACG975，神曲144，中国好歌曲327，盖世英雄772，轻音乐11，经典影视原声782，发烧女声692，儿童故事227，广场舞128，咖啡厅27，一个人54，工作加油曲336" \
                     "，睡前301，学习158，散步344，清吧46，在路上342，驾驶37，打游戏897，聚会暖场293，婚礼47，午休343，安静32，起床150，轻松223，伤感42，寂寞30，甜蜜31，兴奋296，思念43" \
                     "，90后25，80后24，70后23，00后237，草原风232，流行299，民歌216，钢琴60，萨克斯678，中国风精选83，乡村音乐269，R&amp;B13，摇滚9，尤克里里724，爵士10，吉他76" \
                     "，古风好歌118，蒸汽波995，民谣16，说唱14，励志62，百听不厌英文歌706，怀旧粤语94，粤语20，欧美19，怀旧华语96，闽南语49，韩语22，国语18，日语21，法语40，泰语193" \
                     "，印度语1028，俄语1038，德语1040，意大利语1030，客家语1036，西班牙语1032，车载舞曲427，重低音434，EDM热歌898，串烧舞曲433，电音78，电子纯音950，0-1岁儿歌372" \
                     "，1-3岁儿歌377，3-6岁儿歌378，7-12岁儿歌379，英文儿歌963，胎教38，慢摇舞曲430，健身房744，跑步392，动感单车396，热身391，HIIT393，力量训练394，瑜伽367" \
                     "，出神舞曲844，华纳唱片1350，JYP1354，古典音乐15，SACRA MUSIC1356，日本ACG8，Prog House846，Liquid " \
                     "State1358，布鲁斯675，摩登天空1360，国风经典1382，国风新歌1384，伤感国风1390，教育科普1284，轻松唤醒532，抖音热门歌1048，321热歌现场版1058，八音盒804" \
                     "，中文舞曲552，英文舞曲553，新民歌572，二次元精选318，动画儿歌1088，国学启蒙1090，睡眠故事1092，劲舞团的回忆1630，日系轻音1632，冥想1126，150bpm616，自然1128" \
                     "，160bpm617，170bpm618，最热影视歌曲1130，180bpm619，热门动漫歌曲1132，白噪音1142，中国新乡村音乐1659，雨天654，热血国风1424，古筝677，小提琴679" \
                     "，超嗨舞曲426，House舞曲428，外文舞曲432，国语热歌457，欧美热歌458，笛子981，二胡982，葫芦丝983，冥想梵音494，服装店502"
        self.init_window_name.title("酷狗音乐下载工具_v1.0")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')  #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('800x650+50+50')
        # self.init_window_name.iconbitmap("favicon.ico")  # 设置图标
        self.init_window_name.resizable(width=False, height=False)  # 固定窗口大小
        # 标签
        self.init_data_label = Label(self.init_window_name, text="分类举例：")
        self.init_data_label.grid(row=0, column=0)
        # self.result_data_label = Label(self.init_window_name, text="输出结果")
        # self.result_data_label.grid(row=0, column=12)
        # 输入框
        self.path = StringVar()
        Label(self.init_window_name, text="存储路径:").grid(row=11, column=0)
        self.paths = Entry(self.init_window_name, textvariable=self.path)
        self.paths.grid(row=11, column=1)
        self.paths.insert(0, "E:/music")  # 设置默认值
        Button(self.init_window_name, text="路径选择", command=self.select_path).grid(row=11, column=2)

        self.mp3_id = Label(self.init_window_name, text="分类ID：").grid(row=12, column=0)
        self.mp3_id_input = Entry(self.init_window_name)
        self.mp3_id_input.focus()  # 设置焦点
        self.mp3_id_input.insert(0, "73")  # 设置默认值
        self.mp3_id_input1 = self.mp3_id_input.grid(row=12, column=1)

        self.mp3_name = Label(self.init_window_name, text="分类名称：").grid(row=13, column=0)
        self.mp3_name_input = Entry(self.init_window_name)
        self.mp3_name_input.insert(0, "KTV必点曲")  # 设置默认值
        self.mp3_name_input1 = self.mp3_name_input.grid(row=13, column=1)

        self.mp3_number = Label(self.init_window_name, text="下载数量：").grid(row=14, column=0)
        self.mp3_number_input = Entry(self.init_window_name)
        self.mp3_number_input.insert(0, 500)  # 设置默认值
        self.mp3_number_input1 = self.mp3_number_input.grid(row=14, column=1)

        button = Button(self.init_window_name, command=self.thread, text="开始下载", bg="lightblue", width=15, height=2)
        button.grid(row=14, column=10)
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=100, height=35)  # 分类信息展示
        self.init_data_Text.grid(row=1, column=1, rowspan=10, columnspan=10)
        self.init_data_Text.insert(END, self.radio)

    def thread(self):
        """创建线程（打开日志窗口,以免程序假死）"""
        T = threading.Thread(target=self.log_window)
        T.start()

    def log_window(self):
        """下载的歌曲信息展示窗口"""
        f = Toplevel(self.init_window_name, width=220, height=160)
        self.result_data_label = Label(f, text="输出结果：")
        self.result_data_label.grid(row=0, column=0)

        # photo = self.init_window_name.PhotoImage(file="aaa.gif")
        self.image_data_label = Label(f)
        # 信息展示框
        self.result_data_Text = scrolledtext.ScrolledText(f, width=70, height=49, bg="black", fg="OrangeRed")  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.image_data_label.grid(row=0, column=1)

        self.run()

    def select_path(self):
        """选择文件路径"""
        path_ = askdirectory()
        self.path.set(path_)

    def get_song_list(self, radio_id, offset=0, ):
        """
        获取分类音乐列表
        :param offset:
        :param radio_id: 分类
        :return: 音乐id
        """
        url = 'https://gateway.kugou.com/openapicdn/broadcast/v2/get_songlist'
        headers = {
            'User-Agent	': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'Cache-Control': 'no-cache'
        }
        data = {
            'radio_id': radio_id,
            'offset': offset,
            'pagesize': 20
        }
        response = requests.get(url, params=data, headers=headers)
        # print(response.json())
        data = response.json()
        songlist = data['data']['songlist']
        album_audio_id = []
        for i in songlist:
            album_audio_id.append(i['album_audio_id'])  # 遍历获取音乐id

        return album_audio_id

    def get_mp3_url(self, album_audio_id=347230505):
        """
        根据音乐id获取下载链接
        :param album_audio_id:
        :return: 下载链接
        """
        url = 'https://wwwapi.kugou.com/yy/index.php'
        headers = {
            'User-Agent	': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': '*/*',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'Cookie': 'Cookie=kg_mid=b4f03dbb6f8507a526daaf6841969508; kg_dfid=2mSzTC0VnZJK0GdxrD13UEWH; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1641362479; kg_mid_temp=b4f03dbb6f8507a526daaf6841969508; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1641365037'
        }
        data = {
            'r': 'play/getdata',
            'callback': 'jQuery191014049230921227585_1641362507387',
            'hash': '5B0A6869EBADC89B2914A51F44958D93',
            'appid': 1014,
            'mid': 'b4f03dbb6f8507a526daaf6841969508',
            'platid': 4,
            'album_id': album_audio_id,
            'album_audio_id': album_audio_id,
            '_': '1641362507390'
        }
        response = requests.get(url, params=data, headers=headers)
        # print(response.text)
        try:
            aa = re.findall('\((.*)\)', response.text)  # 提取JSON
            bb = json.loads(aa[0])
            # print(json.dumps(bb))
            play_backup_url = (bb['data']['play_backup_url'])  # 提取下载链接
            audio_name = (bb['data']['audio_name'])  # 提取音乐名称

            return play_backup_url, audio_name

        except BaseException:
            pass

    def save_mp3(self, paths, mp3_url, audio_name):
        """
        保存音乐文件
        :param paths: 文件存储路径
        :param mp3_url: 下载地址
        :param audio_name: 音乐名称
        :return:
        """
        url = mp3_url
        r = requests.get(url, stream=True)
        audio_names = re.sub('["*/?|!？！]', '', audio_name)  # 去除歌名中的部分符号
        with open(u"%s%s.mp3" % (paths, audio_names), 'wb') as f:
            f.write(r.content)  # 保存文件
            names = audio_names + "\n"
            self.write_log_to_Text(names)  # 打印歌曲名称

    def run(self):
        """音乐下载保存"""
        radio_id = self.mp3_id_input.get()  # 获取输入的id
        fm_name = self.mp3_name_input.get()  # 获取输入的分类名称
        past_new = self.paths.get()
        # print(radio_id, fm_name)
        paths = past_new + u"/%s/" % fm_name
        src_path = "音乐存储路径：%s\n" % paths
        self.write_log_to_Text(src_path)  # 打印保存路径
        number = self.mp3_number_input.get()
        numbers = int(number)
        if not os.path.exists(paths):
            os.makedirs(paths)  # 如果文件夹不存在则创建
        try:
            for offset in range(0, numbers+1, 20):  # 翻页
                # print("=============分类：%s  已下载 %d 首==========================" % (fm_name, offset))
                src = "========分类：%s  已下载 %d 首===========" % (fm_name, offset) + "\n"
                self.write_log_to_Text(src)  # 打印
                aa = self.get_song_list(radio_id=radio_id, offset=offset)  # 获取音乐id
                # print(aa)
                for i in aa:  # 遍历下载当页歌曲
                    bb = self.get_mp3_url(album_audio_id=i)  # 获取下载地址
                    # print(bb)
                    self.save_mp3(paths=paths, mp3_url=bb[0], audio_name=bb[1])  # 下载音乐
            self.write_log_to_Text(logmsg="                .-\"\"\" -.")
            self.write_log_to_Text(logmsg="               / .===. \\")
            self.write_log_to_Text(logmsg="               \/ 6 6 \/")
            self.write_log_to_Text(logmsg="               ( \___/ )")
            self.write_log_to_Text(logmsg="  _________ooo__\_____/_____________")
            self.write_log_to_Text(logmsg=" /                                  \\")
            self.write_log_to_Text(logmsg=" |     下 载 完 啦 ! ! !            |")
            self.write_log_to_Text(logmsg=" \_______________________ooo________/ ")
            self.write_log_to_Text(logmsg="                |  |  |")
            self.write_log_to_Text(logmsg="                |_ | _|")
            self.write_log_to_Text(logmsg="                |  |  |")
            self.write_log_to_Text(logmsg="                |__|__|")
            self.write_log_to_Text(logmsg="                /-'Y'-\\")
            self.write_log_to_Text(logmsg="               (__/ \__)")

        except BaseException:
            pass

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 20:
            self.result_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.result_data_Text.delete(1.0, 2.0)
            self.result_data_Text.insert(END, logmsg_in)


if __name__ == '__main__':
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)  # 设置根窗口默认属性
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
