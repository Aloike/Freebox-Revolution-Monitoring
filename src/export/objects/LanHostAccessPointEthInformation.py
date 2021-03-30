#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

from ..	import	_generic

# ##############################################################################
# ##############################################################################

def	fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectEthInfo):

	#
	#	Iterate over available keys
	#
	for lJsonKey in pJsonObjectEthInfo:

		_generic.measurement(
			pApiPath	=	pApiPath,
			pApiSubpath	=	pApiSubpath,
			pApiAttribute	=	lJsonKey,
			pAttrValue	=	pJsonObjectEthInfo[lJsonKey],
			pTagsDict	=	pTagsDict#,
			# pFieldsDict	=	lFields
		)

# ##############################################################################
# ##############################################################################