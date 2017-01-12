#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import json
slack_url = 'https://hooks.slack.com/services/T00000000/B00000000/000000000000000000000000'

slack_username='Slack username'

slack_to = sys.argv[1]
slack_subject = sys.argv[2]
lines = sys.argv[3].split('\n')
zbx_data = {}

for line in lines:
    if len(line.rstrip().split('=',1))>1:
        zbx_data[line.rstrip().split('=',1)[0]] = line.rstrip().split('=',1)[1]


slack_colors = { 'OK': '#FF3838', 'PROBLEM': '#43F060' }
slack_color = slack_colors['OK']
if 'PROBLEM' in slack_subject:
    slack_color = slack_colors['PROBLEM']

slack_sev = zbx_data['TRIGGER_SEVERITY']


slack_icons = { 'Disaster':         ':closed_book:',
                 'High':            ':orange_book:',
                 'Average':         ':ledger:',
                 'Warning':         ':notebook_with_decorative_cover:',
                 'Information':     ':blue_book:',
                 'Not classified':  ':notebook:',
               }


slack_icon = slack_icons[slack_sev]
slack_attach_title = zbx_data['TRIGGER_NAME'] + ": " + zbx_data['TRIGGER_VALUE']
slack_attach_pretext = ''

slack_attach_text = ''
for key in zbx_data.iterkeys():
    if ('ITEM_NAME' in key) and (zbx_data[key] != '*UNKNOWN*'):
        value_key = 'ITEM_VALUE'+key[-1]
        slack_attach_text = "{0}{1}: {2}\n".format(slack_attach_text, zbx_data[key], zbx_data[value_key])


try:
    slack_attach_text = slack_attach_text + zbx_data['TRIGGER_DESCRIPTION']
except KeyError:
    pass

try:
    slack_munin_url = zbx_data['INVENTORY_URL_A1']
except KeyError:
    slack_munin_url = ''
if 'UNKNOWN' in slack_munin_url or slack_munin_url=='':
    slack_munin_url = ''
    try:
        slack_attach_fallback = zbx_data['TRIGGER_NAME'] + '\n' + zbx_data['TRIGGER_DESCRIPTION']
    except KeyError:
        slack_attach_fallback = zbx_data['TRIGGER_NAME']
    slack_text = slack_icon + ' ' + zbx_data['HOST_NAME1']
else:
    slack_attach_fallback = slack_munin_url + '|' + zbx_data['TRIGGER_NAME'] + '>' + "\n" + zbx_data['TRIGGER_DESCRIPTION']
    slack_text = (slack_icon + " <" + slack_munin_url + "|" + zbx_data['HOST_NAME1'] + ">")



json_payload = {"channel" : slack_to,
                "username": slack_username,
                "text": slack_text,
                "attachments": [
                        { "fallback": slack_attach_fallback,
                          "color" : slack_color,
                          "title" : slack_attach_title,
                          "pretext" : slack_attach_pretext,
                          "text" : slack_attach_text,
                        }
                    ]
                }

payload = "payload=" + json.dumps(json_payload)
invoke = ['/usr/bin/curl', '-m', '5', '--data-urlencode', payload, slack_url]

subprocess.call(invoke)
