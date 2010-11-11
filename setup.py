from setuptools import setup, find_packages

version = '0.1'

tests_require = [
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
          'setuptools',
          'zeam.form.base',
          'zope.interface',
          'zope.schema',
          'zope.component',
          ],
      entry_points = """
      [console_scripts]
      """,
      )
