# -*- coding: UTF-8 -*-
# This video extraction code based on youtube-dl: https://github.com/ytdl-org/youtube-dl
# From Taapat plugin https://github.com/Taapat/enigma2-plugin-youtube

from __future__ import print_function

from re import search
from re import match
from re import sub
from json import loads
from json import dumps

from Components.config import config

from .compat import compat_urlopen
from .compat import compat_str
from .compat import compat_URLError
from .compat import compat_Request


PRIORITY_VIDEO_FORMAT = ()


def create_priority_formats():
	global PRIORITY_VIDEO_FORMAT
	itag = config.plugins.tmbd_yttrailer.best_resolution.value
	video_formats = (
		('17', '91', '13', '151', '160'),  # 176x144
		('5', '36', '92', '132', '133'),  # 400x240
		('18', '93', '34', '6', '134'),  # 640x360
		('35', '59', '78', '94', '135', '212'),  # 854x480
		('22', '95', '300', '136', '298'),  # 1280x720
		('37', '96', '301', '137', '299', '248', '303', '271'),  # 1920x1080
		('38', '266', '264', '138', '313', '315', '272', '308')  # 4096x3072
	)
	for video_format in video_formats:
		PRIORITY_VIDEO_FORMAT = video_format + PRIORITY_VIDEO_FORMAT
		if video_format[0] == itag:
			break


create_priority_formats()


DASHMP4_FORMAT = (
	'133', '134', '135', '136', '137', '138',
	'160', '212', '264', '266', '298', '299',
	'248', '303', '271', '313', '315', '272', '308'
)

IGNORE_VIDEO_FORMAT = (
	'43', '44', '45', '46',  # webm
	'82', '83', '84', '85',  # 3D
	'100', '101', '102',  # 3D
	'167', '168', '169',  # webm
	'170', '171', '172',  # webm
	'218', '219',  # webm
	'242', '243', '244', '245', '246', '247',  # webm
	'249', '250', '251',  # webm
	'302'  # webm
)


def try_get(src, get, expected_type=None):
	try:
		v = get(src)
	except (AttributeError, KeyError, TypeError, IndexError):
		pass
	else:
		if expected_type is None or isinstance(v, expected_type):
			return v


def clean_html(html):
	"""Clean an HTML snippet into a readable string"""

	html = sub(r'\s+', ' ', html)
	html = sub(r'(?u)\s?<\s?br\s?/?\s?>\s?', '\n', html)
	html = sub(r'(?u)<\s?/\s?p\s?>\s?<\s?p[^>]*>', '\n', html)
	# Strip html tags
	html = sub('<[^>]*>', '', html)
	return html.strip()


