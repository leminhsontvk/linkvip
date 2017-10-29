# -*- coding: utf-8 -*-
#https://www.facebook.com/groups/vietkodi/

import re
import urlfetch
import os
from time import sleep
from addon import notify, alert, ADDON
import simplejson as json
import random
import xbmc
from config import VIETMEDIA_HOST

USER_VIP_CODE = ADDON.getSetting('user_vip_code')

def fetch_data(url, headers=None, data=None):
  	if headers is None:

  		headers = { 
    				'User-agent'	: 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0',
                	'Referer'		: 'http://www.google.com',
                	'X-User-VIP'    :  USER_VIP_CODE
            }
  	try:

  		if data:
  			response = urlfetch.post(url, headers=headers, data=data)
  		else:
			response = urlfetch.get(url, headers=headers)

		return response

	except Exception as e:
  		print e
  		pass


def get(url):
	if '//fptplay.net' in url:
		return get_fptplay(url)
	if 'www.fshare.vn' in url:
		return get_fshare(url)
	if 'hdonline.vn' in url:
		return get_hdonline(url)
	if '//vtvgo.vn' in url:
		return get_vtvgo(url)
	else:
		return url

def get_fptplay(url):
	headers = { 
				'Referer'			: 'https://fptplay.net',
    			'X-Requested-With'	: 'XMLHttpRequest'
            }
	#Kiá»ƒm tra live tivi 
	match = re.search(r'\/livetv\/(.*)$', url)
	if match:
		channel_id = match.group(1)
		data = {
	  		'id' 	   : channel_id,
	  		'type'     : 'newchannel',
	  		'quality'  : 3,
	  		'mobile'   : 'web'
	    }
		response = fetch_data('https://fptplay.net/show/getlinklivetv', headers, data)
		if response:
			json_data = json.loads(response.body)
			return json_data['stream']

	match = re.search(r'\-([\w]+)\.html', url)
	if not match:
		return

	movie_id = match.group(1)
	match = re.search(r'#tap-([\d]+)$', url)
	
	if match:
		episode_id = match.group(1)
	else:
		episode_id = 1

	data = {
  		'id' 	   : movie_id,
  		'type'     : 'newchannel',
  		'quality'  : 3,
  		'episode'  : episode_id,
  		'mobile'   : 'web',
    }

	response = fetch_data('https://fptplay.net/show/getlink', headers, data)
	
	if response:
		json_data = json.loads(response.body)
		return json_data['stream']
	pass

def get_vtvgo(url):
	response = fetch_data(url)
	if not response:
		return ''

	match = re.search(r'"file": \'(.*?)\'', response.body)
	if not match:
		return ''
	video_url = match.group(1)
	xbmc.log(video_url)
	return video_url

def get_hdonline(url):
	attempt = 1
	MAX_ATTEMPTS = 5
	
	xbmc.log(url)

	while attempt < MAX_ATTEMPTS:
		if attempt > 1: 
			sleep(2)
		url_play = ''
		notify (u'Láº¥y link láº§n thá»© #%s'.encode("utf-8") % attempt)
		attempt += 1
		response = fetch_data(url)
		if not response:
			return ''

		match = re.search(r'\-(\d+)\.?\d*?\.html$', url)
		if not match:
			return ''
		fid = match.group(1)

		match = re.search(r'\-tap-(\d+)-[\d.]+?\.html$', url)
		if not match:
			ep = 1
		else:
			ep = match.group(1)
		
		match = re.search(r'\|(\w{86}|\w{96})\|', response.body)
		if match:
			token = match.group(1)
			
			match = re.search(r'\|14(\d+)\|', response.body)
			token_key = '14' + match.group(1)
			
			token = token + '-' + token_key

			_x = random.random()
			url_play = ('http://hdonline.vn/frontend/episode/xmlplay?ep=%s&fid=%s&format=json&_x=%s&token=%s' % (ep, fid, _x, token))
			break
		else:
			match = re.search(r'"file":"(.*?)","', response.body)
			if match:
				url_play = 'http://hdonline.vn' + match.group(1).replace('\/','/') + '&format=json'
				url_play = url_play.replace('ep=1','ep=' + str(ep))
				break
	if len(url_play) == 0:
		notify (u'KhĂ´ng láº¥y Ä‘Æ°á»£c link.')
		return ''

	headers = { 
				'User-Agent' 	: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
				'Referer'		: url,
				'Accept'		: 'application/json, text/javascript, */*; q=0.01',
				'Cookie'		: response.cookiestring
			}
	response = fetch_data(url_play, headers)

	json_data = json.loads(response.body)
	video_url = json_data['file']
	if json_data.get('level') and len(json_data['level']) > 0:
		video_url = json_data['level'][len(json_data['level']) - 1]['file']

	subtitle_url = ''
	if json_data.get('subtitle') and len(json_data['subtitle']) > 0:
		for subtitle in json_data['subtitle']:
			subtitle_url = subtitle['file']
			if subtitle['code'] == 'vi':
				subtitle_url = subtitle['file']
				break
	
	xbmc.log(video_url)

	if len(subtitle_url) > 0:		
		subtitle_url = ('http://data.hdonline.vn/api/vsub.php?url=%s' % subtitle_url)
		return video_url + "[]" + subtitle_url
	else:
		return video_url

def get_hash(m):
	md5 = m or 9
	s = ''
	code = 'LinksVIP.Net2014eCrVtByNgMfSvDhFjGiHoJpKlLiEuRyTtYtUbInOj9u4y81r5o26q4a0v'
	for x in range(0, md5):
		s = s + code[random.randint(0,len(code)-1)] 
    
	return s
