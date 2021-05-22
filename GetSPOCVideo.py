from utils import urlsplit, get, post, get_cookie, save, loads
from asyncio import get_event_loop, Semaphore, wait
from os.path import dirname, exists
from os import startfile, mkdir
from config import Urls
from time import sleep


def is_mkdir(path):
    if not exists(path):
        mkdir(path)
    return path


async def login_in():
    try:
        return await get_cookie(Urls.login_url, {
            **Urls.login,
            "userName": input("输入账户："),
            "password": input("输入密码：")
        })
    except AssertionError as err:
        print(err)


class GetSPOCEVideo:
    max_load = 2  # 并行数量
    out_time = 5

    def __init__(self, url: str):
        self.url = url
        self.is_url = False
        self.headers = Urls.headers
        self.params = urlsplit(url)
        self.loop = get_event_loop()
        self.save_path = dirname(__file__)
        self.semaphore = Semaphore(self.max_load)
        self.loop.run_until_complete(self.run())

    async def get_chapter(self):
        """
        获取 queryChapterBytermId 中的数据
        """
        data = loads(
            await get(Urls.queryChapterBytermId,
                      headers=self.headers,
                      params=self.params)
        )["data"]["chapterList"]
        await wait([self.loop.create_task(
            self.get_subsection(i)) for i in data], timeout=None)

    async def get_subsection(self, data: dict):
        print("下载路径:", self.save_path)
        path = is_mkdir(data["chapterName"]) if self.is_url else None
        params = {
            "chapterId": data["id"],
            **self.params
        }
        data = loads(await get(
            Urls.querySubsectionListByChapterId,
            headers=self.headers,
            params=params)
            )["data"]["subsectionList"]

        await wait([self.loop.create_task(
            self.get_video({**params, "subsectionId": i["id"]}, path)
        ) for i in data], timeout=None)

    async def get_video(self, data: dict, path: str = None):
        data = loads(await post(Urls.queryStudentTrianList, headers=self.headers, data={
            "subsectionId": data["subsectionId"],
            "chapterId": data["chapterId"]
        }))["data"]

        if self.is_url:
            print(data["videoData"]["videoList"][0]["value"])
        else:
            path = is_mkdir(path or data["subsectionName"])
            data = data["videoData"]
            file_name = data["name"]
            async with self.semaphore:
                print("开始下载:", file_name)
                await save(await get(data["videoList"][0]["value"]), f"{path}/{file_name}")
                print("下载完成:", file_name, "\n所在目录:", path)

    async def login_select(self):
        cookie = None
        select = input("请选择大连医科大学登录方式\n1.手动登录\n2.输入Cookie\n请输入(1 or 2)：")
        if select == "1" or select == 1:
            cookie = await login_in()
        elif select == "2" or select == 2:
            cookie = input("请输入Cookie（如对于Cookie参数未知请退出重新选择）：")
        else:
            print("输入有误！没有%s选项" % select)

        if cookie:
            print("您的Cookie值为（可用于下次登录）：%s" % cookie)
            self.headers["Cookie"] = cookie
            return True
        return False

    def is_video_url(self):
        return all([i in self.params for i in ["subsectionId", "chapterId"]])

    def is_main_url(self):
        if Urls.main_url in self.url:
            return True
        print("链接输入有误！！")

    def load_type(self):
        __type = input("选择爬取类型:\n1.只爬取链接\n2.爬取视频（程序为为您整理爬取的视频并放置相应文件夹）\n请输入(1 or 2)：")
        self.is_url = __type == "1" or __type == 1

    async def run(self):
        if self.is_main_url():
            self.load_type()
            if await self.login_select():
                if self.is_video_url():
                    await self.get_video(self.params)
                else:
                    await self.get_chapter()

    def __del__(self):
        if self.is_url:
            input("按下回车(Enter)退出")
        else:
            print("%ss后自动退出" % self.out_time)
            startfile(self.save_path)
            sleep(self.out_time)


if __name__ == '__main__':
    print("本程序爬取默认爬取最高画质视频，所以爬取速度可能会稍慢，还请耐心等待，如果觉得过慢或者出错可以选择生成视频链接通过其他软件下载！")
    GetSPOCEVideo(input("输入目录或视频链接>> "))