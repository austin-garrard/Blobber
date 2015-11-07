from blob import Blob
import time
from ast import literal_eval as make_tuple

#converts a blob to a formatted string
def blobToString(blob):
	blob_str = "%s:%.3f:%.3f:%.3f:%s:%.3f:%.3f:%.3f:%s;" % (blob.name,
			                                  				blob.x,
			                                  				blob.y,
			                                  				blob.radius,
						                                  	blob.color,
						                                  	blob.direction[0],
						                                  	blob.direction[1],
						                                  	blob.velocity,
						                                  	time.time() )
	return blob_str

#converts a formatted blob string to a blob object.
def blobFromString(blob_str):
	blob_attr = blob_str.split(":")
	blob_obj  = Blob(blob_attr[0],
					float(blob_attr[1]),
					float(blob_attr[2]), 
					float(blob_attr[3]),
					make_tuple(blob_attr[4]), 
					[float(blob_attr[5]),float(blob_attr[6])], 
					float(blob_attr[7]),
					float(blob_attr[8]))

	return blob_obj

#converts a list of blobs to a list of formatted strings.
def blobsToString(blob_list):
	#handles the case of no blobs to convert.
	if len(blob_list) == 0:
		return ""

	blob_str = "" #the return str.
	for blob in blob_list:
		#converts each of the important blob-attributes to a string and appends that to blob_list.
		blob_str += blobToString(blob)
	return blob_str



#converts a list of formatted blob strings to a list of blob objects.
def blobsFromString(blob_strs):
	#handles the case of no blobs to convert.
	if blob_strs == "":
		return []

	blob_list = [] 	#the return list.
	conv_list = blob_strs.split(";")[:-1] #breaks the large string into smaller blob strings.
	for blob in conv_list:
		blob_obj = blobFromString(blob)
		blob_list.append(blob_obj)
	return blob_list

def resourceToString(resource):
	res_str = "%.3f:%.3f;" % (resource.x, resource.y)
	return res_str

def resourceFromString(res_str):
	res_attr = res_str.split(":")
	res_obj  = 1



