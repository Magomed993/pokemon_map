from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Наименование")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Наименование на англ.")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="Наименование на яп.")
    image = models.ImageField(null=True, blank=True, verbose_name="Картинка")
    description = models.TextField(blank=True, verbose_name="Описание")
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name="next_evolution", verbose_name="Предыдущая эволюция")

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон")
    lat = models.FloatField(verbose_name="Широта", blank=True, null=True)
    lon = models.FloatField(verbose_name="Долгота", blank=True, null=True)
    appeared_at = models.DateTimeField(verbose_name="Появился", blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name="Исчез", blank=True, null=True)
    level = models.IntegerField(verbose_name="Уровень", blank=True, null=True)
    health = models.IntegerField(verbose_name="Здоровье", blank=True, null=True)
    strength = models.IntegerField(verbose_name="Сила", blank=True, null=True)
    defence = models.IntegerField(verbose_name="Защита", blank=True, null=True)
    stamina = models.IntegerField(verbose_name="Выносливость", blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.pokemon.title)
