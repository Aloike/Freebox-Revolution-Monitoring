#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import os

from datetime import datetime

import freebox.api as fbx_api

import export._generic

# ##############################################################################
# ##############################################################################
#
#	Logging configuration
#
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# ##############################################################################
# ##############################################################################

def __get_creation_date(pFile):
	stat	=	os.stat(pFile)
	return stat.st_mtime

# ##############################################################################
# ##############################################################################

def	all(pFile, pVersion):

	lApiPath	=	'exporterInfos'
	# # Convertir Timestamp en datetime
	# update_date = datetime.fromtimestamp(__get_creation_date(__file__))
	# update_str = datetime.ctime(update_date)


	# export._generic.measurementNew(
	# 	pApiPath	=	lApiPath,
	# 	pApiAttribute	=	'file',
	# 	pAttrValue	=	pFile
	# )


	# # Export git version description
	# lGitDescription	=	"no_description"
	# try:
	# 	lGitDescription = subprocess.check_output(
	# 			["git", "describe", "--long", "--tags", "--always", "--dirty"] 
	# 		).strip().decode('utf-8')
	# except:
	# 	lGitDescription	=	"(git describe error)"


	export._generic.measurement(
		pApiPath	=	lApiPath,
		pApiAttribute	=	'version',
		pAttrValue	=	pVersion
	)


# ##############################################################################
# ##############################################################################
