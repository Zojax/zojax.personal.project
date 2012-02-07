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
from zope.component import getUtility, queryUtility, \
    queryMultiAdapter, getMultiAdapter
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL

from zojax.catalog.interfaces import ICatalog
from zojax.content.space.utils import getSpace
from zojax.authentication.utils import getPrincipal
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.content.discussion.catalog import getCatalog

from zojax.content.textannotation.interfaces import ITextAnnotation


class BrowseMyProjects(object):

    items = None

    def update(self):
        catalog = queryUtility(ICatalog)

        if catalog is not None:
            # only open projects:
            state = 1
            results = catalog.searchResults(
                    traversablePath={'any_of': (getSite(),)},
                    sort_order='reverse', sort_on='modified',
                    type={'any_of': ('content.project', \
                                     'content.standaloneproject',)},
                    members={'any_of': (self.request.principal.id,)},
                    projectState={'any_of': (state,)},
                    isDraft={'any_of': (False,)},)

            if results:
                self.items = results


    def getTasks(self, project):
        """ returns active tasks for project """

        tasks = getUtility(ICatalog).searchResults(
            type={'any_of': ('project.task',),},
            projectTaskState = {'any_of': (1,)},
            searchContext = project, sort_on='projectTaskDate')[:3]

        if tasks:
            return tasks


    def getTaskCommits(self, task):
        """ returns comments for task """

        catalog = getCatalog()
        comments = catalog.search(contexts=(task,))[:3]

        if comments:
            result = []
            for item in comments:
                principal = getPrincipal(item.author)
                homeFolder = IPersonalSpace(principal, None)
                profileUrl = homeFolder is not None \
                        and '%s/profile/'%absoluteURL(homeFolder, self.request) or ''

                # limit text length
                text = getMultiAdapter((item, self.request), ITextAnnotation).getText(text=item.comment)

                info = {
                    'text': text,
                    'author': principal and principal.title or u'Unknown',
                    'author_url': profileUrl
                }
                result.append(info)

            return result


    def getProjectInfo(self, project):
        """ returns project info """

        context = project

        info = {
            'title': context.title,
            'description': context.description,
            'icon': queryMultiAdapter((context, self.request), name='zmi_icon'),
            'url': '%s/'%absoluteURL(context, self.request),
            'space': getSpace(context.__parent__),
            'tasks': self.getTasks(context)
            }

        return info
