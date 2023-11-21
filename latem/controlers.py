from .serializers import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from more_itertools import unique_everseen

class CRUD:
	def __init__(self):
		self.serializer=""
		self.table=""

	def create(self, data):

		serializer = self.serializer(data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return 'ok'
		else :
			print(serializer.errors)

	def delete (self, objectId):
		
		try :
			objectToDelete=self.table.objects.get(id=objectId)
			objectToDelete.delete()
		except Exception as error:
			raise error
	
		return 'ok'

	def update (self, objectId, data) :
		
		try :
			objectToUpdate = self.table.objects.get(id=objectId)
		
		except objectToUpdate.DoesNotExist:
			return 'fail'
		serializer = self.serializer(objectToUpdate, data=data, partial=True)
		if serializer.is_valid():
		
			serializer.save()
			return 'ok'
		else : 
			# raise serializer.errors
			print(serializer.errors)

	def readOne (self, objectId) :
		try : 
			objectToRead = self.table.objects.get(id=objectId)
		except objectToRead.DoesNotExist :
			return 'fail'
		objectReadable = self.serializer(objectToRead)
		return objectReadable.data

	def readAll(self) :
		objectsToRead = self.table.objects.all()
		objectsReadable = self.serializer(objectsToRead, many=True)
		return objectsReadable.data

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
	def getAllOrderedByLevel(self):
		objectsToRead = self.table.objects.all().order_by('level')
		objectsReadable = self.serializer(objectsToRead, many=True)
		return objectsReadable.data
	def getMaxLevel(self):
		objectsToRead = self.table.objects.all().order_by('-level').first()
		objectsReadable = self.serializer(objectsToRead)
		return objectsReadable.data['level']

class DEVIS(CRUD):
	def __init__(self):
		self.serializer=DevisSerializer
		self.table=Devis
	def getNewDevis(self):
		self.serializer=DevisClientSerializer
		try : 
			objectsToRead = self.table.objects.filter(Q(responsableId__isnull=True) & ~Q(status='clôturé')).select_related('clientId')
		except self.table.DoesNotExist:
			return ''
		objectsReadable = self.serializer(objectsToRead, many=True)
		return objectsReadable.data
	def getMyDevis(self, id):
		self.serializer=DevisClientSerializer
		try : 
			objectsToRead = self.table.objects.filter(Q(responsableId=id) & ~Q(status='clôturé')).select_related('clientId')
		except self.table.DoesNotExist:
			return ''
		objectsReadable = self.serializer(objectsToRead, many=True)
		return objectsReadable.data
	def getMyCustomerDevis(self, id):

		try : 
			objectsToRead = self.table.objects.filter(clientId=id)
		except self.table.DoesNotExist:
			return ''
		objectsReadable = self.serializer(objectsToRead, many=True)
		return objectsReadable.data

	def getOtherDevis(self, id):
		self.serializer=DevisClientSerializer
		try : 
			objectsToRead = self.table.objects.filter(~Q(responsableId=id) & ~Q(status='clôturé')& ~Q(responsableId__isnull=True)).select_related('clientId')
		except self.table.DoesNotExist:
			return ''
		objectsReadable = self.serializer(objectsToRead, many=True)
		return objectsReadable.data

	def getArchivedDevis(self):
		self.serializer=DevisClientSerializer
		try : 
			objectsToRead = self.table.objects.filter(status='clôturé').select_related('clientId')
		except self.table.DoesNotExist:
			return ''
		objectsReadable = self.serializer(objectsToRead, many=True)
		return objectsReadable.data

	def initDevis(self, id):
		try : 
			devis = self.table.objects.get(id=id)
			lignesItems = LignesItemsDevis.objects.filter(devisId=devis)
			items = [ligne.itemId for ligne in lignesItems]
			client = devis.clientId
			lignesDescription = [LignesDescDevis.objects.filter(LignesItemsDevisId=ligne) for ligne in lignesItems]
			listLignesDescription = [item for queryset in lignesDescription for item in queryset]
			description = [ligne.descriptionItems for ligne in listLignesDescription]
			file = DevisFile.objects.filter(devisId=devis)

			dataset = {
			'devis' : self.serializer(devis).data,
			'lignesItems' : LignesItemsDevisSerializer(lignesItems, many=True).data,
			'items' : list(unique_everseen(ItemsSerializer(ligne).data for ligne in items)),
			'client' : UserSerializer(client).data,
			'lignesDescription' : [LignesDescDevisSerializer(ligne, many=True).data for ligne in lignesDescription],
			'description' : list(unique_everseen(DescriptionItemsSerializer(ligne).data for ligne in description)),
			'files' : DevisFileSerializer(file, many=True).data,
			 }

			return dataset
		except Exception as error : 
			raise error


class DEVIS_FILE(CRUD):
	def __init__(self):
		self.serializer=DevisFileSerializer
		self.table=DevisFile

class LIGNES_ITEMS_DEVIS(CRUD):
	def __init__(self):
		self.serializer=LignesItemsDevisSerializer
		self.table=LignesItemsDevis
	def getAllItemsOfOneDevis(self,devis_id) :
		try :
			objectsToRead = self.table.objects.filter(devisId=devis_id)

		except objectsToRead.DoesNotExist:
			raise error
		objectsReadable = self.serializer(objectsToRead, many=True)
		return objectsReadable.data

class LIGNES_DESC_DEVIS(CRUD):
	def __init__(self):
		self.serializer=LignesDescDevisSerializer
		self.table=LignesDescDevis

