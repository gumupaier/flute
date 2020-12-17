# -*- coding: utf-8 -*-
# @Time    : 2020/12/10 5:09 下午
# @File    : task.py
import yaml
import inquirer
import copy

from flute.apps.amber.const import VERSION_IMAGE_MAP


class StackfileGenerator(object):
    def __init__(self):
        self._template = None
        self._yaml = None
        self._metad_tpl = None
        self._storaged_tpl = None
        self._graphd_tpl = None
        self.usr_cfg = dict()

    def load_template(self):
        import os
        tmp_path = os.path.dirname(__file__)
        tmp_path = os.path.join(tmp_path, 'template/docker-stack-template.yml')
        with open(tmp_path) as f:
            self._template = yaml.load(f, Loader=yaml.FullLoader)

        self._metad_tpl = self._template['services']['metad']
        self._storaged_tpl = self._template['services']['storaged']
        self._graphd_tpl = self._template['services']['graphd']

    def ip_validation(self, answers, current):
        ip_list = current.split()
        if not ip_list:
            return False
        for ip_addr in ip_list:
            sep = ip_addr.split('.')
            if len(sep) != 4:
                return False
            for i, x in enumerate(sep):
                try:
                    int_x = int(x)
                    if int_x < 0 or int_x > 255:
                        return False
                except ValueError as e:
                    return False
        return True

    def process(self):
        self.load_template()
        self.user_config()
        self.update_yaml()
        self.generate_file()

    def user_config(self):
        #  ip and version config
        questions = [
            inquirer.Text('ip_list',
                          message="What's your ip list",
                          validate=self.ip_validation,
                          ),
            inquirer.List('version',
                          message="What version of Nebula will you deploy?",
                          choices=['nightly', '1.1', '1.2'],
                          default='nightly'
                          ),
        ]
        answers = inquirer.prompt(questions)
        self.usr_cfg.update(
            {'version': answers['version'], 'ip_list': answers['ip_list'].split(),
             'roles': {'metad': set(), 'storaged': set(),
                       'graphd': set()}, 'hostnames': dict()})

        # machine configuration
        for _machine in self.usr_cfg['ip_list']:
            questions = [
                inquirer.Checkbox('roles',
                                  message=f"Select the machine role with IP as {_machine}",
                                  choices=['metad', 'graphd', 'storaged']),
                inquirer.Text('hostname',
                              message=f"What is the hostname of the machine with IP as {_machine}?"),
            ]
            answers = inquirer.prompt(questions)
            for v in answers['roles']:
                self.usr_cfg['roles'][v].add(_machine)
            self.usr_cfg['hostnames'][_machine] = answers['hostname']

    def update_yaml(self):
        self._yaml = copy.deepcopy(self._template)
        # update metad service
        metad_cfg = copy.deepcopy(self._metad_tpl)
        metad_cfg['image'] = VERSION_IMAGE_MAP['metad'].get(self.usr_cfg['version'])
        # update meta_server config
        metad_server_str = '--meta_server_addrs=' + ','.join([f'{v}:45500' for v in self.usr_cfg['roles']['metad']])
        metad_cfg['command'][0] = metad_server_str
        services = dict()

        for index, meta_ip in enumerate(self.usr_cfg['roles']['metad']):
            _meta_cfg = copy.deepcopy(metad_cfg)
            _meta_cfg['command'][1], _meta_cfg['command'][2] = f'--local_ip={meta_ip}', f'--ws_ip={meta_ip}'
            _meta_cfg['deploy']['placement']['constraints'], _meta_cfg['healthcheck']['test'][3] = [
                                                                                                       f'node.hostname == {self.usr_cfg["hostnames"][meta_ip]}'], f'http://{meta_ip}:11000/status'
            _meta_cfg['volumes'] = [f'data-metad{index}:/data/meta', f'logs-metad{index}:/logs']
            services[f'metad{index}'] = _meta_cfg

        # update storage service
        storage_cfg = copy.deepcopy(self._storaged_tpl)
        storage_cfg['image'] = VERSION_IMAGE_MAP['storaged'].get(self.usr_cfg['version'])
        # update storage_server config
        storage_cfg['command'][0] = metad_server_str
        for index, storage_ip in enumerate(self.usr_cfg['roles']['storaged']):
            _storage_cfg = copy.deepcopy(storage_cfg)
            _storage_cfg['command'][1], _storage_cfg['command'][2] = f'--local_ip={storage_ip}', f'--ws_ip={storage_ip}'
            _storage_cfg['deploy']['placement']['constraints'], _storage_cfg['healthcheck']['test'][3] = [
                                                                                                             f'node.hostname == {self.usr_cfg["hostnames"][storage_ip]}'], f'http://{storage_ip}:12000/status'
            _storage_cfg['volumes'] = [f'data-storaged{index}:/data/meta', f'logs-storaged{index}:/logs']
            services[f'storaged{index}'] = _storage_cfg

        # update graph service
        graph_cfg = copy.deepcopy(self._graphd_tpl)
        graph_cfg['image'] = VERSION_IMAGE_MAP['graphd'].get(self.usr_cfg['version'])
        # update graph_server config
        graph_cfg['command'][0] = metad_server_str
        for index, graph_ip in enumerate(self.usr_cfg['roles']['graphd']):
            _graph_cfg = copy.deepcopy(graph_cfg)
            _graph_cfg['command'][1], _graph_cfg['command'][2] = f'--local_ip={graph_ip}', f'--ws_ip={graph_ip}'
            _graph_cfg['deploy']['placement']['constraints'], _graph_cfg['healthcheck']['test'][3] = [
                                                                                                         f'node.hostname == {self.usr_cfg["hostnames"][graph_ip]}'], f'http://{graph_ip}:13000/status'
            _graph_cfg['volumes'] = [f'data-graphd{index}:/data/meta', f'logs-graphd{index}:/logs']
            services[f'graphd{index}'] = _graph_cfg

        self._yaml['services'] = services

        self._yaml['volumes'] = dict()
        for str in ('metad', 'storaged', 'graphd'):
            self._yaml['volumes'].update({
                f'logs-{str}{index}': None
                for index, value in enumerate(self.usr_cfg['roles'][str])})
            if str != 'graphd':
                self._yaml['volumes'].update({
                    f'data-{str}{index}': None
                    for index, value in enumerate(self.usr_cfg['roles'][str])})

    def generate_file(self):
        with open(r'./docker-stack.yaml', 'w') as f:
            yaml_str = yaml.safe_dump(self._yaml,
                                      default_flow_style=False,
                                      width=50,
                                      indent=2).replace(r"''", '').replace('null', '')
            f.write(yaml_str)


if __name__ == '__main__':
    sg = StackfileGenerator()
    # sg.load_template()
    sg.process()
