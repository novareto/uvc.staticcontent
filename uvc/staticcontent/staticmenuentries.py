import grok
import uvcsite
import urllib
import uvcsite.browser.layout.menu
import uvcsite.browser.layout.slots.interfaces

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from uvcsite.interfaces import IHomeFolder
from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.component import getMultiAdapter
from megrok.pagetemplate import PageTemplate
from zope.pagetemplate.interfaces import IPageTemplate


grok.templatedir("templates")


class PersonalPanel(uvcsite.browser.Page):
    """Page for Personal Properties
    """

    grok.name("personalpanelview")
    grok.order(35)
    grok.require("zope.View")
    grok.context(IHomeFolder)

    grok.title(u"Meine Einstellungen")
    title = u"Meine Einstellungen"
    description = u"Hier werden Einstellungen zu" " Ihrem Benutzerprofil \
        vorgenommen."

    def render(self):
        template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()


class PersonalPanelTemplate(PageTemplate):
    grok.view(PersonalPanel)


class PersonalPanelEntry(uvcsite.browser.layout.menu.MenuItem):
    grok.adapts(Interface, IDefaultBrowserLayer, Interface,
                uvcsite.browser.layout.slots.interfaces.IPersonalPreferences)

    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        hf = IHomeFolder(principal, None)
        viewname = "personalpanelview"
        return urllib.parse.unquote(grok.util.url(self.request, hf, viewname))


class UserName:
    grok.title("USERSNAME")
    grok.context(Interface)
    grok.viewletmanager(uvcsite.browser.layout.slots.interfaces.IPersonalPreferences)
    grok.order(10)
    grok.require("zope.View")
    action=""

    @property
    def title(self):
        return self.request.principal.title


class MeinOrdner:

    @property
    def hfurl(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        hf = IHomeFolder(principal)
        return urllib.parse.unquote(grok.util.url(self.request, hf))

    @property
    def action(self):
        return self.hfurl


class Mitbenutzerverwaltung:

    @property
    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal)
        return str(absoluteURL(homeFolder, self.request)) + "/enms"

    @property
    def action(self):
        return self.url
