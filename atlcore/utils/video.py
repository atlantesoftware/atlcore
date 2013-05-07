#coding=UTF-8
import commands

def takethumbnailfromvideo(sourcefile, thumbnailfile):
    try:
        ffmpegcommand = 'ffmpeg -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec mjpeg -f rawvideo -s 320x240 %s' % (sourcefile, thumbnailfile)
        commandresult = commands.getoutput(ffmpegcommand)
        return 1
    except:
        return 0
