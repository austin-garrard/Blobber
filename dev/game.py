import blob_
import time
from ast import literal_eval as make_tuple


def blobsToString(blob_list):
	#takes a list of blobs and converts it to a string representation.
	#handles the case of no blobs to convert.
	if len(blob_list) == 0:
		return ""

	blob_str = "" #the return str.
	for blob in blob_list:
		print blob.name
		#converts each of the important blob-attributes to a string and appends that to blob_list.
		blob_str += "%s:%s:%s:%s:%s:%s:%s:%s:%s;" % (blob.name,
			                                  	blob.x,
			                                  	blob.y,
			                                  	blob.radius,
			                                  	blob.color,
			                                  	blob.direction[0],
			                                  	blob.direction[1],
			                                  	blob.velocity,
			                                  	time.time() )
		print blob_str
	return blob_str




def blobsFromString(blob_str):
	#takes a blob-list formatted string and converts it to a list of blobs.
	#handles the case of no blobs to convert.
	if blob_str == "":
		return []

	blob_list = [] 	#the return list.
	conv_list = blob_str.split(";")[:-1] #breaks the large string into smaller blob strings.
	for blob in conv_list:
		blob_attr = blob.split(":")
		blob_obj  = blob_.Blob(blob_attr[0],
								float(blob_attr[1]),
								float(blob_attr[2]), 
								float(blob_attr[3]),
								make_tuple(blob_attr[4]), 
								[float(blob_attr[5]),float(blob_attr[6])], 
								float(blob_attr[7]),
								float(blob_attr[8]))
		blob_list.append(blob_obj)
	return blob_list



