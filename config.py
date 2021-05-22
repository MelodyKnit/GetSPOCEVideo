class Urls:
    main_url = "210.47.245.72"
    # 登录url
    login_url = "http://210.47.245.72/user/loginV2"
    # 查询章节id
    queryChapterBytermId = "http://210.47.245.72/courseResourceCtrl/queryChapterBytermId"
    # 通过查询的章节id获取字列表
    querySubsectionListByChapterId = "http://210.47.245.72/courseResourceCtrl/querySubsectionListByChapterId"
    # 获取视频数据
    queryStudentTrianList = "http://210.47.245.72/multilingual/queryStudentTrianList"
    # 请求头
    headers = {
        "Host": "210.47.245.72",
        "Origin": "http://210.47.245.72",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36 "
    }
    # 登录信息
    login = {
        "userName": "",
        "password": "",
        "backurl": "http://210.47.245.72/pages/search/course.jsp",
        "autoLogin": 0,
        "cdoe": "",
        "tokenType": ""
    }
