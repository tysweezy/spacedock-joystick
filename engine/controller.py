class Controller(object):
	def __init__(self, type = 'joystick'):
		# default to joystick
		self.type = type

	def render(self):
		""" 
		Renders controller type.
		"""
		if self.type == 'joystick':
			print('render joystick')
		elif self.type == 'keyboard_movement':
			print('asdf control')
		else:
			raise Exception('No control set.')