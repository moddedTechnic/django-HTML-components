from distutils.core import setup

setup(
	name='django_HTML_components',
	packages=['django_HTML_components'],
	version='0.1',
	license='GNU GPL 3.0',
	description='Adds several commonly used components for Django, such as a styled header and footer.',
	author='Jonathan Leeming',
	author_email='jpleeming51@gmail.com',
	url='https://github.com/moddedTechnic/django-HTML-components',
	download_url='https://github.com/moddedTechnic/django-HTML-components/archive/v0.1.3-alpha.tar.gz',
	keywords=['django', 'HTML', 'components'],
	install_requires=[
		'django',
	],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Framework :: Django :: 3.0',
		'Topic :: Software Development',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
	],
)
