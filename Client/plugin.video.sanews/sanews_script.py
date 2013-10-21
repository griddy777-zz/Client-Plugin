# import the XBMC libraries so we can use the controls and functions of XBMC
import xbmc, xbmcgui,xbmcplugin ,sys ,xbmcaddon, urllib,re,urllib2

#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10 # 'Esc'
ACTION_SELECT_ITEM = 7 # 'Enter'

#thisInstance = int(sys.argv[1])
_port = '8091'
_ip = '10.0.0.5'
_url = 'http://'+_ip+':'+_port+'/'

_rtsp_port = '8555'
_rtsp_url = 'rtsp://'+_ip+':'+_rtsp_port+'/'
_content_url = _url + 'stat.html'
_dir = "special://xbmc/addons/skin.confluence/backgrounds/SKINDEFAULT.jpg"
_icon = "special://xbmc/addons/plugin.video.sanews/icon.png"
_channelOne = "special://xbmc/addons/plugin.video.sanews/Firefly_S1.sdp"
_scrWidth = 1920
_scrHeight = 1080
_pluginId = 0#int (sys.argv[1])
__settings__   = xbmcaddon.Addon(id='plugin.video.sanews')

class SANewsMainWIndows(xbmcgui.Window):
	def __init__(self):
		self.button0 = xbmcgui.ControlButton(50, 50, 256, 256, "",focusTexture=_icon,noFocusTexture=_icon)
		self.addControl(self.button0)

	#Show popup message: self.message('Hello')
	def message(self, title, message):
		dialog = xbmcgui.Dialog()
		dialog.ok(title, message)
		
def __init__():
	scrapeMedia()
	
def getHTML(url):
        try:
            req = urllib2.Request(url)
			#req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link = response.read()
            response.close()
        except urllib2.HTTPError, e:
			mydisplay = SANewsMainWIndows()
			mydisplay.message('Error', "HTTP Error: " + e.code)
        except urllib2.URLError, e:
			mydisplay = SANewsMainWIndows()
			mydisplay.message('Error', "The server is currently offline. Please try again later.")
        else:
            return link
	
							
def scrapeMedia():
	handle = int(sys.argv[1])
	link = getHTML(_content_url)
	results = re.compile('<a href="(.+?)">').findall(link)
	#http://docs.python.org/3.2/library/re.html#match-objects
	results.pop() #last item
	results.pop() #last item
	for link in results:
		#Check File extension
		link = link[1:] #Skip first character '/'
		ext = re.split('\.', link)
		filename = ext[0]
		extention = ext[1]
		
		listitem = xbmcgui.ListItem(filename, iconImage="DefaultFolder.png")
		#listitem.setInfo(type="Video", infoLabels={ "Title": title, "Plot" : plot, "Duration" : time })
		listitem.setInfo('video', {'Title': filename, 'Genre': 'The Genre', 'Plot' : 'This is the plot!', 'Duration' : '180'})
		listitem.setProperty("IsPlayable", "true")
		
		if extention == 'rtsp':
			rtsp_file_path = _rtsp_url + link
			listitem.setPath(rtsp_file_path)
			xbmcplugin.addDirectoryItem(handle=handle, url=(rtsp_file_path), listitem=listitem)
		else:
			ogg_file_path = _url + link
			listitem.setPath(ogg_file_path)
			xbmcplugin.addDirectoryItem(handle=handle, url=(ogg_file_path), listitem=listitem)
			
	listitem = xbmcgui.ListItem('Electronic Programming Guide', iconImage=_icon)	
#	listitem.setInfo('video', {'Title': link[1:], 'Genre': 'The Genre', 'Plot' : 'This is the plot!', 'Duration' : '180'})
	listitem.setProperty("IsPlayable", "false")
#	listitem.setPath('sdp://F_low.sdp')
	xbmcplugin.addDirectoryItem(handle=handle, url=(''), listitem=listitem)
	    
    			
			
#def onAction(, action):
	#ESC is pressed
	#if action == ACTION_PREVIOUS_MENU:
	#	close()
		
#def onControl(control):
#	if control == button0:
#		listitem_URLVid = xbmcgui.ListItem('SABC X')
#		listitem_URLVid.setInfo('video', {'Title': 'SABC', 'Genre': 'News'})
#		xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ).play("http://10.0.0.101:8080", listitem_URLVid, False)

#Show popup message: message('Hello')
def message(title, message):
	dialog = xbmcgui.Dialog()
	dialog.ok(title, message)

__init__()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
