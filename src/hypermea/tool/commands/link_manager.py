import os
import glob
import re

import hypermea.tool
import hypermea.tool.commands._api
from hypermea.tool.code_gen import \
    ChildLinksInserter, \
    ParentLinksInserter, \
    DomainChildrenDefinitionInserter, \
    DomainRelationsInserter, \
    ChildLinksRemover, \
    ParentReferenceRemover, \
    DomainRelationsRemover
from hypermea.tool.commands._resource import _get_resource_list


class LinkManager:

    REMOTE_PREFIX = 'remote:'

    def __init__(self, parent, child, as_parent_ref=False):
        self.remote_parent = self.remote_child = False

        if parent.startswith(LinkManager.REMOTE_PREFIX):
            parent = parent[len(LinkManager.REMOTE_PREFIX):]
            self.remote_parent = True

        if child.startswith(LinkManager.REMOTE_PREFIX):
            child = child[len(LinkManager.REMOTE_PREFIX):]
            self.remote_child = True

        self.parent, self.parents = hypermea.tool.get_singular_plural(parent)  # TODO: validate, safe name, etc.
        self.child, self.children = hypermea.tool.get_singular_plural(child)  # TODO: validate, safe name, etc.
        self.parent_ref = '_parent_ref' if as_parent_ref else f'_{parent}_ref'

    def _link_already_exists(self):
        rels = LinkManager.get_relations()

        if 'children' in rels.get(self.parents, {}):
            needle = LinkManager.REMOTE_PREFIX + self.children if self.remote_child else self.children
            if needle in rels[self.parents]['children']:
                return True  # i.e. link does exist

        if self.remote_parent and 'parents' in rels.get(self.children, {}):
            needle = LinkManager.REMOTE_PREFIX + self.parent
            if needle in rels[self.children]['parents']:
                return True

        return False  # i.e. link does not exist

    def _list_missing_resources(self):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}/domain')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        rtn = ''
        if not self.remote_parent and not os.path.exists(f'./{self.parents}.py'):
            rtn += self.parents

        if not self.remote_child and not os.path.exists(f'./{self.children}.py'):
            if rtn:
                rtn += ', '

            rtn += self.children

        hypermea.tool.jump_back_to(starting_folder)
        return rtn

    def _validate(self):
        if self._link_already_exists():
            raise LinkManagerException(801, 'This link already exists')

        missing = self._list_missing_resources()
        if missing:
            raise LinkManagerException(802, f'missing local resource: {missing}')

        if self.remote_parent and self.remote_child:
            raise LinkManagerException(803, 'Both parent and child cannot be remote')

    @staticmethod
    def get_relations():
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}/domain')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        with open('__init__.py', 'r') as f:
            lines = f.readlines()

        dict_string = ''
        listening = False
        for line in lines:
            if line.startswith('DOMAIN_RELATIONS'):
                line = re.sub(r'DOMAIN_RELATIONS.*?=', '', line)
                listening = True

            if not listening:
                continue

            if line.startswith('}'):
                dict_string += '}'
                break

            dict_string += line

        dict_string = re.sub(r'["\']schema["\'].*?,', '', dict_string, flags=re.DOTALL)

        keep_trying = True
        result = ''
        while keep_trying:  # TODO: this is icky but works 99.9% of the time
            try:
                result = eval(dict_string)
                keep_trying = False
            except NameError as ex:
                variable_name = f'{ex}'.split("'")[1]
                dict_string = re.sub(variable_name, '0', dict_string, flags=re.DOTALL)

        resources = _get_resource_list()
        relations = {}
        for relation in result:
            child = result[relation]['resource_title']
            parent = relation.replace(f"_{child}", "")
            parent, parents = hypermea.tool.get_singular_plural(parent)
            child, children = hypermea.tool.get_singular_plural(child)

            if parents not in resources:
                continue

            if parents not in relations:
                relations[parents] = {}
            if 'children' not in relations[parents]:
                relations[parents]['children'] = set()
            relations[parents]['children'].add(children)

            if children not in relations:
                relations[children] = {}
            if 'parents' not in relations[children]:
                relations[children]['parents'] = set()
            relations[children]['parents'].add(parent)

        LinkManager._add_remote_relations(relations)

        hypermea.tool.jump_back_to(starting_folder)
        return relations

    @staticmethod
    def _add_remote_relations(rels):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}/hooks')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        files = [file for file in glob.glob('*.py') if not file.startswith('_')]

        for file in files:
            resource = file.split('.')[0]  # TODO: replace with more elegant basename or something
            with open(file, 'r') as f:
                lines = f.readlines()

            my_relationship = ''
            its_relationship = ''
            for line in lines:
                if line.startswith('def _add_remote_'):
                    my_relationship = line.split('_')[3]
                    if my_relationship == 'parent':
                        my_relationship = 'parents'
                    its_relationship = 'children' if my_relationship == 'parents' else 'parents'
                    continue
                elif line.startswith('def '):
                    my_relationship = ''
                    continue

                if my_relationship and '_links' in line:
                    remote = line.split("'")[3]
                    singular, plural = hypermea.tool.get_singular_plural(remote)
                    remote = 'remote:' + (singular if my_relationship == 'parents' else plural)
                    remotes = 'remote:' + plural
                    singular, plural = hypermea.tool.get_singular_plural(resource)
                    if resource not in rels:
                        rels[resource] = {}
                    if my_relationship not in rels[resource]:
                        rels[resource][my_relationship] = set()
                    rels[resource][my_relationship].add(remote)

                    if remotes not in rels:
                        rels[remotes] = {}
                    if resource not in rels[remotes]:
                        rels[remotes][its_relationship] = set()
                    rels[remotes][its_relationship].add(singular if its_relationship == 'parents' else plural)

        hypermea.tool.jump_back_to(starting_folder)

    def add(self):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        self._validate()
        print(
            f'Creating link rel from {"remote " if self.remote_parent else ""}{self.parent} (parent) '
            f'to {"remote " if self.remote_child else ""}{self.children} (children)'
        )

        if self.remote_parent:
            hypermea.tool.commands._api._add_addins({'add_validation': 'n/a'}, silent=True)

        # update parent code
        if not self.remote_parent:
            ParentLinksInserter(self).transform(f'hooks/{self.parents}.py', )

        # update child code
        if not self.remote_child:
            DomainRelationsInserter(self).transform('domain/__init__.py', )
            DomainChildrenDefinitionInserter(self).transform(f'domain/{self.children}.py')
            ChildLinksInserter(self).transform(f'hooks/{self.children}.py')

        hypermea.tool.jump_back_to(starting_folder)

    def remove(self):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        if not self._link_already_exists():
            raise LinkManagerException(804, f'There is no link from {self.parent} to {self.children}')

        print(f'Removing link from {self.parent} to {self.children}')

        DomainRelationsRemover(self.parents, self.children).transform('domain/__init__.py')
        if not self.remote_parent:
            ChildLinksRemover(self.children).transform(f'hooks/{self.parents}.py')

        # update child code
        if not self.remote_child:
            ParentReferenceRemover(self.parents).transform(f'domain/{self.children}.py')
            ChildLinksRemover(self.parents).transform(f'hooks/{self.children}.py')

        hypermea.tool.jump_back_to(starting_folder)


class LinkManagerException(Exception):
    def __init__(self, exit_code, message):
        super().__init__(message)
        self.exit_code = exit_code


