from django import template
from django.shortcuts import redirect
from django.template.loader import get_template
from django.templatetags.static import static
from django.utils.html import format_html

register = template.Library()

@register.tag
def navbar(parser, token):
	nodelist = parser.parse(('endnavbar'),)
	parser.delete_first_token()
	return NavbarNode(nodelist)

class NavbarNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		rendered = self.nodelist.render(context)
		output = get_template('navbar.html').render({
			'links': rendered,
		})
		return output


@register.tag
def navlink(parser, token):
	bits = token.split_contents()
	link = '/'
	classes = ''
	for bit in bits:
		if '=' in bit:
			attr, val = bit.split('=')
			if attr == 'href':
				link = val
			elif attr == 'class':
				classes += f' {val}'

	nodelist = parser.parse(('endnavlink'),)
	parser.delete_first_token()
	return NavLinkNode(nodelist, classes, link)

class NavLinkNode(template.Node):
	def __init__(self, nodelist, classes, link):
		self.nodelist = nodelist
		self.classes = classes
		self.link = link

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<li class="item {self.classes}"><a href={self.link}>{rendered}</a></li>')

@register.tag
def navlogo(parser, token):
	bits = token.split_contents()
	link = '/'
	for bit in bits:
		if '=' in bit:
			attr, val = bit.split('=')
			if attr == 'href':
				link = val.replace('"', '').replace("'", '')

	nodelist = parser.parse(("endnavlogo"),)
	parser.delete_first_token()
	return NavLogoNode(nodelist, link)

class NavLogoNode(template.Node):
	def __init__(self, nodelist, link):
		self.nodelist = nodelist
		self.link = link

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<li class="logo"><a href="{self.link}">{rendered}</a></li>')

@register.tag
def navbutton(parser, token):
	bits = token.split_contents()
	link = '/'
	secondary = False
	for bit in bits:
		if '=' in bit:
			attr, val = bit.split('=')
			if attr == 'href':
				link = val
		else:
			if bit == 'secondary':
				secondary = True

	nodelist = parser.parse(("endnavlogo"),)
	parser.delete_first_token()
	return NavButtonNode(nodelist, link, secondary=secondary)

class NavButtonNode(template.Node):
	def __init__(self, nodelist, link, /, secondary=False):
		self.nodelist = nodelist
		self.link = link
		self.is_secondary = secondary

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<li class="item button {"secondary" if self.is_secondary else ""}"><a href="{self.link}">{rendered}</a></li>')

@register.tag
def navuser(parser, token):
	bits = token.split_contents()
	icons = False
	for bit in bits:
		if bit == 'icons':
			icons = True

	return NavUserNode(icons)

class NavUserNode(template.Node):
	def __init__(self, icons=False):
		self.icons = icons

	def render(self, context):
		user = context['user']
		buttons = f'''
			<li class="item button"><a href=/components/user/login>{IconNode('sign-in-alt').render({}) if self.icons else ""}Log in</a></li>
			<li class="item button secondary"><a href=/components/user/signup>{IconNode('user-plus').render({}) if self.icons else ""}Sign up</a></li>
		'''
		if user.is_authenticated:
			buttons = f'''
				<li class="item button"><a href=/components/user/profile>{IconNode('user').render({}) if self.icons else ""}Profile</a></li>
				<li class="item button secondary"><a href=/components/user/logout>{IconNode('sign-out-alt').render({}) if self.icons else ""}Log out</a></li>
			'''
		return format_html(buttons)

@register.tag
def navadmin(parser, token):
	bits = token.split_contents()
	icons = False
	for bit in bits:
		if bit == 'icons':
			icons = True

	return NavAdminNode(icons)

class NavAdminNode(template.Node):
	def __init__(self, icons=False):
		self.icons = icons

	def render(self, context):
		user = context['user']
		if user.is_staff or user.is_superuser:
			return format_html(
				f'<li class="item button secondary"><a href="/admin">{IconNode("tools").render({}) if self.icons else ""}Admin</a></li>'
			)
		else:
			return ''



