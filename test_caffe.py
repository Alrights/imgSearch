import urllib2
import json
if __name__=='__main__':
	url = 'http://192.168.116.131:8080'
	res = urllib2.urlopen(url).read()
	dict_res = json.loads(res)
	print dict_res
	bef_res = {}
	for key in dict_res.keys():
		bef_res[key] = float(dict_res[key])
	print bef_res
	final_res = sorted(bef_res.iteritems(),key=lambda d:d[1],reverse=True)
	print final_res
	for i in range(len(final_res)):
		print final_res[i][0]
		print final_res[i][1]