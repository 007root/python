#!/usr/bin/env python3
# coding:utf8
# pip3 install python-jenkins==1.5.0
# 8/28/2019
"""
Also you can create a configuration file.
cat ~/.conf.json
{
"url": "jeknins.com/jeknins/",
"user": "username",
"token": "token"
}
"""

import json
import jenkins
import requests
import time
import argparse
from argparse import RawTextHelpFormatter


class Jenkins(jenkins.Jenkins):

    def get_views_job(self, view_url):
        suffix = 'api/python'
        url = view_url + suffix
        ret = server.jenkins_open(requests.Request('GET', url))
        ret = ret.replace('None','null')
        ret = json.loads(ret)
        jobs = ret.get('jobs')
        job_list = []
        for job in jobs:
            name = job.get('name')
            if 'AAA' in name:
                continue
            job_list.append(name)
        return job_list

    def get_parameter(self, job_name):
        ret = {}
        try:
            actions = self.get_job_info(job_name).get('actions')
            parameterDefinitions = actions[0].get('parameterDefinitions')

            for params in parameterDefinitions:
                result = params.get('defaultParameterValue')
                if result:
                    ret[params.get('name')] = result.get('value').split(':')[0]

            return ret
        except:
            return ret
    
    def job_check(self, item_id, get_color=False):
        task = self.get_queue_item(item_id).get('task')
        color = task.get('color')
        if get_color:
            return color
        if 'anime' in color:
            return True
        return False
    
    def build(self, jobs=None, view_name=None, 
             parameters={}, build_all=False):
        """
        jenkins build job.
        build one job or job list.
        :param jobs: on job name or job list, ``str | list``
        :param view_name: build all jobs of one view  build_all must be True, ``str``
        :param parameters: build param, ``dict``
        :param build_all: ``bool``
        """
        err = {}
        if jobs:
            if not isinstance(jobs, list):
                jobs = jobs.split(',')
        else:
            if view_name and build_all:
                for view in self.get_views():
                    if view.get('name') == view_name:
                        view_url = view.get('url')
                        break
                jobs = self.get_views_job(view_url)
        if not jobs:
            return
        total = len(jobs)
        build_num = 0
        print('total: {}'.format(total))
        for job in jobs:
            if not self.job_exists(job):
                print(job, ' Not found\r')
                build_num += 1
                continue

            parameters.update(self.get_parameter(job))
            item_id = self.build_job(job, parameters=parameters)
            build_num += 1
            print('build: {} building...{}\r'.format(build_num, job),)
            time.sleep(3)
            while True:
                if self.job_check(item_id):
                    time.sleep(3)
                    continue
                color = self.job_check(item_id, True)
                if 'red' in color:
                    err[job] = 'Build error'
                break
            time.sleep(5)
        print('\nerr:', err)


if __name__ == '__main__':
    def get_parse():
        arg = argparse.ArgumentParser()
        arg = argparse.ArgumentParser(description='Example:\n\tjenkins_api.py -j [gofun-ms|gofun-ms-pay,gofun-ms-ser]\n\t\
jenkins_api.py -v view_name -a ', formatter_class=RawTextHelpFormatter)
        arg.add_argument("-l", "--url", help="jenkins address")
        arg.add_argument("-u", "--user", help="username")
        arg.add_argument("-p", "--token", help="token")
        arg.add_argument("-j", "--job", help="single job name or comma-separated multiple job names")
        arg.add_argument("-v", "--view", help="view name, build all jobs of view")
        arg.add_argument("-a", "--build-all", action="store_true",
                         help="build all jobs of view, must be True")
        return arg.parse_args()

    args = vars(get_parse())
   
    url = args.get('url') 
    user = args.get('user')
    token = args.get('token')
    if not url and not user and not token:
        import os
        home = os.environ['HOME']
        config = home + '/.conf.json'
        assert os.path.exists(config), 'Not found conf.py'
        f = open(config)
        conf = json.loads(f.read())
        url = conf.get('url')
        user = conf.get('user')
        token = conf.get('token')
    assert url and user and token, 'Not userlogin'    

    server = Jenkins(url,
                     username=user,
                     password=token)

    server.build(jobs = args.get('job'),
          view_name = args.get('view'),
          build_all = args.get('build_all'))