@register.tag
def footer(parser, token):
	nodelist = parser.parse(('endfooter'),)
	parser.delete_first_token()
	return FooterNode(nodelist)

@register.tag
class FooterNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		logo = ''
		social = ''
		rights = ''
		newsletter = False
		signup = ''
		for node in self.nodelist:
			node_type = node.__class__.__name__
			if node_type == FooterLogoNode.__name__:
				logo = node.render(context)
			elif node_type == FooterSocialNode.__name__:
				social = node.render(context)
			elif node_type == FooterRightsNode.__name__:
				rights = node.render(context)
			elif node_type == NewsletterSignupNode.__name__:
				newsletter = True
				signup = node.render(context)

		output = get_template('footer.html').render({
			'logo': logo,
			'social': social,
			'rights': rights,
			'newsletter': newsletter, 'signup': signup
		})
		return output


def footercomponent(parser, endtag):
	nodelist = parser.parse((endtag),)
	parser.delete_first_token()
	return nodelist

@register.tag
def footerlink(parser, token):
	bits = token.split_contents()
	link = '/'
	classes = ''
	for bit in bits:
		if '=' in bit:
			attr, val = bit.split('=')
			if attr == 'href':
				link = val
			elif attr == 'class':
				classes = val

	nodelist = footercomponent(parser, 'endfooterlink')
	return FooterLinkNode(nodelist, classes, link)

class FooterLinkNode(template.Node):
	def __init__(self, nodelist, classes, link):
		self.nodelist = nodelist
		self.classes = classes
		self.link = link

	def render(self, context):
		rendered = self.nodelist.render(context)
		return f'<li class="{self.classes}"><a href={self.link}>{rendered}</a></li>'

@register.tag
def footerlogo(parser, token):
	bits = token.split_contents()
	classes = ''
	for bit in bits:
		if '=' in bit:
			attr, val = bit.split('=')
			if attr == 'class':
				classes = val

	nodelist = footercomponent(parser, 'endfooterlogo')
	return FooterLogoNode(nodelist, classes)

class FooterLogoNode(template.Node):
	def __init__(self, nodelist, classes):
		self.nodelist = nodelist
		self.classes = classes

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<h1 class="logo {self.classes}">{rendered}</h1>')

@register.tag
def footersocial(parser, token):
	nodelist = footercomponent(parser, 'endfootersocial')
	return FooterSocialNode(nodelist)

class FooterSocialNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<div class="social-media">{rendered}</div>')

@register.tag
def footerrights(parser, token):
	nodelist = footercomponent(parser, 'endfooterrights')
	return FooterRightsNode(nodelist)

class FooterRightsNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<p class="rights-text">{rendered}</p>')



icon_prefixes = {
	'facebook-f': 'fab',
	'twitter': 'fab',
	'instagram': 'fab',
	'youtube': 'fab',
	'linkedin-in': 'fab',

	'bars': 'fas',
	'times': 'fas',
	'tools': 'fas',

	'user': 'fas',
	'user-plus': 'fas',
	'sign-in-alt': 'fas',
	'sign-out-alt': 'fas',
}

@register.tag
def icon(parser, token):
	_, icon_name = token.split_contents()
	return IconNode(icon_name)

class IconNode(template.Node):
	def __init__(self, icon_name):
		self.icon_name = icon_name
		self.prefix = icon_prefixes[icon_name] if icon_name in icon_prefixes else ''

	def render(self, context):
		registerAPI('https://kit.fontawesome.com/791417c75e.js')
		return format_html(f'<i class="{self.prefix} fa-{self.icon_name}"></i>')



apis_to_load = []
scripts_to_load = []

class API():
	def __init__(self, api, *options):
		self.api = api
		self.same_site = ''
		self.secure = False

		for option in options:
			if '=' in option:
				attr, val = option.split('=')
				if attr == 'SameSite':
					self.same_site = val
			else:
				if option == 'Secure':
					self.secure = True

