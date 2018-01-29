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
        webbrowser.open('http://www.baidu.com/s?ie=UTF-8&wd='+quiz)
        ans = {}
        while True:
            f = open('C:\\Users\\john\\Desktop\\choose.txt','r',encoding = 'utf-8')
            try:
                ans = json.loads(f.read())
            
                if ans['data']['num'] == j['data']['num']:
                    print('num',ans['data']['num'])
                    break;
            except:
                pass
            time.sleep(0.3)
        answer = j['data']['options'][ans['data']['answer']-1]
        print(answer)
        cursor.execute('INSERT INTO a (quiz, answer) VALUES("%s", "%s")'%(quiz,answer))
    else:
        print(result)
    cursor.close()
    connect.close()
def main():
    
    quiz_backup = ''
    print('find_answer')
    while True:
        try:
            f = open('C:\\Users\\john\\Desktop\\response_body.txt','r',encoding = 'utf-8')
            
            j = json.loads(f.read())
            if 'quiz' in j['data']:
                quiz = j['data']['quiz']
                if quiz == quiz_backup:
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

