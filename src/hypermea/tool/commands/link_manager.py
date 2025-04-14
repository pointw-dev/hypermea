import json

import os
import os.path
import glob
import importlib.util
from typing import Dict, Set

from hypermea.core.domain import Relation

import hypermea.tool
import hypermea.tool.commands._service
from hypermea.tool.code_gen import (
    DomainChildrenDefinitionInserter,
    DomainRelationsInserter,
    ## ParentReferenceRemover,
    DomainRelationsRemover,
)
from hypermea.tool.commands._resource import _get_resource_list


class LinkManager:
    EXTERNAL_PREFIX = 'external:'

    def __init__(self, parent, child, as_parent_ref=False):
        self.relation = Relation.from_link_command(parent, child)
        self.parent, self.parents = hypermea.tool.get_singular_plural(self.relation.parent)
        self.child, self.children = hypermea.tool.get_singular_plural(self.relation.child)
        self.parent_ref = '_parent_ref' if as_parent_ref else f'_{self.relation.parent}_ref'

    def _link_already_exists(self):
        rels = LinkManager.get_relations()

        if 'children' in rels.get(self.parents, {}):
            needle = self.children if not self.relation.child_is_external else LinkManager.EXTERNAL_PREFIX + self.children
            if needle in rels[self.parents]['children']:
                return True

        if self.relation.parent_is_external and 'parents' in rels.get(self.children, {}):
            needle = LinkManager.EXTERNAL_PREFIX + self.parent
            if needle in rels[self.children]['parents']:
                return True

        return False

    def _list_missing_resources(self):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/service/domain')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        rtn = ''
        if not self.relation.parent_is_external and not os.path.exists(f'./{self.parent}.py'):
            rtn += self.parent

        if not self.relation.child_is_external and not os.path.exists(f'./{self.child}.py'):
            if rtn:
                rtn += ', '
            rtn += self.child

        hypermea.tool.jump_back_to(starting_folder)
        return rtn

    def _validate(self):
        if self._link_already_exists():
            raise LinkManagerException(801, 'This link already exists')

        missing = self._list_missing_resources()
        if missing:
            raise LinkManagerException(802, f'missing local resource: {missing}')

        if self.relation.parent_is_external and self.relation.child_is_external:
            raise LinkManagerException(803, 'Both parent and child cannot be external')

    @staticmethod
    def get_relations() -> Dict[str, Dict[str, Set[str]]]:
        relations: Dict[str, Dict[str, Set[str]]] = {}
        resources = _get_resource_list()

        try:
            starting_folder, _ = hypermea.tool.jump_to_folder('src/service')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        if not os.path.isfile('domain/_relations.py'):
            hypermea.tool.jump_back_to(starting_folder)
            return relations

        spec = importlib.util.spec_from_file_location("_relations", "domain/_relations.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        registry = getattr(module, 'RELATION_REGISTRY', [])
        for rel in registry:
            parent, parents = hypermea.tool.get_singular_plural(rel.parent)
            child, children = hypermea.tool.get_singular_plural(rel.child)

            if not rel.parent_is_external and parent not in resources:
                continue
            if parents not in relations:
                relations[parents] = {}
            if 'children' not in relations[parents]:
                relations[parents]['children'] = set()
            relations[parents]['children'].add(children if not rel.child_is_external else LinkManager.EXTERNAL_PREFIX + children)

            if children not in relations:
                relations[children] = {}
            if 'parents' not in relations[children]:
                relations[children]['parents'] = set()
            relations[children]['parents'].add(parent if not rel.parent_is_external else LinkManager.EXTERNAL_PREFIX + parent)

        LinkManager._add_external_relations(relations)
        hypermea.tool.jump_back_to(starting_folder)
        return relations

    @staticmethod
    def _add_external_relations(rels):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/service/hooks')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        files = [file for file in glob.glob('*.py') if not file.startswith('_')]

        for file in files:
            resource = file.split('.')[0]
            with open(file, 'r') as f:
                lines = f.readlines()

            my_relationship = ''
            its_relationship = ''
            for line in lines:
                if line.startswith('def _add_external_'):
                    my_relationship = line.split('_')[3]
                    if my_relationship == 'parent':
                        my_relationship = 'parents'
                    its_relationship = 'children' if my_relationship == 'parents' else 'parents'
                    continue
                elif line.startswith('def '):
                    my_relationship = ''
                    continue

                if my_relationship and '_links' in line:
                    external = line.split("'")[3]
                    singular, plural = hypermea.tool.get_singular_plural(external)
                    external = 'external:' + (singular if my_relationship == 'parents' else plural)
                    externals = 'external:' + plural
                    singular, plural = hypermea.tool.get_singular_plural(resource)
                    if resource not in rels:
                        rels[resource] = {}
                    if my_relationship not in rels[resource]:
                        rels[resource][my_relationship] = set()
                    rels[resource][my_relationship].add(external)

                    if externals not in rels:
                        rels[externals] = {}
                    if its_relationship not in rels[externals]:
                        rels[externals][its_relationship] = set()
                    rels[externals][its_relationship].add(singular if its_relationship == 'parents' else plural)

        hypermea.tool.jump_back_to(starting_folder)

    def add(self):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        self._validate()
        print(
            f'Creating link rel from {"external " if self.relation.parent_is_external else ""}{self.parent} (parent) '
            f'to {"external " if self.relation.child_is_external else ""}{self.children} (children)'
        )

        if self.relation.parent_is_external:
            hypermea.tool.commands._service._add_addins({'add_validation': 'n/a'}, silent=True)

        if not self.relation.child_is_external:
            DomainRelationsInserter(self).transform('domain/_relations.py')
            ## DomainChildrenDefinitionInserter(self).transform(f'domain/{self.children}.py')

        hypermea.tool.jump_back_to(starting_folder)

    def remove(self):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        if not self._link_already_exists():
            raise LinkManagerException(804, f'There is no link from {self.parent} to {self.children}')

        print(f'Removing link from {self.parent} to {self.children}')

        DomainRelationsRemover(self.parents, self.children).transform('domain/_relations.py')

        ## if not self.relation.child_is_external:
        ##     ParentReferenceRemover(self.parents).transform(f'domain/{self.children}.py')

        hypermea.tool.jump_back_to(starting_folder)


class LinkManagerException(Exception):
    def __init__(self, exit_code, message):
        super().__init__(message)
        self.exit_code = exit_code
