from django.db import models


class BallonMass(models.Model):
    oxygen = models.IntegerField()
    argon = models.IntegerField()
    nitrogen = models.IntegerField()

    def __str__(self):
        return f"{self.oxygen} {self.argon} {self.nitrogen}"
