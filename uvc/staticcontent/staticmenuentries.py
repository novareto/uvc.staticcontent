# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite
import urllib

from uvcsite.utils.shorties import getHomeFolderUrl
from uvcsite import PersonalPreferences, GlobalMenu, PersonalMenu
from uvcsite.homefolder.interfaces import IHomeFolder
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
    grok.context(IHomeFolder)

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
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        hf = IHomeFolder(principal).homeFolder
        viewname = 'personalpanelview'
        return urllib.unquote(grok.util.url(self.request, hf, viewname))


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
        hf = IHomeFolder(principal).homeFolder
        return urllib.unquote(grok.util.url(self.request, hf))

    @property
    def action(self):
        return self.hfurl


class Mitbenutzerverwaltung(uvcsite.MenuItem):
    grok.context(IHomeFolder)
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
        homeFolder = IHomeFolder(principal).homeFolder
        return str(absoluteURL(homeFolder, self.request)) + '/enms'

    @property
    def action(self):
        return self.url