@register.simple_tag
def registerAPI(api, *options):
	for api_to_load in apis_to_load:
		if api == api_to_load.api:
			return ''
	apis_to_load.append(API(api, options))
	return ''

@register.simple_tag
def registerScript(script):
	if script not in scripts_to_load:
		scripts_to_load.append(script)
	return ''

@register.simple_tag
def loadAPIs():
	apis = ''
	for api in apis_to_load:
		security = ''
		if api.secure:
			security = 'Secure'
		apis += f'<script src="{api.api}" {security} SameSite={api.same_site}></script>'

	for api in scripts_to_load:
		apis += f'<script src="{static(api)}"></script> '

	return format_html(f'''
	<div class="apis">
		{apis}
	</div>
	''')



@register.simple_tag
def facebook(href):
	ico = IconNode('facebook-f').render({})
	return format_html(f'<a href="{href}">{ico}</a>')

@register.simple_tag
def twitter(href):
	ico = IconNode('twitter').render({})
	return format_html(f'<a href="{href}">{ico}</a>')

@register.simple_tag
def instagram(href):
	ico = IconNode('instagram').render({})
	return format_html(f'<a href="{href}">{ico}</a>')

@register.simple_tag
def youtube(href):
	ico = IconNode('youtube').render({})
	return format_html(f'<a href="{href}">{ico}</a>')

@register.simple_tag
def linkedin(href):
	ico = IconNode('linkedin-in').render({})
	return format_html(f'<a href="{href}">{ico}</a>')

@register.simple_tag
def SVG(src, *args, **kwargs):
	isStatic = to_bool(unpack_kwargs(kwargs, 'static', False))
	width    = float(unpack_kwargs(kwargs, 'width', 0))
	height   = float(unpack_kwargs(kwargs, 'height', 0))

	if isStatic:
		from django.conf import settings
		from os.path import join
		src = join(settings.BASE_DIR, src)
	
	with open(src, 'r') as f:
		data = f.read()

	w = 0
	h = 0

	for line in data.split('\n')[1:]:
		if '=' in line:
			attr, val = line.split('=')
			attr = attr.strip()
			val = val.strip()

			if attr == 'width':
				w = float(val.replace('"', '').replace("'", ''))
			elif attr == 'height':
				h = float(val.replace('"', '').replace("'", ''))

	view_box = f'viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet"'
	if width > 0:
		width = f'{width}px'
	else:
		width = 'auto'
	if height > 0:
		height = f'{height}px'
	else:
		height = 'auto'
	style = f'style="width:{width};height:{height};padding-left:15px;"'

	_, svg = data.split('<svg')
	svg = f'<svg {style} {view_box}\n{svg}'
	return format_html(svg)

def unpack_kwargs(kwargs, idx, default=None):
	return kwargs[idx] if idx in kwargs.keys() else default

def to_bool(b):
	if type(b) == str:
		return b.lower() == 'true'
	elif type(b) in (int, float):
		return b != 0
	elif type(b) == bool:
		return b
	return False


@register.tag
def newslettersignup(parser, token):
	nodelist = parser.parse(('endnewslettersignup',))
	parser.delete_first_token()
	return NewsletterSignupNode(nodelist)

class NewsletterSignupNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		title = ''
		desc = ''
		for node in self.nodelist:
			node_type = node.__class__.__name__
			if node_type == NewsletterTitleNode.__name__:
				title = node.render(context)
			elif node_type == NewsletterDescNode.__name__:
				desc = node.render(context)
		return format_html(f'''
			{title}
			<div class="border"></div>
			{desc}
			<form action="/newsletter/signup" method="POST" class="newsletter-form">
				<input type="email" name="email" id="email" class="txtb" placeholder="Enter your email">
				<input type="submit" value="Sign up" class="btn">
			</form>
		''')

@register.tag
def newslettertitle(parser, token):
	nodelist = parser.parse(('endnewslettertitle',))
	parser.delete_first_token()
	return NewsletterTitleNode(nodelist)

class NewsletterTitleNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<h1>{rendered}</h1>')

