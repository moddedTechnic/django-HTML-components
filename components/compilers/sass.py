
class Compiler:
	def __init__(self, code):
		if type(code) == str:
			self.code = code.split('\n')
		else:
			self.code = code
		self.idx = 0

	def remaining_tokens(self):
		return self.idx < len(self.code) - 1

	def get_block(self):
		start = self.idx
		bracket_count = 1
		while bracket_count > 0 and self.remaining_tokens():
			line = self.code[self.idx]
			self.idx += 1
			bracket_count += line.count('{')
			bracket_count -= line.count('}')
		end = self.idx
		return self.code[start:end]

	def parse(self):
		commands = []
		
		while self.remaining_tokens():
			line = self.code[self.idx]
			self.idx += 1
			if '{' in line:
				selector = (line.split('{', 1)[0]).strip()
				block = self.get_block()
				c = Compiler(block)
				if '@' in line:
					commands.append(MediaQuery(selector, c.parse()))
				else:
					commands.append(RuleSet(selector, c.parse()))
			elif ':' in line:
				prop, val = line.split(':')
				prop = prop.strip()
				val = val.strip()
				rule = Rule(prop, val)
				commands.append(rule)
			elif line == '':
				continue

		return commands

	def compile(self):
		out = ''
		for cmd in self.parse():
			out += cmd.evaluate()

		lines = out.split('\n')
		out = ''

		for line in lines:
			if '{}' not in line:
				out += line + '\n'

		return out + '}'


class Command:
	def __init__(self, name, arg=None):
		self.name = name
		self.arg = arg
		self.commands = []

	def __str__(self):
		cmds = ''
		for cmd in self.commands:
			cmds += f'\n\t{cmd}'
		return f'{self.name} {f"({self.arg})" if self.arg is not None else ""} {":" if cmds != "" else ""} {cmds}'

class RuleSet:
	def __init__(self, selector, rules):
		self.selector = selector
		self.rules = rules

	def __str__(self):
		rule_string = ''
		for rule in self.rules:
			rule_string += f'{rule}\n'
		return f'{self.selector}{{{rule_string}}}'

	def evaluate(self, selector=''):
		if selector == '':
			selector = self.selector
		elif self.selector[0] == '&':
			selector = self.selector.replace('&', selector)
		else:
			selector += ' ' + self.selector
		res = ''
		rule_string = ''
		for rule in self.rules:
			if type(rule) == RuleSet:
				res += rule.evaluate(selector)
			else:
				rule_string += str(rule) + '\n'
		res += f'\n{selector}{{{rule_string}}}'
		return res

class MediaQuery(RuleSet):
	def evaluate(self, selector=''):
		res = ''
		for rule in self.rules:
			res += rule.evaluate()
		return f'{self.selector}{{{res}}}'

class Rule:
	def __init__(self, prop, val):
		self.prop = prop
		self.val  = val

	def __str__(self):
		return f'{self.prop}:{self.val}'
