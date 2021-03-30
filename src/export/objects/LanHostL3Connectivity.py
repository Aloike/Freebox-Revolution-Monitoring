#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

# import export._generic
from ..	import	_generic

# ##############################################################################
# ##############################################################################

def	fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectLanHostL3Connectivity):

	# Set some tags
	lTags	=	pTagsDict.copy()
	lTags['l3connectivity_addr']	=	pJsonObjectLanHostL3Connectivity['addr']
	lTags['l3connectivity_af']	=	pJsonObjectLanHostL3Connectivity['af']

	#
	#	Iterate over available keys
	#
	for lJsonKey in pJsonObjectLanHostL3Connectivity:

		#
		#	Those keys are used in tags, skip them.
		#
		if	(	lJsonKey	==	'addr'
			or	lJsonKey	==	'af'	):
			continue

		#
		# Default export rule
		#
		else:
			_generic.measurement(
				pApiPath	=	pApiPath,
				pApiSubpath	=	pApiSubpath,
				pApiAttribute	=	lJsonKey,
				pAttrValue	=	pJsonObjectLanHostL3Connectivity[lJsonKey],
				pTagsDict	=	pTagsDict#,
				# pFieldsDict	=	lFields
			)

# ##############################################################################
# ##############################################################################
