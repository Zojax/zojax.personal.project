##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, component
from zojax.catalog.utils import getRequest
from zojax.content.type.container import ContentContainer
from zojax.content.space.workspace import WorkspaceFactory
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.personal.space.interfaces import IPersonalWorkspaceDescription

from interfaces import _, IMyTasks, IMyTasksFactory, IMyProjects, IMyProjectsFactory


class MyTasks(ContentContainer):
    interface.implements(IMyTasks)

    title = _('My tasks')
    __name__ = u'mytasks'


class MyTasksFactory(WorkspaceFactory):
    component.adapts(IPersonalSpace)
    interface.implements(IMyTasksFactory)

    name = 'mytasks'
    title = _(u'My tasks')
    description = u''
    weight = 9
    factory = MyTasks

    def isAvailable(self):
        request = getRequest()
        if request.principal.id != self.space.principalId:
            return False

        return True


class MyTasksDescription(object):
    interface.implements(IPersonalWorkspaceDescription)

    name = 'mytasks'
    title = _(u'My tasks')
    description = u''

    def createTemp(self, context):
        ws = MyTasks()
        ws.__parent__ = context
        return ws


class MyProjects(ContentContainer):
    interface.implements(IMyProjects)

    title = _('My projects')
    __name__ = u'myprojects'


class MyProjectsDescription(object):
    interface.implements(IPersonalWorkspaceDescription)

    name = 'myprojects'
    title = _(u'My projects')
    description = u''

    def createTemp(self, context):
        ws = MyProjects()
        ws.__parent__ = context
        return ws


class MyProjectsFactory(WorkspaceFactory):
    component.adapts(IPersonalSpace)
    interface.implements(IMyProjectsFactory)

    name = 'myprojects'
    title = _(u'My projects')
    description = u''
    weight = 10
    factory = MyProjects

    def isAvailable(self):
        request = getRequest()
        if request.principal.id != self.space.principalId:
            return False

        return True