@register.tag
def newsletterdesc(parser, token):
	nodelist = parser.parse(('endnewsletterdesc',))
	parser.delete_first_token()
	return NewsletterDescNode(nodelist)

class NewsletterDescNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<p>{rendered}</p>')



@register.tag
def productcard(parser, token):
	nodelist = parser.parse(('endproductcard',))
	parser.delete_first_token()
	return ProductCardNode(nodelist)

class ProductCardNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		header = ''
		varients = ''
		footer = ''
		for node in self.nodelist:
			node_type = node.__class__.__name__
			if node_type in (ProductNameNode.__name__, ProductDescNode.__name__):
				header += node.render(context)
			elif node_type in (ProductVarientsNode,):
				varients += node.render(context)
			# elif node_type in ():

		return format_html(f'''
			<div class="product-card">
				{header}
				<div class="product-img"></div>
				<div class="product-varients">'''
					# <span class="blue active" data-color='#7ed6df' data-img='url(static "main/1.png")'></span>
					# <span class="green"       data-color='#badc58' data-img='url(static "main/2.png")'></span>
					# <span class="rose"        data-color='#ff7979' data-img='url(static "main/4.png")'></span>
					# <span class="yellow"      data-color='#f9ca24' data-img='url(static "main/3.png")'></span>
				+f'''
					{varients}
				</div>
				<div class="product-info">'''
					# footer
					# <div class="product-price">£90</div>
				+f'''
					{footer}
					<a href="#" class="product-button">Add to Cart</a>
				</div>
			</div>
		''')


@register.simple_tag
def productobj(obj):
	return ''


@register.tag
def productname(parser, token):
	_, name = token.split_contents()
	name = name.replace('"', '').replace("'", '')
	return ProductNameNode(name)

class ProductNameNode(template.Node):
	def __init__(self, name):
		self.name = name

	def render(self, context):
		return format_html(f'<h1>{self.name}</h1>')

@register.tag
def productdesc(parser, token):
	nodelist = parser.parse(('endproductdesc,'))
	parser.delete_first_token()
	return ProductDescNode(nodelist)

class ProductDescNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<p>{rendered}</p>')

@register.tag
def productvarients(parser, token):
	nodelist = parser.parse(('endproductvarients',))
	parser.delete_first_token()
	return ProductVarientsNode(nodelist)

class ProductVarientsNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		rendered = self.nodelist.render(context)
		return format_html(f'<div class="product-varients>{rendered}</div>')

@register.simple_tag
def productvarient(color, img):
	return format_html(f'<span class="green" data-color="{color}" data-img="url({static(img)}"></span>')

# <div class="product-card">
# 	<h1>Product 1</h1>
# 	<p>Lorem ipsum dolor sit amet.</p>
# 	<div class="product-img"></div>
# 	<div class="product-varients">
# 		<span class="blue active" data-color='#7ed6df' data-img='url({% static "main/1.png" %})'></span>
# 		<span class="green"       data-color='#badc58' data-img='url({% static "main/2.png" %})'></span>
# 		<span class="rose"        data-color='#ff7979' data-img='url({% static "main/4.png" %})'></span>
# 		<span class="yellow"      data-color='#f9ca24' data-img='url({% static "main/3.png" %})'></span>
# 	</div>
# 	<div class="product-info">
# 		<div class="product-price">£90</div>
# 		<a href="#" class="product-button">Add to Cart</a>
# 	</div>
# </div>

# {% productcard %}
# 	{% productname "Product 1" %}
# 	{% productdesc %} Lorem ipsum dolor sit amet. {% endproductdesc %}

# 	{% productvarients %}
# 		{% productvarient color="#7ed6df" img="url({% static "main/1.png" %})" %}
# 		{% productvarient color="#badc58" img="url({% static "main/2.png" %})" %}
# 		{% productvarient color="#ff7979" img="url({% static "main/3.png" %})" %}
# 		{% productvarient color="#f9ca24" img="url({% static "main/4.png" %})" %}
# 	{% endproductvarients %}

# 	{% productprice "90" "£" %}
# {% endproductcard %}
