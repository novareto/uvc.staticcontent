# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from uvcsite.utils.shorties import getHomeFolderUrl
from uvcsite import PersonalPreferences, GlobalMenu, PersonalMenu
from uvc.homefolder.interfaces import IHomefolder
from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.component import getMultiAdapter
from megrok.pagetemplate import PageTemplate
from zope.pagetemplate.interfaces import IPageTemplate


grok.templatedir('templates')


class PersonalPanel(uvcsite.Page):
    """Page for Personal Properties
    """
    grok.name('personalpanelview')
    grok.order(35)
    grok.require('zope.View')
    grok.context(IHomefolder)

    grok.title(u"Meine Einstellungen")
    title = (u"Meine Einstellungen")
    description = (u"Hier werden Einstellungen zu"
                     " Ihrem Benutzerprofil vorgenommen.")

    
    def render(self):
        template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()


class PersonalPanelTemplate(PageTemplate):
    grok.view(PersonalPanel)


class PersonalPanelEntry(uvcsite.MenuItem):
    grok.require('zope.View')
    grok.order(35)

    grok.title(u"Meine Einstellungen")
    title = (u"Meine Einstellungen")
    grok.viewletmanager(uvcsite.IPersonalPreferences)
    
    @property
    def action(self):
        return str(getHomeFolderUrl(self.request)) + 'personalpanelview'


class UserName(uvcsite.MenuItem):
    grok.title("USERSNAME")
    grok.context(Interface)
    grok.viewletmanager(uvcsite.IPersonalPreferences)
    grok.order(10)
    grok.require('zope.View')

    @property
    def title(self):
        return self.request.principal.title


class MeinOrdner(uvcsite.MenuItem):
    grok.context(Interface)
    grok.name('Mein Ordner')
    grok.title('Mein Ordner')
    grok.viewletmanager(uvcsite.IPersonalPreferences)
    grok.order(20)
    grok.require('zope.View')

    @property
    def hfurl(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomefolder(principal, None)
        return homeFolder and absoluteURL(homeFolder, self.request) or ''

    @property
    def action(self):
        return self.hfurl


class Mitbenutzerverwaltung(uvcsite.MenuItem):
    grok.context(IHomefolder)
    grok.name('Mitbenutzerverwaltung')
    grok.title('Mitbenutzerverwaltung')
    grok.viewletmanager(uvcsite.IPersonalMenu)
    grok.order(30)
    grok.require('uvc.ManageCoUsers')

    @property
    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomefolder(principal)
        return str(absoluteURL(homeFolder, self.request)) + '/enms'

    @property
    def action(self):
        return self.url
