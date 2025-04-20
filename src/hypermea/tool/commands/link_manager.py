import os
import os.path
import glob
import importlib.util
from argparse import ArgumentError
from typing import Dict, Set

from hypermea.core.domain import Relation, external, get_resource_model_by_rel
from hypermea.core.utils import get_singular_plural

import hypermea.tool
import hypermea.tool.commands._service
from hypermea.tool.code_gen import (
    DomainRelationsInserter,
    DomainRelationsRemover,
    ParentLinksInserter,
    ChildLinksInserter
)


class LinkManager:
    EXTERNAL_PREFIX = 'external:'

    def __init__(self, parent: str, child: str):
        relation = Relation(parent=parent, child=child)

        parent_name = str(relation.parent)
        child_name = str(relation.child)

        parent_class = get_resource_model_by_rel(parent_name)
        child_class = get_resource_model_by_rel(child_name)

        is_parent_valid = parent_class is not None or relation.parent.external
        is_child_valid = child_class is not None or relation.child.external

        if not (is_parent_valid and is_child_valid):
            problems = []
            if not is_parent_valid:
                problems.append(f'Parent "{parent}" must either exist in the domain or be prefixed with "external:"')
            if not is_child_valid:
                problems.append(f'Child "{child}" must exist in the domain or be prefixed with "external:"')
            raise ArgumentError(None, 'Invalid link: ' + ' '.join(problems))

        self.parent, self.parents = (
            get_singular_plural(parent_name) if relation.parent.external else parent_class.singplu()
        )
        self.child, self.children = (
            get_singular_plural(child_name) if relation.child.external else child_class.singplu()
        )

        self.relation = Relation(
            parent=external(self.parent) if relation.parent.external else self.parent,
            child=external(self.child) if relation.child.external else self.child,
        )
        self.parent_ref = f'_{self.relation.parent}_ref'


    def _link_already_exists(self):
        rels = LinkManager.get_relations()

        if 'children' in rels.get(self.parents, {}):
            needle = self.children  # if not self.relation.child.external else LinkManager.EXTERNAL_PREFIX + self.children
            if needle in rels[self.parents]['children']:
                return True

        if 'parents' in rels.get(self.children, {}):
            needle = self.parent
            if needle in rels[self.children]['parents']:
                return True

        return False

    def _list_missing_resources(self):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/service/domain')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        rtn = ''
        if not self.relation.parent.external and not os.path.exists(f'./{self.parent}.py'):
            rtn += self.parent

        if not self.relation.child.external and not os.path.exists(f'./{self.child}.py'):
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

    @staticmethod
    def get_relations() -> Dict[str, Dict[str, Set[str]]]:
        try:
            starting_folder, _ = hypermea.tool.jump_to_folder('src/service')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        relations: Dict[str, Dict[str, Set[str]]] = {}

        if not os.path.isfile('domain/_relations.py'):
            hypermea.tool.jump_back_to(starting_folder)
            return relations

        registry = LinkManager.get_relation_registry()
        for rel in registry:
            parent, parents = get_singular_plural(str(rel.parent))
            child, children = get_singular_plural(str(rel.child))

            if parents not in relations:
                relations[parents] = {}
            if 'children' not in relations[parents]:
                relations[parents]['children'] = set()
            relations[parents]['children'].add(children if not rel.child.external else LinkManager.EXTERNAL_PREFIX + children)

            if children not in relations:
                relations[children] = {}
            if 'parents' not in relations[children]:
                relations[children]['parents'] = set()
            relations[children]['parents'].add(parent if not rel.parent.external else LinkManager.EXTERNAL_PREFIX + parent)

        LinkManager._add_external_relations(relations)
        hypermea.tool.jump_back_to(starting_folder)
        return relations

    @staticmethod
    def get_relation_registry():
        spec = importlib.util.spec_from_file_location("_relations", "domain/_relations.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        registry = getattr(module, 'RELATION_REGISTRY', [])
        return registry

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
                    singular, plural = get_singular_plural(external)
                    external = 'external:' + (singular if my_relationship == 'parents' else plural)
                    externals = 'external:' + plural
                    singular, plural = get_singular_plural(resource)
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
            f'Creating link rel from {"external " if self.relation.parent.external else ""}{self.parent} (parent) '
            f'to {"external " if self.relation.child.external else ""}{self.children} (children)'
        )

        DomainRelationsInserter(self).transform('domain/_relations.py')
        if self.relation.parent.external:
            hypermea.tool.commands._service._add_addins({'add_validation': 'n/a'}, silent=True)

        if self.relation.child.external:
            ParentLinksInserter(self).transform(f'hooks/{self.relation.parent}.py')
        else:
            ChildLinksInserter(self).transform(f'hooks/{self.relation.child}.py')

        hypermea.tool.jump_back_to(starting_folder)
        return None

    def remove(self):
        try:
            starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
        except RuntimeError:
            return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

        if not self._link_already_exists():
            raise LinkManagerException(804, f'There is no link from {self.parent} to {self.children}')

        print(f'Removing link from {self.parent} to {self.children}')

        DomainRelationsRemover(self.relation).transform('domain/_relations.py')

        ## if not self.relation.child.external:
        ##     ParentReferenceRemover(self.parents).transform(f'domain/{self.children}.py')

        hypermea.tool.jump_back_to(starting_folder)


class LinkManagerException(Exception):
    def __init__(self, exit_code, message):
        super().__init__(message)
        self.exit_code = exit_code
