import os
import sys

#返回根目录绝对路径
def PATH():
    path=(os.path.split( os.path.realpath( sys.argv[0] ) )[0]+'/')
    return (path)