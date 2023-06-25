#l'importe l'objet Q pour faciliter apartir de plusieurs champs
from django.db.models import Q

# filtrer sur base de l'utilisateur connecter
# filtrer sur base du mode d'acquisition ou buy mode
class QSFilterWithByUserLogged():
    def get_queryset(self, *args, **kwargs):
        # on recuper l'user connecter ou authentifier
        user = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(user_id=user.pk)