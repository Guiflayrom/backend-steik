# core/signals.py
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Funcionario, Pedido, Restaurante

User = get_user_model()


@receiver(post_save, sender=Restaurante)
def create_user_for_restaurante(sender, instance, created, **kwargs):
    if created:
        User.objects.create_user(
            username=instance.email,
            password=instance.senha_acesso,
            restaurante=instance,
            email=instance.email,
        )


User = get_user_model()


@receiver(post_save, sender=Funcionario)
def criar_usuario_para_funcionario(sender, instance, created, **kwargs):
    if created and not instance.user:
        # Criando um nome de usuário único com base no ID do funcionário
        username = f"funcionario_{instance.id}@exemplo.com"

        # Criando o usuário
        user = User(username=username, email=username)
        user.set_password("inicial@123")  # Define a senha padrão
        user.save()

        # Vinculando o usuário ao funcionário
        instance.user = user
        instance.save()


@receiver(post_save, sender=Pedido)
def ajustar_valor_pago(sender, instance, **kwargs):
    # Verifica se o status é "Fechado" ou "Entregue"
    if instance.status in ["Fechado", "Entregue"]:
        # Calcula o valor total dos pratos associados ao pedido
        total_pratos = sum(
            prato_pedido.prato.valor * prato_pedido.quantidade
            for prato_pedido in instance.pratos.all()
        )
        # Atualiza o valor_pago para o total dos pratos
        Pedido.objects.filter(id=instance.id).update(valor_pago=total_pratos)
    else:
        # Define valor_pago como None para outros status
        Pedido.objects.filter(id=instance.id).update(valor_pago=None)
