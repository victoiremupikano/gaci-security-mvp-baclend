from rest_framework import permissions

# class des groupes permis,....
class IsStaffPermissions(permissions.DjangoModelPermissions):
    # creation de la methode has_permission
    def has_permission(self, request, view):
        if not request.user.staff:
            return False 
        return True

# class pour verifier si l'user a access a certains methode
class IsStaffModelPermissions(permissions.DjangoModelPermissions):
    # creation de la methode has_permission
    def has_permission(self, request, view):
        if not request.user.staff:
            if request and request.method == "POST":
                return False
            elif request and request.method == "PUT":
                return False
            elif request and request.method == "DELETE":
                return False
            else:
                return True
        return True
