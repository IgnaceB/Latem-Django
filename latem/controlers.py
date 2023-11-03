from .serializers import *
from .models import *

class CRUD:
	def __init__(self):
		self.serializer=""
		self.table=""

	def create(self, data):
		serializer = self.serializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return 'ok'
		else :
			return 'fail'

	def delete (self, objectId):
		try :
			objectToDelete=self.table.objects.get(id=objectId)
		except objectToDelete.DoesNotExist:
			return 'fail'
		objectToDelete.delete()
		return 'ok'

	def update (self, objectId, data) :
		try :
			objectToUpdate = self.table.objects.get(id=objectId)
		except objectToUpdate.DoesNotExist:
			return 'fail'
		serializer = self.serializer(objectToUpdate, data=data)
		if serializer.is_valid():
			serializer.save()
			return 'ok'

	def readOne (self, objectId) :
		try : 
			objectToRead = self.table.objects.get(id=objectId)
		except objectToRead.DoesNotExist :
			return 'fail'
		objectReadable = self.serializer(objectToRead)
		return objectReadable

	def readAll(self) :
		objectsToRead = self.table.objects.all()
		objectsReadable = self.serializer(objectsToRead)
		return objectsReadable

class USERS(CRUD):
	def __init__(self):
		self.serializer=UserSerializer
		self.table=Users

class ITEMS(CRUD):
	def __init__(self):
		self.serializer=ItemsSerializer
		self.table=Items

class DESCRIPTION_ITEMS(CRUD):
	def __init__(self):
		self.serializer=DescriptionItemsSerializer
		self.table=DescriptionItems

class DEVIS(CRUD):
	def __init__(self):
		self.serializer=DevisSerializer
		self.table=Devis

class DEVIS_FILE(CRUD):
	def __init__(self):
		self.serializer=DevisFileSerializer
		self.table=DevisFile

class LIGNES_ITEMS_DEVIS(CRUD):
	def __init__(self):
		self.serializer=LignesItemsDevisSerializer
		self.table=LignesItemsDevis

class LIGNES_DESC_DEVIS(CRUD):
	def __init__(self):
		self.serializer=LignesDescDevisSerializer
		self.table=LignesDescDevis

