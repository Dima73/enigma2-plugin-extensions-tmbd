from sys import version_info


# Disable certificate verification on python 2.7.9
if version_info >= (2, 7, 9):
	import ssl
	ssl._create_default_https_context = ssl._create_unverified_context


if version_info[0] == 2:
	# Python 2
	compat_str = unicode

	from urllib2 import urlopen as compat_urlopen
	from urllib2 import Request as compat_Request
	from urllib2 import URLError as compat_URLError
else:
	# Python 3
	compat_str = str

	from urllib.request import urlopen as compat_urlopen
	from urllib.request import Request as compat_Request
	from urllib.error import URLError as compat_URLError
