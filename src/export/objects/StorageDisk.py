#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

from ..	import	_generic

# ##############################################################################
# ##############################################################################
#
#	Logging configuration
#
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# ##############################################################################
# ##############################################################################

def	fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectStorageDisk):

	if 'id' not in pJsonObjectStorageDisk:
		log.error("This StorageDisk doesn't have any 'id'!")
		return


	lTags	=	pTagsDict.copy()

	# Add the station unique ID in the tags to identify the station
	lTags['disk_id']	=	pJsonObjectStorageDisk['id']


	#
	#	Iterate over attributes and export them
	#
	for lJsonKey in pJsonObjectStorageDisk:

		#
		#	Those keys are used in tags, skip them.
		#
		if	(	lJsonKey	==	'id'	):
			continue

		#
		# Default export rule
		#
		else:
			_generic.measurement(
				pApiPath	=	pApiPath,
				pApiSubpath	=	pApiSubpath,
				pApiAttribute	=	lJsonKey,
				pAttrValue	=	pJsonObjectStorageDisk[lJsonKey],
				pTagsDict	=	lTags#,
				# pFieldsDict	=	lFields
			)

# ##############################################################################
# ##############################################################################