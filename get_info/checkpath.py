import time
import os


def checkpath(title, DIR):
    if DIR[-1] != '/':
        DIR += '/'

    suffix = time.strftime("_%y%m%d_%H%M%S", time.localtime())
    fditems = f'{title}_ditems'.replace(' ', '_') + suffix + '.txt'
    finfo = f'{title}_info'.replace(' ', '_') + suffix + '.csv'

    fditemspath = DIR + 'ditems/'
    finfopath = DIR + 'info/'
    if not os.path.exists(fditemspath):
        os.makedirs(fditemspath)
    if not os.path.exists(finfopath):
        os.makedirs(finfopath)

    fditemspath = fditemspath + fditems
    finfopath = finfopath + finfo
    if os.path.exists(fditemspath):
        print("{} has been removed.".format(fditemspath))
        os.remove(fditemspath)
    if os.path.exists(finfopath):
        print("{} has been removed.".format(finfopath))
        os.remove(finfopath)

    return fditemspath, finfopath
