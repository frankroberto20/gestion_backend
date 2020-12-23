from django.test import TestCase

from .models import *

# Create your tests here.

class MedicalAssistantTest(TestCase):

    def setUp(self):

        #Create patients
        p1 = Paciente()