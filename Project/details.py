"""@package docstring
Documentation for this module.

This module has functions to find the semester and department from roll number.
"""
from time import gmtime, strftime

def semFinder(roll): 
	"""Function to parse the roll number and get semester
	"""
	a=str(roll)
	year=a[0:2]
	m=strftime("%m", gmtime())
	y=strftime("%y", gmtime())
	ans = ((float(m)-1)/12)+int(y)-int(year)
	return int(ans*2)

def depFinder(roll): 
	"""Function to parse the roll number and get department
	"""
	a=str(roll)
	dep=a[4:6]
	deps={"01":"CSE","02":"ECE","03":"ME","04":"CE","05":"bdes","06":"BT","07":"CL","08":"EEE","21":"EPh","22":"CST","23":"MC"}
	return deps[dep]
