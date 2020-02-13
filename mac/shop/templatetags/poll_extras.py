from django.test import TestCase
import datetime
from django import template
from django.template import Template
# Create your tests here.
# Register our own template tag
register = template.Library()	
@register.filter()
def addDays(days):
   newDate = datetime.date.today() + datetime.timedelta(days=days)
   return newDate
# @register.simple_tag(takes_context=True)
# def productRating(b):
	# startHtml = '<h1>Hello World</h1>'
	# return Template(startHtml).render(b)
@register.filter()
def to_int(value):
	return int(value)	