from blob import Blob
import time
from random import randint
from ast import literal_eval as make_tuple

#converts a blob to a formatted string
def blobToString(blob):
	blob_str = "%s:%.3f:%.3f:%.3f:%s:%d:%.3f:%.3f:%.3f:%.3f;" % (blob.name,
															blob.x,
															blob.y,
															blob.radius,
															blob.color,
															blob.game_id,
															blob.direction[0],
															blob.direction[1],
															blob.velocity,
															blob.timestamp )
	return blob_str

#converts a formatted blob string to a blob object.
def blobFromString(blob_str):
	blob_str  = blob_str[:-1]
	blob_attr = blob_str.split(":")
	blob_obj  = Blob(blob_attr[0],
					float(blob_attr[1]),
					float(blob_attr[2]), 
					float(blob_attr[3]),
					make_tuple(blob_attr[4]),
					int(blob_attr[5]),
					[float(blob_attr[6]),float(blob_attr[7])], 
					float(blob_attr[8]),
					float(blob_attr[9]))

	return blob_obj

#converts a list of blobs to a list of formatted strings.
def blobsToString(blob_list):
	#handles the case of no blobs to convert.
	if len(blob_list) == 0:
		return ""

	blob_str = "" #the return str.
	for blob in blob_list:
		#converts each of the important blob-attributes to a string and appends that to blob_list.
		blob_str += blobToString(blob_list[blob])
	return blob_str



#converts a list of formatted blob strings to a list of blob objects.
def blobsFromString(blob_strs):
	#handles the case of no blobs to convert.
	if blob_strs == "":
		return {}

	blob_list = {} 	#the return dict.
	conv_list = blob_strs.split(";")[:-1] #breaks the large string into smaller blob strings.
	for blob in conv_list:
		blob_obj = blobFromString(blob)
		blob_list[blob_obj.game_id] = blob_obj
	return blob_list

def resourceToString(resource):
	res_str = "%d:%d" % (resource.x, resource.y)
	return res_str

def resourceFromString(res_str):
	res_attr = res_str.split(":")
	for i in res_attr:
	return Resource(int(res_attr[0]), int(res_attr[1])) if len(res_attr) is 2 else None



class Resource:
	def __init__(self, x, y, radius=5, value=1):
		self.x = x
		self.y = y
		self.color = (0,255,0)
		self.radius = radius
		self.value = value


def makeResource(xBound, yBound):
	return Resource(
			randint(0, xBound), 
			randint(0, yBound)
		)