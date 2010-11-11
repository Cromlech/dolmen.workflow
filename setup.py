from setuptools import setup, find_packages

version = '0.1'

tests_require = [
    'zope.container',
    'zope.testing',
    'zope.traversing',
    'zope.site',
    ]

setup(name='dolmen.workflow',
      version=version,
      description="",
      long_description="",
      classifiers=[],
      keywords="",
      author="",
      author_email="",
      url="",
      license="",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      extras_require = {'test': tests_require},
      install_requires=[
          'dolmen.app.authentication',
          'dolmen.app.breadcrumbs',
          'dolmen.app.container',
          'dolmen.app.content',
          'dolmen.app.layout',
          'dolmen.app.site',
          'dolmen.file',
          'dolmen.forms.wizard',
          'dolmen.menu',
          'dolmen.security.policies',
          'dolmen.widget.file',
          'gp.fileupload',
          'grok',
          'grokcore.startup',
          'grokui.admin',
          'hurry.jquery',
          'hurry.resource',
          'megrok.resource',
          'menhir.skin.lightblue',
          'setuptools',
          'zeam.form.composed >= 1.2',
          'zeam.form.autofields',
          'zope.app.exception',
          'zope.app.form',
          'zope.browserresource',
          ],
      entry_points = """
      [console_scripts]
      """,
      )
