#!/usr/bin/env python
# Setup Gmail OAuth2 authentication easily
# Copyright (C) 2016 Ingo Hoffmann, Tiago Moreira Vieira
# <ingo@hoffmann.cx>, 
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# This script is based on Google Calendar Command Line Interface work
# https://github.com/insanum/gcalcli
# Python 2
# Google API Client Python 2 module
# A love for the command line!

import os
import httplib2
import json
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

class GmailOauth2:
	# These must be setup by offlineimap author?
	client_id = '1053103103160-udpnkreqpfk09kblb7pfhaahopcq93oq.apps.googleusercontent.com'
	client_secret = 'PHjktEMD7BST57Y6R3YAQN57'

	config_folder = "~/tmp"
	config_file = "offlineimap_oauth"
	authHttp = None

	def _GoogleAuth(self):
	    if not self.authHttp:
	        if self.config_folder:
	            storage = Storage(os.path.expanduser("{0}/{1}".format(
	                                                 unicode(self.config_folder), unicode(self.config_file))))
	        else:
	            storage = Storage(os.path.expanduser('~/%s' % self.config_file))
	        
	        credentials = storage.get()

	        if credentials is None or credentials.invalid:
	            credentials = run(
	                OAuth2WebServerFlow(
	                    client_id=self.client_id,
	                    client_secret=self.client_secret,
	                    scope=['https://mail.google.com/'],
	                    user_agent='offlineimap' + '/' + '6.7.0'),
	                storage)

	        self.authHttp = credentials.authorize(httplib2.Http())

	    return self.authHttp

	def read_access_token(self):
		oauth_credential_file = open(os.path.expanduser("{0}/{1}".format(unicode(self.config_folder), self.config_file)))
		os.remove(os.path.expanduser("{0}/{1}".format(unicode(self.config_folder), self.config_file)))
		json_credential = json.load(oauth_credential_file)
		return json_credential['token_response']['access_token']


if __name__ == '__main__':
	gmail = GmailOauth2()
	gmail._GoogleAuth()
	print gmail.read_access_token()