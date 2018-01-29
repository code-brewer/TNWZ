import json
import time
import webbrowser
import threading
import pymysql


def find_answer(j,quiz):
    connect = pymysql.connect(host='localhost', user='root', passwd='123123', db='tnwz', charset='utf8')
    cursor = connect.cursor()
    cursor.execute('SELECT answer FROM a WHERE quiz="%s"'%quiz)
    result = cursor.fetchall()
    if result:
        webbrowser.open('http://www.baidu.com/s?ie=UTF-8&wd='+quiz)                       #本地数据库中没找到问题则百度
        ans = {}
        while True:
            f = open('C:\\Users\\john\\Desktop\\choose.txt','r',encoding = 'utf-8')     #读取答完题之后，答案的数据
            try:
                ans = json.loads(f.read())
            
                if ans['data']['num'] == j['data']['num']:      #判断当前答案题号是否跟问题题号一致，因为答案比问题晚出来
                    print('num',ans['data']['num'])
                    break;
            except:
                pass
            time.sleep(0.3)
        answer = j['data']['options'][ans['data']['answer']-1]  #获取答案
        print(answer)
        cursor.execute('INSERT INTO a (quiz, answer) VALUES("%s", "%s")'%(quiz,answer))#将问题，答案存入数据库
    else:
        print(result)               #如果本地数据库中有该问题则直接输出答案
    cursor.close()
    connect.close()
def main():
    
    quiz_backup = ''
    print('find_answer')
    while True:
        try:
            f = open('C:\\Users\\john\\Desktop\\response_body.txt','r',encoding = 'utf-8')
            
            j = json.loads(f.read())        #把保存下来的数据转成字典
            if 'quiz' in j['data']:
                quiz = j['data']['quiz']
                if quiz == quiz_backup:     #如果相等说明下一题还没来
                    pass
                else:
                    print(quiz)
                    quiz_backup = quiz
                    t = threading.Thread(target=find_answer,args=(j,quiz))
                    t.start()
            else:
                pass
                
            f.close()
            time.sleep(0.2)
        except:
            pass

if __name__ == '__main__':
    main()

