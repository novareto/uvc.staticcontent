# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import uvclight
from cromlech.browser import ITemplate, IURL
from cromlech.security.interfaces import IUnauthenticatedPrincipal
from uvc.homefolder.components import HomefolderURL
from uvc.homefolder.interfaces import IHomefolder
from uvc.design.canvas import IPersonalPreferences, IGlobalMenu, IPersonalMenu
from zope.component import getMultiAdapter
from zope.interface import Interface


class PersonalPanel(uvclight.Page):
    """Page for Personal Properties
    """
    uvclight.auth.require('zope.View')
    uvclight.context(IHomefolder)
    uvclight.name('personalpanelview')
    uvclight.order(35)
    uvclight.title(u"Meine Einstellungen")

    title = (u"Meine Einstellungen")
    description = (u"Hier werden Einstellungen zu"
                     " Ihrem Benutzerprofil vorgenommen.")

    def render(self):
        template = getMultiAdapter((self, self.request), ITemplate)
        return template()


@uvclight.adapter(PersonalPanel, Interface)
@uvclight.implementer(ITemplate)
def personalpanel_menu(context, request):
    return uvclight.get_template('personalpaneltemplate.pt', __file__)


class PersonalPanelEntry(uvclight.MenuItem):
    uvclight.auth.require('zope.View')
    uvclight.order(35)
    uvclight.title(u"Meine Einstellungen")
    uvclight.menu(IPersonalPreferences)

    title = (u"Meine Einstellungen")

    @property
    def action(self):
        url = str(getMultiAdapter(
            (self.request.principal, self.request), IURL, name="homefolder"))
        return url + 'personalpanelview'


class UserName(uvclight.MenuItem):
    uvclight.auth.require('zope.View')
    uvclight.context(Interface)
    uvclight.order(10)
    uvclight.title("USERSNAME")
    uvclight.menu(IPersonalPreferences)

    @property
    def title(self):
        return self.request.principal.title


class MeinOrdner(uvclight.MenuItem):
    uvclight.auth.require('zope.View')
    uvclight.context(Interface)
    uvclight.name('Mein Ordner')
    uvclight.order(20)
    uvclight.title('Mein Ordner')
    uvclight.menu(IPersonalPreferences)

    @property
    def hfurl(self):
        url = str(getMultiAdapter(
            (self.request.principal, self.request), IURL, name="homefolder"))
        return url

    @property
    def action(self):
        return self.hfurl


class Mitbenutzerverwaltung(uvclight.MenuItem):
    uvclight.context(IHomefolder)
    uvclight.name('Mitbenutzerverwaltung')
    uvclight.title('Mitbenutzerverwaltung')
    uvclight.menu(IPersonalMenu)
    uvclight.order(30)
    uvclight.auth.require('uvc.ManageCoUsers')

    @property
    def url(self):
        url = str(getMultiAdapter(
            (self.request.principal, self.request), IURL, name="homefolder"))
        return url + '/enms'
 
    @property
    def action(self):
        return self.url
