"""
Created on Wed Sep 13 18:08:32 2023

@author: r.osipovskiy

EXAMPLE:

token = 'perm: '
proj_name = "01. "
base = 'http://youtrack.{domain name}.com/'

pars = TaskScrapper(token, base, proj_name )
pars.make_step()

"""

import requests
import json
from collections import deque as queue


class TaskScrapper:
    def __init__(self, token, url, project):

        self.state = dict()
        self.new_state = None # list
        self.changes = queue() # queue

        self.url = url
        self.token = token
        self.project = project.replace(' ', '+')

        self.request = f'api/issues?fields=id,idReadable,updated,summary,project(id,name),customFields(id,assign,updated,name,stage,value(fullName,id,isResolved,localizedName,name))&query=project:+%7B{self.project}%7D'

        self.head = {'Accept': 'application/json',
                     'Authorization': self.token,
                     'Cache-Control': 'no-cache'}

    def get_last_update(self) -> tuple:
        """

        """
        res = requests.get(self.url + self.request, headers=self.head)
        if res.status_code != 200:
            return (False, res)
        dcd_cnt = res.content.decode()
        try:
            cont = json.loads(dcd_cnt)
            self.new_state = cont
            return (True, 'ok')
        except Exception as e:
            return (False, e)

    def comit_changes(self) -> bool :
        if not self.new_state:
            return []

        for v in self.new_state:
            vals = {value['name']: value['value'] for value in v['customFields']}

            issue_id = v['idReadable'] #['id']
            upd_time = v['updated']
            summ = v['summary']

            use_key = 'name' if vals['Stage']['localizedName'] is None or not len(vals['Stage']['localizedName']) else 'localizedName'

            if issue_id not in self.state.keys():
                # add key
                self.state[issue_id] = {'updated': v['updated'],
                                        'summary': v['summary'],
                                        'stage': vals['Stage'][use_key]}
            else:
                # check time and stage
                if upd_time - self.state[issue_id]['updated']:
                    # update in state
                    if self.state[issue_id]['stage'] != vals['Stage'][use_key]:
                        # append to queue
                        self.changes.append({'id':issue_id,
                                             'summary':summ.replace('_', "\-").replace('*', "\*"),
                                             'prev_stage':self.state[issue_id]['stage'],
                                             'new_stage': vals['Stage'][use_key],
                                             'assign':vals['Assignee']['fullName']}
                                            )
                        self.state[issue_id]['stage'] = vals['Stage'][use_key]
                    self.state[issue_id]['updated'] = upd_time

        self.new_state = None
        return len(self.changes) > 0

    def make_step(self) -> tuple :
        """"""
        status, info = self.get_last_update()
        if status:
            return (self.comit_changes(), 'ok')
        else:
            return (status, info)

    def get_value(self) -> str :
        """ """
        if not len(self.changes):
            return None
        item = self.changes.pop()
        link_to_task = f"{self.url}/agiles/121-24/current?issue={item['id']}"
        msg = f"*{item['id']}* @{item['assign']}\n*stage*: {item['prev_stage']} -> {item['new_stage']}\n*Description:* {item['summary']};\n[link]({link_to_task})"
        return msg

