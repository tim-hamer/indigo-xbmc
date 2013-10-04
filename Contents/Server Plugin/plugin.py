#! /usr/bin/env python # -*- coding: utf-8 -*-
####################

import jsonrpclib, sys, os, pprint

class Plugin(indigo.PluginBase):

############## --- Indigo Plugin Methods --- ##############

    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = True

	def __del__(self):
		indigo.PluginBase.__del__(self)

	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

############## --- Helper Methods --- ##############

    def getServer(self, device):
        user = device.pluginProps['username']
        pwd = device.pluginProps['password']
        ip = device.pluginProps['ipaddress']
        port = device.pluginProps['port']

        return jsonrpclib.Server("http://"+user+":"+pwd+"@"+ip+":"+port+"/jsonrpc")

    def methodFromString(self, device, prefix, methodName):
        if methodName is None or prefix is None:
            self.debugLog(u"ERROR: both prefix and method name must be specified.")
            return
        fullName = prefix+"."+methodName
        try:
            return getattr(self.getServer(device), fullName)
        except AttributeError:
            self.debugLog(u"ERROR: method not found for '"+fullName+"'")
            return None

    def getCurrentPlayerId(self, device):
        server = self.getServer(device)
        response = server.player.getActivePlayers()

        return response[0]['playerid']

############## --- Action Methods --- ##############

    def navigate(self, action, device):
        method = self.methodFromString(device, 'input', action.props['direction'])

        if method is None:
            self.debugLog(u"ERROR: unable to perform action")
            return
        
        result = method()
        self.debugLog(u"result: " + result)

    def playback(self, action, device):
        currentPlayerId = self.getCurrentPlayerId(device)
        method = self.methodFromString(device, 'player', action.props['command'])
        
        if method is None:
            self.debugLog(u"ERROR: unable to perform action")
            return

        result = method(currentPlayerId)

    def seek(self, action, device):
        currentPlayerId = self.getCurrentPlayerId(device)
        stepSize = action.props['stepSize']

        method = self.methodFromString(device, 'player', 'seek')

        if method is None:
            self.debugLog(u"ERROR: unable to perform action")
            return

        result = method(currentPlayerId, stepSize)