def get_linkvips(fshare_url,username, password):
	host_url = 'http://linksvip.net'
	login_url = 'http://linksvip.net/login/'
	logout_url = 'http://linksvip.net/login/logout.php'
	getlink_url = 'http://linksvip.net/GetLinkFs'
	
	response = fetch_data(host_url)
	if not response:
		return
	
	cookie = response.cookiestring

	headers = { 
				'User-Agent' 	: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
				'Cookie'		: cookie,
				'Referer'		: host_url,
				'Content-Type'	: 'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept'		: 'application/json, text/javascript, */*; q=0.01',
				'X-Requested-With'	: 'XMLHttpRequest'
            }
	
	data = {
			"u"				: username,
			"p"				: password,
			"auto_login"	: 'checked'
		}

	response = fetch_data(login_url, headers, data)

	video_url = ''
	if response.status == 200:
		json_data = json.loads(response.body)
		if int(json_data['status']) == 1:
			cookie = cookie + ';' + response.cookiestring
			headers['Cookie'] = cookie
			data = {
				"link"			: fshare_url,
				"pass"			: 'undefined',
				"hash"			: get_hash(32),
				"captcha"		: ''

			}
			headers['Accept-Encoding'] = 'gzip, deflate'
			headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
			
			response = fetch_data(getlink_url, headers, data)

			json_data = json.loads(response.body)

			link_vip = json_data['linkvip']
			
			response = fetch_data(link_vip, headers)

			match = re.search(r'id="linkvip"\stype="text"\svalue="(.*?)"', response.body)
			if not match:
				return ''
			video_url = match.group(1)

			#logout
			response = fetch_data(logout_url, headers)
			
	return video_url

def get_fshare(url):
	login_url = 'https://www.fshare.vn/login'
	logout_url = 'https://www.fshare.vn/logout'
	download_url = 'https://www.fshare.vn/download/get'

	username = ADDON.getSetting('fshare_username')
	password = ADDON.getSetting('fshare_password')

	direct_url = ''
	if len(username) == 0  or len(password) == 0:
		try:
			url_account = VIETMEDIA_HOST + '?action=fshare_account_linkvips'
			response = fetch_data(url_account)
			json_data = json.loads(response.body)
			username = json_data['username']
			password = json_data['password']

			if len(username) > 0  and len(password) > 0:
				direct_url = get_linkvips(url, username,password)
				if len(direct_url) > 0:
					notify(u'Láº¥y link fshare VIP thÃ nh cÃ´ng.'.encode("utf-8"))
					return direct_url
		except:
			pass

	if len(username) == 0  or len(password) == 0:
		alert(u'Báº¡n chÆ°a nháº­p tÃ i khoáº£n fshare, hoáº·c cáº§n pháº£i cÃ³ VIP code'.encode("utf-8"))
		return

	response = fetch_data(login_url)
	if not response:
		return

	csrf_pattern = '\svalue="(.+?)".*name="fs_csrf"'

	csrf=re.search(csrf_pattern, response.body)
	fs_csrf = csrf.group(1)

	headers = { 
				'User-Agent' 	: 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0',
				'Cookie'		: response.cookiestring
            }
	
	data = {
			"LoginForm[email]"		: username,
			"LoginForm[password]"	: password,
			"fs_csrf"				: fs_csrf
		}

	response = fetch_data(login_url, headers, data)
	headers['Cookie'] = response.cookiestring
	headers['Referer'] = url
	
	attempt = 1
	MAX_ATTEMPTS = 8
	file_id = os.path.basename(url)
	if response and response.status == 302:
		notify (u'ÄÄƒng nháº­p fshare thÃ nh cÃ´ng'.encode("utf-8"))
		while attempt < MAX_ATTEMPTS:
			if attempt > 1: sleep(2)
			notify (u'Láº¥y link láº§n thá»© #%s'.encode("utf-8") % attempt)
			attempt += 1

			response = fetch_data(url, headers, data)

			if response.status == 200:
				csrf=re.search(csrf_pattern, response.body)
				fs_csrf = csrf.group(1)
				data = {
						'fs_csrf'					: fs_csrf,
						'ajax'						: 'download-form',
						'DownloadForm[linkcode]'	: file_id
					}
				
				response=fetch_data(download_url, headers, data);
				
				json_data = json.loads(response.body)
				
				if json_data.get('url'):
					direct_url = json_data['url']
					break
				elif json_data.get('msg'):
					notify(json_data['msg'].encode("utf-8"))
			elif response.status == 302:
				direct_url = response.headers['location']
				break
			else:
				notify (u'Lá»—i khi láº¥y link, mÃ£ lá»—i #%s. Äang thá»­ láº¡i...'.encode("utf-8") % response.status) 

		response = fetch_data(logout_url, headers)
		if response.status == 302:
			notify (u'ÄÄƒng xuáº¥t fshare thÃ nh cÃ´ng'.encode("utf-8"))
	else:
		notify (u'ÄÄƒng nháº­p khÃ´ng thÃ nh cÃ´ng, kiá»ƒm tra láº¡i tÃ i khoáº£n'.encode("utf-8"))
	if len(direct_url) > 0:
		notify (u'ÄÃ£ láº¥y Ä‘Æ°á»£c link'.encode("utf-8"))
	else:
		notify (u'KhÃ´ng Ä‘Æ°á»£c link, báº¡n vui lÃ²ng kiá»ƒm tra láº¡i tÃ i khoáº£n'.encode("utf-8"))

	return direct_url
