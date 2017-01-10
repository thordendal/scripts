#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
slack_url = 'https://hooks.slack.com/services/YOUR/HOOK/KEY'
slack_username='Slack username'

slack_to = sys.argv[1]
slack_subject = sys.argv[2]
lines = sys.argv[3].split('\n')
zbx_data = {}

for line in lines:
    if len(line.rstrip().split('=',1))>1:
        zbx_data[line.rstrip().split('=',1)[0]] = line.rstrip().split('=',1)[1]

slack_icon = ':white_check_mark:'
if 'PROBLEM' in slack_subject:
    slack_icon = ':warning:'

slack_sev = zbx_data['TRIGGER_SEVERITY']

slack_colors = { 'Disaster': '#FF3838',
                 'High': '#FF9999',
                 'Average': '#FFF6A5',
                 'Warning': '#FFF6A5',
                 'Information': '#D6F6FF',
                 'Not classified': '#BBBBBB',
               }

slack_color = slack_colors[slack_sev]
slack_attach_title = zbx_data['TRIGGER_NAME'] + ": " + zbx_data['TRIGGER_VALUE']
slack_attach_pretext = ''
slack_attach_text = zbx_data['ITEM_NAME1'] + ": " + zbx_data['ITEM_VALUE1'].replace('"','&quot;') + "\n" + zbx_data['TRIGGER_DESCRIPTION']

try:
    slack_munin_url = zbx_data['INVENTORY_URL_A1']  + "\n" + zbx_data['TRIGGER_DESCRIPTION']
except KeyError:
    slack_munin_url = ''
if 'UNKNOWN' in slack_munin_url:
    slack_munin_url = ''
slack_attach_fallback = '<' + slack_munin_url + '|' + zbx_data['TRIGGER_NAME'] + '>' + "\n" + zbx_data['TRIGGER_DESCRIPTION']

json_payload = {"channel" : slack_to,
                "username": slack_username,
                "text": (slack_icon + " <" + slack_munin_url + "|" + zbx_data['HOST_NAME1'] + ">"),
                "attachments": [
                        { "fallback": slack_attach_fallback,
                          "color" : slack_color,
                          "title" : "",
                          "pretext" : slack_attach_pretext,
                          "text" : slack_attach_title + "\n" + slack_attach_text } ] }

invoke = "/usr/bin/curl -m 5 --data-urlencode 'payload=" + json.dumps(json_payload) + "' '" + slack_url + "'"
os.system(invoke)