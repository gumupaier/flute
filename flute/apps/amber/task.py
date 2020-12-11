# -*- coding: utf-8 -*-
# @Time    : 2020/12/10 5:09 下午
# @File    : task.py
import yaml
import inquirer


class StackfileGenerator(object):
    def __init__(self):
        self._template = None
        self._metad_tpl = None
        self._storaged_tpl = None
        self._graphd_tpl = None
        self.usr_cfg = dict()

    def load_template(self):
        with open('./template/docker-stack-template.yml') as f:
            self._template = yaml.load(f, Loader=yaml.FullLoader)

        self._metad_tpl = self._template['services']['metad']
        self._storaged_tpl = self._template['services']['storaged']
        self._graphd_tpl = self._template['services']['graphd']
        print(self._template)
        print(self._metad_tpl)
        print(self._storaged_tpl)
        print(self._graphd_tpl)

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
        pass

    def update_image(self):
        pass

    def generate_file(self):
        with open(r'./docker-stack.yaml', 'w') as f:
            yaml_str = yaml.safe_dump(self._template,
                                      default_flow_style=False,
                                      width=50,
                                      indent=2).replace(r"''", '').replace('null', '')
            f.write(yaml_str)


if __name__ == '__main__':
    sg = StackfileGenerator()
    # sg.load_template()
    sg.process()
