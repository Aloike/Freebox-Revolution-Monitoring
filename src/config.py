#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import os


def init():
	global FREEBOX_HOST
	FREEBOX_HOST = os.getenv('FREEBOX_HOST', 'mafreebox.freebox.fr')

	global INFLUXDB_MEASUREMENT
	INFLUXDB_MEASUREMENT = os.getenv('INFLUXDB_MEASUREMENT', 'freebox')
