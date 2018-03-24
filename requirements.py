from pip import main

package_list = ['django','django-redis','channels','django-cors-headers','geopy','channels_redis','requests','websocket-client']
for i in package_list:''
	main(['install', i])
