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
from zope import component, interface
from zope.location import LocationProxy
from zope.component import getUtility, queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.app.intid.interfaces import IIntIds
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.security.interfaces import IUnauthenticatedPrincipal

from zojax.catalog.interfaces import ICatalog
from zojax.project.interfaces import ITask, IMilestone
from zojax.project.browser.tasks import Tasks, TitleColumn
from zojax.assignment.interfaces import IAssignments
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.personal.project.interfaces import _, IMyTasks


class MyTasks(Tasks):
    component.adapts(IMyTasks, interface.Interface, interface.Interface)

    pageSize = 30
    cssClass = 'z-table project-tasks-table'
    enabledColumns = ('id', 'title', 'milestone', 'severity', 'status', 'date')
    msgEmptyTable = _('There are no active tasks.')

    def initDataset(self):
        self.dataset = getUtility(ICatalog).searchResults(
            type = {'any_of': ('project.task',),},
            assignments = {'any_of': (self.context.__parent__.principalId,)},
            projectTaskState = {'any_of': (1,)},
            sort_on = 'projectTaskDate')


class TitleColumn(TitleColumn):
    component.adapts(interface.Interface, interface.Interface, MyTasks)

    def update(self):
        self.ids = getUtility(IIntIds)

    def render(self):
        return u'<a href="%s/">%s</a>'%(
            self.ids.getId(self.content), self.query())


class MyTasksPublisher(object):
    interface.implements(IBrowserPublisher)
    component.adapts(IMyTasks, interface.Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        context = self.context

        view = queryMultiAdapter((context, request), name=name)
        if view is not None:
            return view

        if not IUnauthenticatedPrincipal.providedBy(request.principal):
            try:
                taskId = int(name)
            except:
                taskId = None

            if taskId:
                task = getUtility(IIntIds).queryObject(taskId)
                if task is not None:
                    space = context.__parent__
                    if space.principalId != request.principal.id:
                        space = IPersonalSpace(request.principal, None)
                        if space is None:
                            raise NotFound(context, name, request)
                        else:
                            request.response.redirect(
                                '%s/mytasks/%s/'%(
                                    absoluteURL(space, request), name))

                    return LocationProxy(task, context, name)

        if name in context:
            return context[name]

        raise NotFound(context, name, request)

    def browserDefault(self, request):
        return self.context, ('index.html',)
