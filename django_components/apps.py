from django.apps import AppConfig
from django.conf import settings

from os import system, walk
from os.path import join

from .compilers import sass


class Printer:
	def __init__(self):
		self.tabs = 0

	def fprint(self, *args, **kwargs):
		t = ''
		for _ in range(self.tabs):
			t += '    '
		print(f'{t}{args[0]}', *args[1:], **kwargs)

	def indent(self):
		self.tabs += 1

	def dedent(self):
		if self.tabs > 0:
			self.tabs -= 1


class ComponentConfig(AppConfig):
	name = 'components'
	printer = Printer()

	def ready(self):
		self.printer.fprint('\nInitialising app: main')
		self.printer.indent()
		
		self.compile_static()

		self.printer.dedent()
		self.printer.fprint('Initialised app: main\n')

	def compile_static(self):
		for root, _, files in walk(settings.BASE_DIR):
			for fname in files:
				_, *ext = fname.split('.')
				if type(ext) == list:
					ext = ext[-1]
				if ext in ('scss',):
					self.compile_css(join(root, fname))

	def compile_css(self, fname):
		self.printer.fprint(f'Compiling (SCSS): {fname}')
		fname, ext = fname.split('.')
		with open(fname + '.' + ext, 'r') as f:
			data = f.read()
		data = data.replace('\t', '')
		c = sass.Compiler(data)
		with open(fname + '.min.css', 'w') as f:
			f.write(c.compile())
		self.printer.fprint(f'Compiled successfully (SCSS): {fname}')
