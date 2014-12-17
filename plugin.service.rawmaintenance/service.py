import xbmc, xbmcgui, xbmcaddon
import os, sys, statvfs, time, datetime
from time import mktime
import feedparser
 
__addon__       = xbmcaddon.Addon(id='plugin.video.rawmaintenance')
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')

thumbnailPath = xbmc.translatePath('special://thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.service.rawmaintenance')
mediaPath = os.path.join(addonPath, 'media')
databasePath = xbmc.translatePath('special://database')


#######################################################################
#							RSS
#######################################################################
global rss
global lastCheck

def rssStartup():
    global rss
    global lastCheck 

    string = ''

    print "----####RSS STARTUP####----"
    rss = feedparser.parse('http://notanrss.info/rss.vex')
    if rss.bozo:
        return
    
    try:
        fo = open(os.path.join(addonPath, "lastAccess.bin"), "rb+")
    except:
        #if file doesn't exist create a new one
        fo = open(os.path.join(addonPath, "lastAccess.bin"), "wb+")
        fo.write(time.strftime('%m/%d/%Y %I:%M:%S %p', (1993, 1, 1, 1,1,1,1,1,1)))
    fo.seek(0)
    string = fo.readline()
    fo.seek(0)
    fo.write(time.strftime('%m/%d/%Y %I:%M:%S %p'))
    fo.close()
    
    print "LAST CHECKED DATE: "+ string
    lastCheck = time.strptime(string, '%m/%d/%Y %I:%M:%S %p')
    
    checkStories()

def checkStories():
    global rss
    global lastCheck
    
    for story in rss.entries:
        publish = time.strptime(story.published[:-6], '%a, %d %b %Y %H:%M:%S')
        publishd = datetime.datetime.fromtimestamp(mktime(publish))
        if abs((publishd - datetime.datetime.now()).days) < 14 and publish > lastCheck:
            rssShowStory(story)

def rssShowStory(story):
    global rss

    dialog = xbmcgui.Dialog()
    dialog.ok(story.title, story.description)

#######################################################################
#							MAIN
#######################################################################

if __name__ == '__main__':
    #check HDD freespace
    st = os.statvfs(xbmc.translatePath('special://home'))

    if((st.f_bfree/1024) < 500):
        text = "You have less than 500MB of free space"
        text1 = "Please use the Raw Maintenance tool"
        text2 = "immediately to prevent system issues"

        xbmcgui.Dialog().ok(__addonname__, text, text1, text2)

    #rss check
    rssStartup()

    while not xbmc.abortRequested:    
        xbmc.sleep(500)
