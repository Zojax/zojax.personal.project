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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zojax.portlet.interfaces import _ as pMsg
from zojax.portlet.interfaces import IPortletManagerConfiguration
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory

_ = MessageFactory('zojax.personal.project')


class IMyTasks(IWorkspace):
    """ my tasks workspace """


class IMyTasksFactory(IWorkspaceFactory):
    """ factory """


class ILeftPortletManager(IPortletManagerConfiguration):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = (),
        required = True)


class IRightPortletManager(IPortletManagerConfiguration):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = ('portlet.actions',),
        required = True)
