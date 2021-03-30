#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import os

from datetime import datetime

import freebox.api as freebox_api

import export._generic

from .objects	import SystemConfig

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

def	all():
	sys_json_raw = freebox_api.get_system()

	if 'result' not in sys_json_raw:
		log.error( "No result in request answer: %s" % sys_json_raw)
		return
	log.debug( "sys_json_raw == %s" % sys_json_raw)


	lJsonObjectSystemConfig	=	sys_json_raw['result']

	SystemConfig.fromJson(
		pApiPath	=	"system",
		pApiSubpath	=	'',
		pTagsDict	=	{},
		pJsonObjectSystemConfig	=	lJsonObjectSystemConfig
	)

# ##############################################################################
# ##############################################################################
