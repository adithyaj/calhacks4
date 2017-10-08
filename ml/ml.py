from goog import ML
from bingme import imageURL
from bingme import *


def ml_main():
    count = 0
    query1 = 'landscape'
    query2 = 'city'
    while (count < 10):
        reply1,q1,c1=bingMe(query1,count)
        reply2,q2,c2=bingMe(query2,count)
        opt1 = imageURL(reply1)
        opt2 = imageURL(reply2)
        dler(opt1,q1,c1)
        dler(opt2,q2,c2)
        ans1 = imageUpload(q1,c1)
        ans2 = imageUpload(q2,c2)

        ##give shivam and yara the urls
        #left = paratu(ans1)
        #right = paratu(ans2)
        ### end names
        #gui_list=[left,right]

        if get_answer() == 0:
            query2 = ML(ans1)
            print(query2)
        else:
            query1 = ML(ans2)
            print(query1)
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