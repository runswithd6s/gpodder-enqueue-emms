# -*- coding: utf-8 -*-
# Simple extension to enqueue episodes to EMMS player. Will start
# Emacs in daemon mode if it isn't already running.
#
# Requirements: gPodder 3.x (or "tres" branch newer than 2011-06-08)
#
# (c) 2016-09-01 Chad Walstrom <gchewie@gmail.com>
#
# Released GNU Public License v3.0 or greater

import subprocess

import logging
logger = logging.getLogger(__name__)

# Provide some metadata that will be displayed in the gPodder GUI
__title__ = 'Enqueue to EMMS'
__description__ = 'Enqueue to EMMS, the Emacs MultiMedia Server'
__only_for__ = 'gtk, cli, qml'
__authors__ = 'Chad Walstrom <gchewie@gmail.com>'


class gPodderExtension(object):
    # The extension will be instantiated the first time it's used
    # You can do some sanity checks here and raise an Exception if
    # you want to prevent the extension from being loaded..
    def __init__(self, container):
        self.container = container

    # This function will be called when the extension is enabled or
    # loaded. This is when you want to create helper objects or hook
    # into various parts of gPodder.
    def on_load(self):
        logger.info('Extension is being loaded.')

    # This function will be called when the extension is disabled or
    # when gPodder shuts down. You can use this to destroy/delete any
    # objects that you created in on_load().
    def on_unload(self):
        logger.info('Extension is being unloaded.')

    def _enqueue_episodes(self, episodes):
        filenames = [episode.get_playback_url() for episode in episodes]
        for filename in filenames:
            cmd = ['emacsclient', '-a', ' \"\"', '--eval', '(emms-add-file \"%s\")' % filename]
            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def on_episodes_context_menu(self, episodes):
        return [('Enqueue in EMMS', self._enqueue_episodes)]
