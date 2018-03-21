from pip import main

package_list = ['django','channels','django-cors-headers','geopy','channels_redis','requests','websocket']
for i in package_list:
	main(['install', i])
