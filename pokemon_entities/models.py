from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    image = models.ImageField(null=True)
    description = models.TextField('description', blank=True)

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField("lat")
    lon = models.FloatField("lon")
    appeared_at = models.DateTimeField('appeared_at')
    disappeared_at = models.DateTimeField('disappeared_at')
    level = models.IntegerField('level')
    health = models.IntegerField('health')
    strength = models.IntegerField('strength')
    defence = models.IntegerField('defence')
    stamina = models.IntegerField('stamina')

    def __str__(self):
        return '{}'.format(self.pokemon.title)
