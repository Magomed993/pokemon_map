from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField("lat")
    lon = models.FloatField("lon")
    appeared_at = models.DateTimeField('appeared_at')
    disappeared_at = models.DateTimeField('disappeared_at')
