from django.urls import path
from . import views

urlpatterns = [
    path('addMaterial/', views.addMaterial, name='add_material'),
    path('getMaterial/<int:material_id>/', views.getMaterial, name='get_material'),
    path('updateMaterial/<int:material_id>/', views.updateMaterial, name='update_material'),
    path('getMaterials/', views.getMaterials, name='get_materials'),
    path('deleteMaterial/<int:material_id>/', views.deleteMaterial, name='delete_material'),
    path('addTransaction/', views.addTransaction, name='add_transaction'),
    path('getTransaction/<int:transaction_id>/', views.getTransaction, name='get_transaction'),
    path('getTransactions/', views.getTransactions, name='get_transactions'),
    path('getTransactionsByMaterial/<int:material_id>/', views.getTransactionsByMaterial, name='get_transactions_by_material'),
    path('deleteTransaction/<int:transaction_id>/', views.deleteTransaction, name='delete_transaction'),
    path('updateTransaction/<int:transaction_id>/', views.updateTransaction, name='update_transaction'),
    path('addConfirmation/', views.addConfirmation, name='add_confirmation'),
    path('getConfirmation/<int:confirmation_id>/', views.getConfirmation, name='get_confirmation'),
    path('getConfirmations/', views.getConfirmations, name='get_confirmations'),
    path('getConfirmationsByCollector/<int:collector_id>/', views.getConfirmationsByCollector, name='get_confirmations_by_collector'),
    path('deleteConfirmation/<int:confirmation_id>/', views.deleteConfirmation, name='delete_confirmation'),
    path('updateConfirmation/<int:confirmation_id>/', views.updateConfirmation, name='update_confirmation'),
]