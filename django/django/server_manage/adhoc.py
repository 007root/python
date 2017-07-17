#coding:utf-8
#!/bin/env python


import os
import sys
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.playbook.play import Play
from ansible import constants as C
from ansible.plugins.callback import CallbackBase
from ansible.executor.task_queue_manager import TaskQueueManager


# def Playbook_Run(host,playbook_path):
#     variable_manager = VariableManager()
#     loader = DataLoader()
#     inventory = Inventory(loader=loader,variable_manager=variable_manager,host_list=host)
#     Options = namedtuple('Options',['listtags','listtasks','listhosts','syntax','connection','module_path','forks','remote_user',
#                                     'private_key_file','ssh_common_args','ssh_extra_args','sftp_extra_args','scp_extra_args','become',
#                                     'become_method','become_user','verbosity','check'])
#     options = Options(listtags=False,listtasks=False,listhosts=False,syntax=False,connection='ssh',module_path=None,forks=100,remote_user='root',
#                       private_key_file=None,ssh_common_args=None,ssh_extra_args=None,sftp_extra_args=None,scp_extra_args=None,become=True,
#                       become_method=None,become_user='root',verbosity=None,check=False)
#     passwords = {}
#     pbex = PlaybookExecutor(playbooks=[playbook_path],inventory=inventory,variable_manager=variable_manager,loader=loader,options=options,
#                             passwords=passwords)
#     result = pbex.run()
#     return result


def Order_Run(host,module_name,module_args):
    class ResultCallback(CallbackBase):
        def __init__(self,*args,**kwargs):
            self.host_ok = {}
            self.host_unreachable = {}
            self.host_failed = {}
        def v2_runner_on_unreachable(self, result):
            self.host_unreachable[result._host.get_name()] = result

        def v2_runner_on_ok(self, result, *args, **kwargs):
            self.host_ok[result._host.get_name()] = result

        def v2_runner_on_failed(self, result, *args, **kwargs):
            self.host_failed[result._host.get_name()] = result

    variable_manager = VariableManager()
    loader = DataLoader()
    invertory = Inventory(loader=loader,variable_manager=variable_manager,host_list=host)
    Options = namedtuple('Options',['listtags','listtasks','listhosts','syntax','connection','module_path','forks','remote_user',
                                    'private_key_file','ssh_common_args','ssh_extra_args','sftp_extra_args','scp_extra_args','become',
                                    'become_method','become_user','verbosity','check'])
    options = Options(listtags=False,listtasks=False,listhosts=False,syntax=False,connection='ssh',module_path=None,forks=100,remote_user='root',
                      private_key_file=None,ssh_common_args=None,ssh_extra_args=None,sftp_extra_args=None,scp_extra_args=None,become=True,
                      become_method=None,become_user='root',verbosity=None,check=False)
    passwords = {}

    play_source = dict(
        name = 'Ansible Play',
        hosts = host,
        gather_facts = 'no',
        tasks = [dict(action=dict(module=module_name,args=module_args))]
    )
    play = Play().load(play_source,variable_manager=variable_manager,loader=loader)

    tqm = None
    callback = ResultCallback()
    try:
        tqm = TaskQueueManager(
            inventory=invertory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            stdout_callback=callback,
            run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
            run_tree=False,
        )
        tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()


    results_raw = {}
    results_raw['success'] = {}
    results_raw['failed'] = {}
    results_raw['unreachable'] = {}

    for host,result in callback.host_ok.items():

        if result._result.get('stdout_lines'):
            if result._result['stdout_lines']:
                results_raw['success'][host] = json.dumps(result._result['stdout_lines'])
            else:
                result._result['stdout_lines']='success'.split() # 成功返回success字符串
                results_raw['success'][host] = json.dumps(result._result['stdout_lines'])

    for host,result in callback.host_failed.items():

        if result._result.get('stderr'):
            results_raw['failed'][host] = result._result['stderr']
        elif result._result.get('msg'):
            results_raw['failed'][host] = result._result['msg'] # copy模块error信息返回

    for host,result in callback.host_unreachable.items():
        results_raw['unreachable'][host] = result._result['msg']
    return results_raw











