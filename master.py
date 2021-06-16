import requests
from flask import Flask, request


def query():
	'''
	query the device parameters
	'''
	IP_list = []
	infos = []
	for ip in IP_list:
		info = requests.get('http://' + ip + ':5000/get_status')
		infos.append(info)

	return infos

def decision():
	'''
	generate the offloading decisions
	'''
	pass

def message():
	'''
	send the control message to the edge devices
	'''
	pass