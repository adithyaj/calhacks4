from goog import ML
from bingme import imageURL
from bingme import *




guiDict = {}
count = 0
query1 = 'landscape'
query2 = 'city'
def ml_main(param=None):
    global count
    global guiDict
    global query2
    global query1

    if param == 0:
        query2 = ml_left[0]
        print(query2,'\n')
    elif param == 1:
        query1 = ml_right[0]
        print(query1,'\n')

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

    """
    reply,q,c=bingMe('landscape',0)
    opt1 = imageURL(reply)
    dler(opt1,q,c)
    ans = imageUpload(q,c)
    print(ML(ans))
    """