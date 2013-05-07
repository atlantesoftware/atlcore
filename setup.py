from distutils.core import setup

setup(
    name='atlcore',
    version='1.5',
    packages=['atlcore', 'atlcore.cms', 'atlcore.cms.admin', 'atlcore.cms.templatetags', 'atlcore.doc', 'atlcore.vcl',
              'atlcore.vcl.components', 'atlcore.vcl.templatetags', 'atlcore.vcl.dataproviders',
              'atlcore.vcl.dataproviders.jqgrid', 'atlcore.vcl.dataproviders.jstree', 'atlcore.apps',
              'atlcore.apps.atlgallery', 'atlcore.apps.atlgallery.migrations', 'atlcore.libs', 'atlcore.libs.stdimage',
              'atlcore.libs.clipboard', 'atlcore.site', 'atlcore.site.templatetags', 'atlcore.skin',
              'atlcore.skin.tools', 'atlcore.skin.migrations', 'atlcore.utils', 'atlcore.aspect',
              'atlcore.aspect.migrations', 'atlcore.plugins', 'atlcore.plugins.news', 'atlcore.plugins.document',
              'atlcore.plugins.news_box', 'atlcore.plugins.news_box.migrations', 'atlcore.plugins.atlplugin_jwplayer',
              'atlcore.plugins.atlplugin_jwplayer.migrations', 'atlcore.plugins.atlplugin_html5video',
              'atlcore.plugins.atlsocialnetworklinks', 'atlcore.schedule', 'atlcore.schedule.conf',
              'atlcore.schedule.feeds', 'atlcore.schedule.migrations', 'atlcore.schedule.templatetags',
              'atlcore.relations', 'atlcore.relations.migrations', 'atlcore.workflows', 'atlcore.workflows.migrations',
              'atlcore.contenttype', 'atlcore.contenttype.admin', 'atlcore.contenttype.models',
              'atlcore.contenttype.models.signals', 'atlcore.contenttype.migrations',
              'atlcore.contenttype.translations', 'atlcore.permissions', 'atlcore.permissions.management',
              'atlcore.permissions.management.commands', 'atlcore.permissions.migrations',
              'atlcore.permissions.templatetags', 'atlcore.siteprofile', 'atlcore.siteprofile.migrations',
              'atlcore.tinymce_old', 'atlcore.tinymce_old.templatetags', 'atlcore.configvalues',
              'atlcore.configvalues.migrations', 'atlcore.nomenclature', 'atlcore.nomenclature.migrations',
              'atlcore.usersprofile', 'atlcore.usersprofile.migrations', 'atlcore.mailresponder',
              'atlcore.modeltranslation', 'atlcore.modeltranslation.management',
              'atlcore.modeltranslation.management.commands'],
    url='http://www.atlantesoftware.com',
    license='BSD License',
    author='hailem',
    author_email='hailem@atlantesoftware.com',
    description='Atlantesoftware CMS Core'
)