class YouTubeVideoUrl():

	@staticmethod
	def _guess_encoding_from_content(content_type, webpage_bytes):
		m = match(r'[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+\s*;\s*charset=(.+)', content_type)
		if m:
			encoding = m.group(1)
		else:
			m = search(br'<meta[^>]+charset=[\'"]?([^\'")]+)[ /\'">]', webpage_bytes[:1024])
			if m:
				encoding = m.group(1).decode('ascii')
			elif webpage_bytes.startswith(b'\xff\xfe'):
				encoding = 'utf-16'
			else:
				encoding = 'utf-8'

		return encoding

	def _download_webpage(self, url, data=None, headers={}):
		""" Return the data of the page as a string """

		if data:
			data = dumps(data).encode('utf8')
		if data or headers:
			url = compat_Request(url, data=data, headers=headers)
			url.get_method = lambda: 'POST'

		try:
			urlh = compat_urlopen(url, timeout=5)
		except compat_URLError as e:
			raise RuntimeError(e.reason)

		content_type = urlh.headers.get('Content-Type', '')
		webpage_bytes = urlh.read()
		encoding = self._guess_encoding_from_content(content_type, webpage_bytes)

		try:
			content = webpage_bytes.decode(encoding, 'replace')
		except Exception:
			content = webpage_bytes.decode('utf-8', 'replace')

		return content

	def _extract_from_m3u8(self, manifest_url):
		url_map = {}

		def _get_urls(_manifest):
			lines = _manifest.split('\n')
			urls = [x for x in lines if x and not x.startswith('#')]
			return urls

		manifest = self._download_webpage(manifest_url)
		formats_urls = _get_urls(manifest)
		for format_url in formats_urls:
			itag = search(r'itag/(\d+?)/', format_url)
			itag = itag.group(1) if itag else ''
			url_map[itag] = format_url
		return url_map

	def _not_in_fmt(self, fmt, itag):
		return not (
			fmt.get('targetDurationSec') or
			fmt.get('drmFamilies') or
			fmt.get('type') == 'FORMAT_STREAM_TYPE_OTF' or
			itag in DASHMP4_FORMAT
		)

	def _extract_fmt_video_format(self, streaming_formats):
		""" Find the best format from our format priority map """
		print('[YouTubeVideoUrl] Try fmt url')
		for our_format in PRIORITY_VIDEO_FORMAT:
			for fmt in streaming_formats:
				itag = str(fmt.get('itag', ''))
				if itag == our_format and self._not_in_fmt(fmt, itag):
					url = fmt.get('url')
					if url:
						print('[YouTubeVideoUrl] Found fmt url')
						return url
		return ''

	def _extract_player_response(self, video_id):
		url = 'https://www.youtube.com/youtubei/v1/player?key=AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w&bpctr=9999999999&has_verified=1'
		ANDROID = '18.48.37'
		USER_AGENT = 'com.google.android.youtube/%s(Linux; U; Android 13; en_US; sdk_gphone64_x86_64 Build/UPB4.230623.005) gzip' % ANDROID
		data = {
			'videoId': video_id,
			'params': 'CgIIAQ==',
			'playbackContext': {
				'contentPlaybackContext': {
					'html5Preference': 'HTML5_PREF_WANTS'
				}
			},
			'context': {
				'client': {
					'hl': 'en',
					'clientVersion': ANDROID,
					'androidSdkVersion': 33,
					'clientName': 'ANDROID',
					'osName': 'Android',
					'osVersion': '13',
					'userAgent': USER_AGENT
				}
			}
		}
		headers = {
			'content-type': 'application/json',
			'Origin': 'https://www.youtube.com',
			'X-YouTube-Client-Name': 3,
			'X-YouTube-Client-Version': ANDROID,
			'User-Agent': USER_AGENT
		}
		try:
			return loads(self._download_webpage(url, data, headers))
		except ValueError:
			print('[YouTubeVideoUrl] Failed to parse JSON')

	def _real_extract(self, video_id):
		url = ''

		player_response = self._extract_player_response(video_id)
		if not player_response:
			raise RuntimeError('Player response not found!')

		is_live = try_get(player_response, lambda x: x['videoDetails']['isLive'])
		playability_status = player_response.get('playabilityStatus', {})

		trailer_video_id = try_get(
			playability_status,
			lambda x: x['errorScreen']['playerLegacyDesktopYpcTrailerRenderer']['trailerVideoId'],
			compat_str
		)
		if trailer_video_id:
			print('[YouTubeVideoUrl] Trailer video')
			return str(trailer_video_id)

		streaming_data = player_response.get('streamingData', {})
		streaming_formats = streaming_data.get('formats', [])

		# If priority format changed in config, recreate priority list
		if PRIORITY_VIDEO_FORMAT[0] != config.plugins.tmbd_yttrailer.best_resolution.value:
			create_priority_formats()

		if not is_live and streaming_formats:
			streaming_formats.extend(streaming_data.get('adaptiveFormats', []))
			url = self._extract_fmt_video_format(streaming_formats)
			if not url:
				for fmt in streaming_formats:
					itag = str(fmt.get('itag', ''))
					if itag not in IGNORE_VIDEO_FORMAT and self._not_in_fmt(fmt, itag):
						url = fmt.get('url')
						if url:
							break
			if not url:
				url = streaming_formats[0].get('url', '')

		if not url:
			print('[YouTubeVideoUrl] Try manifest url')
			hls_manifest_url = streaming_data.get('hlsManifestUrl')
			if hls_manifest_url:
				url_map = self._extract_from_m3u8(hls_manifest_url)

				# Find the best format from our format priority map
				for our_format in PRIORITY_VIDEO_FORMAT:
					if our_format in url_map:
						url = url_map[our_format]
						break
				# If anything not found, used first in the list if it not in ignore map
				if not url:
					for url_map_key in list(url_map.keys()):
						if url_map_key not in IGNORE_VIDEO_FORMAT:
							url = url_map[url_map_key]
							break
				if not url and url_map:
					url = list(url_map.values())[0]

		if not url:
			if streaming_data.get('licenseInfos'):
				raise RuntimeError('This video is DRM protected!')
			pemr = try_get(
				playability_status,
				lambda x: x['errorScreen']['playerErrorMessageRenderer'],
				dict) or {}

			def get_text(x):
				if x and 'runs' in x:
					return x.get('simpleText', '').join([r['text'] for r in x['runs']])

			reason = get_text(pemr.get('reason')) or playability_status.get('reason')
			if reason:
				subreason = pemr.get('subreason')
				if subreason:
					subreason = clean_html(get_text(subreason))
					reason += '\n%s' % subreason
			raise RuntimeError(reason)

		return str(url)

	def extract(self, video_id):
		error_message = None
		for _ in range(3):
			try:
				return self._real_extract(video_id)
			except Exception as ex:
				if str(ex) == 'None':
					print('No supported formats found, trying again!')
				else:
					error_message = str(ex)
					break
		if not error_message:
			error_message = 'No supported formats found in video info!'
		raise RuntimeError(error_message)
