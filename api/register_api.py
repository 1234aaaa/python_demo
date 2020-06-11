
from requests import Response


class RegisterApi:
    '''
    封装请求方法
    '''
    def doGet(self, session, url):
        '''
        封装Get请求
        :rtype:Response
        :param session:
        :param url:
        :return:
        '''
        return session.get(url=url)

    def doFormPost(self, session, url, data, headers=None):
        '''
        封装支持表单数据的Post请求
        :rtype:Response
        :param session:
        :param url:
        :param data:
        :param headers:
        :return:
        '''
        return session.post(url=url, data=data, headers=headers)
