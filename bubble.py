import random
import re

from respond import respond

def white(body, say, args):
    bubble('white', body, say, args)

def yellow(body, say, args):
    bubble('yellow', body, say, args)

def alternate(body, say, args):
    bubble('alternate', body, say, args)

def rand(body, say, args):
    bubble('random', body, say, args)

def bubble(directive, body, say, args):
    colors = ['white', 'yellow']
    color_index = 0

    if directive == 'white':
      color = 'white'
    elif directive == 'yellow':
      color = 'yellow'
    else:
      color = colors[0]

    out = ""

    mapping = {
      '#': 'hash',
      '?': 'question',
      '!': 'exclamation',
    }

    for character in " ".join(args):
      if directive == 'alternate':
        color = colors[color_index]
      elif directive == 'random':
        color = random.choice(colors)

      if re.match(r"[a-zA-Z]", character):
        out += f':alphabet-{color}-{character}:'
      elif character in mapping.keys():
        out += f':alphabet-{color}-{mapping[character]}:'
      elif character == ' ':
        out += ':spacer:'
      else:
        out += character

      color_index = (color_index + 1) % len(colors)

    respond(say, body, out)
