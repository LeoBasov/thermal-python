import unittest
import sys

sys.path.append('../../.')

from thermal import domain

class DomainTest(unittest.TestCase):
	def test_init(self):
		block = domain.Block(0, (0,0), (1,1), conductivity = 1, density = 1, heat_capacity = 1)
		connection = domain.Connection(0, 1)
		side = domain.Side(0, domain.Type.CONNECTION)
