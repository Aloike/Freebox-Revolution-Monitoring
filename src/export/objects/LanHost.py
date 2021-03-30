#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import export._generic

from .	import LanHostAccessPoint
from .	import LanHostL2Ident
from .	import LanHostL3Connectivity
from .	import LanHostName

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

def	fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectLanHost):

	lTags	=	pTagsDict.copy()

	lTags['host_id']	=	pJsonObjectLanHost['id']


	#
	#	Iterate over available keys
	#
	for lJsonKey in pJsonObjectLanHost:

		#
		#	Those keys are used in tags, skip them.
		#
		if	(	lJsonKey	==	'id'	):
			continue

		#
		# Those keys identify subpath; they are managed separately.
		#
		elif	lJsonKey	==	'access_point':
			LanHostAccessPoint.fromJson(
				pApiPath,
				pApiSubpath + '/access_point',
				lTags,
				pJsonObjectLanHost[lJsonKey]
			)

		elif	lJsonKey	==	'l2ident':
			LanHostL2Ident.fromJson(
				pApiPath,
				pApiSubpath + '/l2ident',
				lTags,
				pJsonObjectLanHost[lJsonKey]
			)

		elif	lJsonKey	==	'l3connectivities':

			lTagsLanHostL3Connectivity	= lTags.copy()

			# Iterate over connectivities and export them
			lConnCount	=	len(pJsonObjectLanHost[lJsonKey])
			lConnIdx	=	0
			while lConnIdx < lConnCount :

				lJsonObjLanHostL3Connectivity	=	pJsonObjectLanHost[lJsonKey][lConnIdx]

				# lTagsLanHostL3Connectivity['nameIdx']	=	lNameIdx
				LanHostL3Connectivity.fromJson(
					pApiPath,
					pApiSubpath + '/l3connectivities',
					lTagsLanHostL3Connectivity,
					lJsonObjLanHostL3Connectivity
				)
				lConnIdx	=	lConnIdx + 1

		elif	lJsonKey	==	'names':
			lTagsLanHostName	= lTags.copy()

			# Iterate over names and export them
			lNamesCount	=	len(pJsonObjectLanHost[lJsonKey])
			lNameIdx	=	0
			while lNameIdx < lNamesCount :
				lTagsLanHostName['nameIdx']	=	lNameIdx
				LanHostName.fromJson(
					pApiPath,
					pApiSubpath + '/names',
					lTagsLanHostName,
					pJsonObjectLanHost[lJsonKey][lNameIdx]
				)
				lNameIdx	=	lNameIdx + 1

		#
		# Default export rule
		#
		else:
			export._generic.measurement(
				pApiPath	=	pApiPath,
				pApiSubpath	=	pApiSubpath,
				pApiAttribute	=	lJsonKey,
				pAttrValue	=	pJsonObjectLanHost[lJsonKey],
				pTagsDict	=	lTags#,
				# pFieldsDict	=	lFields
			)

# ##############################################################################
# ##############################################################################