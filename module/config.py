# -*- coding: utf-8 -*-
import sys
import os.path
app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, "3party/"))
sys.path.insert(0, os.path.join(app_root, "module/"))
sys.path.insert(0, os.path.join(app_root, "web/"))
#   指定的模板路径
JINJA2TPL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__)
        , "templates/")
    )

#import hashlib

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 全局值
class Borg():
    '''base http://blog.youxu.info/2010/04/29/borg
        - 单例式配置收集类
    '''
    __collective_mind = {}
    def __init__(self):
        self.__dict__ = self.__collective_mind
    
    #管理员邮箱列表
    ADMIN_EMAIL_LIST = ['zoomquiet+gdg@gmail.com']

    import sae.kvdb
    KV = sae.kvdb.KVClient()

    #KVDB 对象模板
    KEY4_incr = 'gincr'
    TOT = KV.get(KEY4_incr)    # 全局自增序号
    if None == TOT:
        KV.add(KEY4_incr, 0)
    else:
        print "TOT", KV.get(KEY4_incr)

    objUSR={"his_id":""   # 更新戮
        , "del":0
        , "fsm":""      # 有限状态机 当前状态
        , "acl":1       # ban:0 usr:1 staff:10 api:42 admin:100
        , "desc":""     # 解释
        , "pp":''       # Passport 
        , "nm":""       # NickName "Zoom.Quiet"
        , 'em':''       #'zhouqi@ijinshan.com',
        , "lasttm": ''  #"2013-07-05 19:01:33",
        }
        



    # 大妈们的联系方式
    K4DM = {"his_id":""   # 更新戮
        , "del":0
        , "desc":""     # 解释
        , "pp":''       # Passport "kswl662773786"
        , "nm":""       # NickName "Zoom.Quiet"
        , 'em':''       #'zhouqi@ijinshan.com',
        }



    ESSAY_TAG = {'ot':"其它"
        , 'gb':"G术图书 (推荐好书,书无中外)"
        , 'dd':"D码点评 (麻辣评点,善意满盈)"
        , 'gt':"G说公论 (时评杂文,新旧不拘)"
        , 'hd':"海选文章 (得要相信,大妈法眼)"
        }
        
    # 文章索引
    K4DM = {"his_id":""   # 更新戮
        , "del":0
        , "tag":"ot"
        , 'tiele':''
        , "desc":""     # 解释
        , "picurl":''
        , "url":""
        }
        



    #   历史操作 键-名字典
    K4H = {'C':"Create"
        ,'D':"Delete"
        ,'U':"Update"
        }
    #'uuid':""     # 历史版本扩展ID
    objHis = {'hisobj':""
        ,'actype':"..."     # 操作类型C|D|U~ Create|Delet|Update = 创建|删除|更新
        ,'dump':''        # 数据集
        }




    TPL_TEXT=''' <xml>
     <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
     <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
     <CreateTime>%(tStamp)s</CreateTime>
     <MsgType><![CDATA[text]]></MsgType>
     <Content><![CDATA[%(content)s]]></Content>
     </xml>'''

    TPL_URIS='''<xml>
     <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
     <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
     <CreateTime>%(tStamp)s</CreateTime>
     <MsgType><![CDATA[news]]></MsgType>
     <ArticleCount>%(item_count)d</ArticleCount>
     <Articles>
     %(items)s
     </Articles>
     </xml> 
    '''

    TPL_ITEM='''<item>
     <Title><![CDATA[%(title)s]]></Title> 
     <Description><![CDATA[%(description)s]]></Description>
     <PicUrl><![CDATA[%(picurl)s]]></PicUrl>
     <Url><![CDATA[%(url)s]]></Url>
     </item>
    '''
    CMD_ALIAS={"help": ['h', 'H', 'Help', 'help', '?', u'？']
        , "version": ['v', 'V', 'ver', 'Version', 'version', 'Ver']
        , "info": ['i', 'I', 'Info', 'info', 'info.', 'information']
        , "search": ['s', 'S', 'see', 'See', 'search', 'Search', 'seek']
        , "event": ['e', 'E', 'event', 'Event', 'events', 'act']
        , "dm": ['dm', 'DM', 'Dm', 'dd']
        , "sayeahoo": ['syh', 'kvdb', 'stat', 'status']
        }

    DM_ALIAS = {"bonnie": ['Bonnie', 'lxc', 'LXC', u'刘星辰']
        , "zoomquiet": ['zq', 'zoomq', 'ZQ', u'ZQ大妈', u'大妈', u'周琦']
        , "spawnris": ['Spawnris', u'老高', u'高骏腾']
        , "langqixu": ['lqx', 'LQX', u'小郎', u'郎启旭']
        }

    TXT_WELCOME='''GDG珠海 公众号的应答范畴:
    - GDG活动报名、签到、直播
    - GDG大妈联系查询
    - GDG发表文章查阅
    功能正在完善中，欢迎反馈。
    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_HELP='''GDG珠海 公众号目前支持以下命令:
    h   ~ 打印本帮助
    V   ~ 查看系统版本
    s   ~ 查阅过往文章
    i   ~ 查看自己的资料
    e   ~ 查看将要举行的活动
    re  ~ 报名参加活动
    ir  ~ 查看自己已经报名的活动
    dm [组委的名字] 可了解TA更多
    '''

    TXT_NEW_USR='''还未注册 亲 的信息,请输入邮箱先;
    形如:
    em:foo.bar@gmail.com

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_PLS_EM='''请输入你的邮箱!形如:
    em:foo.bar@gmail.com

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_CRT_EM='''亲! 当前的邮箱是:
    %s

    更多细节,请惯性地输入 h 继续吧 :)
    '''


    '''
    2013/09/23 12:13:56] -  <xml>
         <ToUserName><![CDATA[oFNShjiOhclfJ-CtOO81p2sPrBfs]]></ToUserName>
         <FromUserName><![CDATA[gh_5e32c47b5b23]]></FromUserName>
         <CreateTime>13092312135634476</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[本公众号的自动回答范畴：
        - GDG活动报名、签到、直播
        - GDG大妈联系查询
        - GDG发表文章查阅
        功能正在完善中，欢迎反馈。
        更多请惯性地输入 h 继续吧 :)
        ]]></Content>
         </xml> yq34 
    '''

    VERSION = "weknow v13.09.18"
    
CFG = Borg()

