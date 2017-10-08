from goog import ML
from bingme import imageURL
from bingme import *




guiDict = {}
count = 0
MAX_CYCLE = 5
def ml_main():
    global count
    global guiDict
    query1 = 'landscape'
    query2 = 'city'
    while (count < MAX_CYCLE):
        reply1,q1,c1=bingMe(query1,count)
        reply2,q2,c2=bingMe(query2,count)
        opt1 = imageURL(reply1)
        opt2 = imageURL(reply2)
        dler(opt1,q1,c1)
        dler(opt2,q2,c2)
        ans1 = imageUpload(q1,c1)
        ans2 = imageUpload(q2,c2)

        ##give shivam and yara the urls
        left = paratu(ans1)
        ml_left = ML(ans1)
        right = paratu(ans2)
        ml_right = ML(ans2)
        ### end names
        guiDict = {'first' : (left,ml_left), 'second': (right,ml_right)}
        #print(guiDict,'\n')
        if get_answer() == 0:
            query2 = ml_left[0]
            print(query2,'\n')
        else:
            query1 = ml_right[0]
            print(query1,'\n')
        count+=1 



    print('end of loop, we must now give them a place')


    """
    reply,q,c=bingMe('landscape',0)
    opt1 = imageURL(reply)
    dler(opt1,q,c)
    ans = imageUpload(q,c)
    print(ML(ans))
    """
ml_main()