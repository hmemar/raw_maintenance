import urllib,urllib2,re
import xbmcgui,xbmcplugin
import feedparser
import os

thumbnailPath = xbmc.translatePath('special://thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'script.rawmaintenance')
mediaPath = os.path.join(addonPath, 'media')
databasePath = xbmc.translatePath('special://database')

#######################################################################
#							RSS
#######################################################################
global rss

def rssStartup():
    print "----####RSS STARTUP####----"
    global rss 

    rss = feedparser.parse('http://notanrss.info/rss.vex')
    if rss.bozo:
        dialog = xbmcgui.Dialog()
        dialog.ok("RSS", "There was a problem with the feed", "Check your internet connection and/or try again later")
        return -1

def rssMenu():
    print "----####RSS MENU CONFIG####----"
    global rss
    xbmc.executebuiltin("Container.SetViewMode(50)")
    x = 50
    for entry in rss.entries:
        print entry.title
        addItem(entry.title, 'url', x, os.path.join(mediaPath, "news.png"))
        x=x+1
        
def rssShowStory(mode):
    mode = mode - 50;
    print mode
    
    rss = feedparser.parse('http://www.feedforall.com/sample.xml')
    if rss.bozo:
        dialog = xbmcgui.Dialog()
        dialog.ok("RSS", "There was a problem with the feed", "Check your internet connection and/or try again later")
	
    dialog = xbmcgui.Dialog()
    dialog.ok(rss.entries[mode].title, rss.entries[mode].description)
        
#######################################################################
#						Build Main Menu
#######################################################################

def mainMenu():
	print os.path.join(mediaPath, "icon.png")
	xbmc.executebuiltin("Container.SetViewMode(500)")
	addItem('Clear Cache','url', 1,os.path.join(mediaPath, "clear.png"))
	addItem('Delete Thumbnails', 'url', 2,os.path.join(mediaPath, "delete.png"))
	addItem('Purge Packages', 'url', 3,os.path.join(mediaPath, "purge.png"))
	addDir('News', 'url', 4,os.path.join(mediaPath, "news.png"))

#######################################################################
#						Add to menus
#######################################################################

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok


def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	
def addItem(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

#######################################################################
#						Parses Choice
#######################################################################
      
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
					params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
							param[splitparams[0]]=splitparams[1]
							
	return param   

#######################################################################
#						Work Functions
#######################################################################

def clearCache():
	if os.path.exists(cachePath)==True:    
		for root, dirs, files in os.walk(cachePath):
			file_count = 0
			file_count += len(files)
			if file_count > 0:

				dialog = xbmcgui.Dialog()
				if dialog.yesno("Delete XBMC Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
				
					for f in files:
						try:
							if (f == "xbmc.log" or f == "xbmc.old.log"): continue
							os.unlink(os.path.join(root, f))
						except:
							pass
					for d in dirs:
						try:
							shutil.rmtree(os.path.join(root, d))
						except:
							pass
						
			else:
				pass
	if os.path.exists(tempPath)==True:    
		for root, dirs, files in os.walk(tempPath):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Delete XBMC Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
					for f in files:
						try:
							if (f == "xbmc.log" or f == "xbmc.old.log"): continue
							os.unlink(os.path.join(root, f))
						except:
							pass
					for d in dirs:
						try:
							shutil.rmtree(os.path.join(root, d))
						except:
							pass
						
			else:
				pass
	if xbmc.getCondVisibility('system.platform.ATV2'):
		atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
		
		for root, dirs, files in os.walk(atv2_cache_a):
			file_count = 0
			file_count += len(files)
		
			if file_count > 0:

				dialog = xbmcgui.Dialog()
				if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
				
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
						
			else:
				pass
		atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
		
		for root, dirs, files in os.walk(atv2_cache_b):
			file_count = 0
			file_count += len(files)
		
			if file_count > 0:

				dialog = xbmcgui.Dialog()
				if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
				
					for f in files:
						os.unlink(os.path.join(root, f))
					for d in dirs:
						shutil.rmtree(os.path.join(root, d))
						
			else:
				pass	
				
	dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
	pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
					"special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
					"special://profile/addon_data/plugin.video.itv/Images"]
										 
	for currentDialog, currentPath in dialogName, pathName:
		clear_cache_path = xbmc.translatePath(currentPath)
		if os.path.exists(wtf_cache_path)==True:    
			for root, dirs, files in os.walk(currentPath):
				file_count = 0
				file_count += len(files)
				if file_count > 0:

					dialog = xbmcgui.Dialog()
					if dialog.yesno("Raw Manager",str(file_count) + "%s cache files found"%(currentDialog), "Do you want to delete them?"):
						for f in files:
							os.unlink(os.path.join(root, f))
						for d in dirs:
							shutil.rmtree(os.path.join(root, d))
							
				else:
					pass
				

	dialog = xbmcgui.Dialog()
	dialog.ok("Raw Maintenance", "Done Clearing Cache files")
    
	
def deleteThumbnails():
	if os.path.exists(thumbnailPath)==True:  
			dialog = xbmcgui.Dialog()
			if dialog.yesno("Delete Thumbnails", "This option deletes all thumbnails", "Are you sure you want to do this?"):
				for root, dirs, files in os.walk(thumbnailPath):
					file_count = 0
					file_count += len(files)
					if file_count > 0:				
						for f in files:
							try:
								os.unlink(os.path.join(root, f))
							except:
								pass				
	else:
		pass
	
	text13 = os.path.join(databasePath,"Textures13.db")
	os.unlink(text13)
		
	if dialog.yesno("Restart XMBC", "Would you like to restart XBMC", "to rebuild thumbnail library?"):
		xbmc.executebuiltin("RestartApp")
		
def purgePackages():
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Package Cache Files", "This will delete all package files.", "Are you sure?"):  
		for root, dirs, files in os.walk(purgePath):
			file_count = 0
			file_count += len(files)
			if file_count > 0:            
				for f in files:
					os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
				dialog = xbmcgui.Dialog()
				dialog.ok("Raw Maintenance", "Deleting Packages all done")
			else:
				dialog = xbmcgui.Dialog()
				dialog.ok("Raw Maintenance", "No Packages to Purge")


#######################################################################
#						START MAIN
#######################################################################              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

if mode==None or url==None or len(url)<1:
        mainMenu()
       
elif mode==1:
		clearCache()
        
elif mode==2:
        deleteThumbnails()

elif mode==3:
		purgePackages()
        
elif mode==4:
        rssStartup()
        rssMenu()
        
elif mode >= 50:
        rssShowStory(mode)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
