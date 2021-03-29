#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

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

def	config():

	# Fetch connection stats
	lJsonAnswer	=	fbx_api.get_lan_config()
	if 'result' not in lJsonAnswer:
		return
	# log.debug( "lJsonAnswer == %s" % lJsonAnswer )


	export._generic.genericJson(
		pApiPath		=	'lan/config',
		pJsonRoot		=	lJsonAnswer,
		pJsonObjectName	=	'result'
	)

# ##############################################################################
# ##############################################################################
