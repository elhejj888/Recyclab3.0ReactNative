from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse

from Materials.models import Material, Transaction, Confirmation
from django.db import transaction

# Create your views here.
def index(request):
    return render(request, 'index.html')

def addMaterial(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        etat = request.POST.get('etat')
        unitPrice =float(request.POST.get('unitPrice'))
        quantity = int(request.POST.get('quantity'))
        material = Material.objects.create(name=name, description=description, etat=etat, unitPrice=unitPrice)
        material.save()
        return JsonResponse({'success': True, 'material_id': material.id})
    else:
        return JsonResponse({'success': False, 'errors': 'errors occured'}, status=400)

def updateMaterial(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        material.name = request.POST.get('name')
        material.description = request.POST.get('description')
        material.etat = request.POST.get('etat')
        material.quantity = int(request.POST.get('quantity'))
        material.unitPrice =float(request.POST.get('unitPrice'))
        material.save()
        return JsonResponse({'success': True, 'material_id': material.id})
    else:
        # Render the form with the current material data
        return JsonResponse({'success': False, 'errors': 'errors occurred'}, status=400)

def deleteMaterial(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        material.delete()
        return JsonResponse({'success': True, 'material_id': material.id})
    else:
        # Render the confirmation page
        return JsonResponse({'success': False, 'errors': 'errors occurred'}, status=400)
    
def getMaterials(request):
    # Retrieve all materials from the database
    materials = Material.objects.all()
    # Convert materials to JSON format
    data = [{'id': material.id,
            'name': material.name,
            'description': material.description,
            'etat': material.etat,
            'quantity': material.quantity,
            'unitPrice': material.unitPrice,
            'created_at': material.created_at,
            } for material in materials]
    # Return the JSON response
    return JsonResponse(data, safe=False)

def getMaterial(request, material_id):
    # Retrieve the material from the database
    material = get_object_or_404(Material, id=material_id)
    # Convert material to JSON format
    data = {'id': material.id,
            'name': material.name,
            'description': material.description,
            'etat': material.etat,
            'quantity': material.quantity,
            'unitPrice': material.unitPrice,
            'created_at': material.created_at,
            }
    # Return the JSON response
    return JsonResponse(data)

@transaction.atomic
def addTransaction(request):
    if request.method == 'POST':
        transactionType = request.POST.get('transactionType')
        user = request.user

        if(transactionType == 'out'):
            material_id = request.POST.get('material_id')
            quantity = int(request.POST.get('quantity'))
            deliveryAddress = request.POST.get('deliveryAddress')
            
            # Retrieve the material from the database
            material = get_object_or_404(Material, id=material_id)
            
            # Check if there is enough quantity available
            if material.quantity >= quantity:
                # Create a new transaction
                transaction = Transaction.objects.create(material=material, deliveryAddress=deliveryAddress , quantity=quantity , user=user, transactionType=transactionType)
                transaction.save()
                
                # Update the material quantity
                material.quantity -= quantity
                material.save()
                
                return JsonResponse({'success': True, 'transaction_id': transaction.id})
            else:
                return JsonResponse({'success': False, 'errors': 'Not enough quantity available'}, status=400)
            
        elif(transactionType == 'in'):
            material_id = request.POST.get('material_id')
            quantity = int(request.POST.get('quantity'))
            deliveryAddress = request.POST.get('deliveryAddress')

            
            # Retrieve the material from the database
            material = get_object_or_404(Material, id=material_id)
            
            # Create a new transaction
            transaction = Transaction.objects.create(material=material, quantity=quantity,deliveryAddress=deliveryAddress, transactionType=transactionType, user=request.user)
            transaction.save()
            
            # Update the material quantity
            material.quantity += quantity
            material.save()
            
            return JsonResponse({'success': True, 'transaction_id': transaction.id})
    else:
        return JsonResponse({'success': False, 'errors': 'errors occured'}, status=400)

@transaction.atomic
def deleteTransaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == 'POST':
        # Retrieve the material associated with the transaction
        material = transaction.material
        
        # Update the material quantity
        material.quantity += transaction.quantity
        material.save()
        
        # Delete the transaction
        transaction.delete()
        
        return JsonResponse({'success': True, 'transaction_id': transaction.id})
    else:
        # Render the confirmation page
        return JsonResponse({'success': False, 'errors': 'errors occurred'}, status=400)
    
def getTransactions(request):
    # Retrieve all transactions from the database
    transactions = Transaction.objects.all()
    # Convert transactions to JSON format
    data = [{'id': transaction.id,
             'user': transaction.user.username,
            'material_id': transaction.material.id,
            'material_name': transaction.material.name,
            'deliveryAddress': transaction.deliveryAddress,
            'quantity': transaction.quantity,
            'transactionType': transaction.transactionType,
            'created_at': transaction.created_at,
            } for transaction in transactions]
    # Return the JSON response
    return JsonResponse(data, safe=False)

def getTransaction(request, transaction_id):
    # Retrieve the transaction from the database
    transaction = get_object_or_404(Transaction, id=transaction_id)
    # Convert transaction to JSON format
    data = {'id': transaction.id,
            'user': transaction.user.username,
            'material_id': transaction.material.id,
            'material_name': transaction.material.name,
            'deliveryAddress': transaction.deliveryAddress,
            'quantity': transaction.quantity,
            'transactionType': transaction.transactionType,
            'created_at': transaction.created_at,
            }
    # Return the JSON response
    return JsonResponse(data)

def getTransactionsByMaterial(request, material_id):
    # Retrieve all transactions associated with the material from the database
    transactions = Transaction.objects.filter(material_id=material_id)
    # Convert transactions to JSON format
    data = [{'id': transaction.id,
             'user': transaction.user.username,
            'material_id': transaction.material.id,
            'material_name': transaction.material.name,
            'deliveryAddress': transaction.deliveryAddress,
            'quantity': transaction.quantity,
            'transactionType': transaction.transactionType,
            'created_at': transaction.created_at,
            } for transaction in transactions]
    # Return the JSON response
    return JsonResponse(data, safe=False)

def updateTransaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        transaction.quantity = int(request.POST.get('quantity'))
        transaction.deliveryAddress = request.POST.get('deliveryAddress')
        transaction.save()
        return JsonResponse({'success': True, 'transaction_id': transaction.id})
    else:
        # Render the form with the current transaction data
        return JsonResponse({'success': False, 'errors': 'errors occurred'}, status=400)

def addConfirmation(request):
    if request.method == 'POST':
        # Retrieve the necessary data from the request
        collector = request.user
        deliveryDate = request.POST.get('deliveryDate')
        transaction = get_object_or_404(Transaction, id=request.POST.get('transaction_id'))
        
        confirmation = Confirmation.objects.create(transaction=transaction, collector=collector, quantity=quantity, deliveryDate=deliveryDate)
        confirmation.save()
        
        return JsonResponse({'success': True, 'confirmation_id': confirmation.id})
    else:
        return JsonResponse({'success': False, 'errors': 'errors occurred'}, status=400)

def getConfirmation(request, confirmation_id):
    # Retrieve the confirmation from the database
    confirmation = get_object_or_404(Confirmation, id=confirmation_id)
    
    # Convert confirmation to JSON format
    data = {
        'id': confirmation.id,
        'transaction': confirmation.transaction,
        'collector': confirmation.collector,
        'deliveryDate': confirmation.deliveryDate,
        'created_at': confirmation.created_at,
        # Include other necessary fields
    }
    
    # Return the JSON response
    return JsonResponse(data)

def getConfirmations(request):
    # Retrieve all confirmations from the database
    confirmations = Confirmation.objects.all()
    
    # Convert confirmations to JSON format
    data = [
        {
        'id': confirmation.id,
        'transaction': confirmation.transaction,
        'collector': confirmation.collector,
        'deliveryDate': confirmation.deliveryDate,
        'created_at': confirmation.created_at,
        }
        for confirmation in confirmations
    ]
    
    # Return the JSON response
    return JsonResponse(data, safe=False)

def getConfirmationsByCollector(request, collector_id):
    # Retrieve all confirmations associated with the collector from the database
    confirmations = Confirmation.objects.filter(collector_id=collector_id)
    
    # Convert confirmations to JSON format
    data = [
        {
        'id': confirmation.id,
        'transaction': confirmation.transaction,
        'collector': confirmation.collector,
        'deliveryDate': confirmation.deliveryDate,
        'created_at': confirmation.created_at,
        }
        for confirmation in confirmations
    ]
    
    # Return the JSON response
    return JsonResponse(data, safe=False)

def deleteConfirmation(request, confirmation_id):
    confirmation = get_object_or_404(Confirmation, id=confirmation_id)
    if request.method == 'POST':
        # Perform the necessary operations to delete the confirmation
        confirmation.delete()
        return JsonResponse({'success': True, 'confirmation_id': confirmation.id})
    else:
        # Render the confirmation page
        return JsonResponse({'success': False, 'errors': 'errors occurred'}, status=400)

def updateConfirmation(request, confirmation_id):
    confirmation = get_object_or_404(Confirmation, id=confirmation_id)
    if request.method == 'POST':
        # Retrieve the necessary data from the request
        deliveryDate = request.POST.get('deliveryDate')
        
        # Perform the necessary operations to update the confirmation
        
        return JsonResponse({'success': True, 'confirmation_id': confirmation.id})
    else:
        # Render the form with the current confirmation data
        return JsonResponse({'success': False, 'errors': 'errors occurred'}, status=400)
