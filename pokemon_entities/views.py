import folium
import json

from django.utils import timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def get_image_url(request, pokemon):
    if pokemon.image:
        return request.build_absolute_uri(pokemon.image.url)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = timezone.localtime()
    pokemons = PokemonEntity.objects.filter(appeared_at__lte=now, disappeared_at__gte=now)
    for pokemon in pokemons:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            get_image_url(request, pokemon.pokemon)
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemon_image_url = get_image_url(request, pokemon)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    now = timezone.localtime()
    pokemons = PokemonEntity.objects.filter(appeared_at__lte=now, disappeared_at__gte=now)

    requested_pokemon = None
    for pokemon in pokemons:
        if pokemon.pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon.pokemon
            break
    if not requested_pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_image_url = get_image_url(request, requested_pokemon)
    pokemon_data = {
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "img_url": pokemon_image_url,
        "description": requested_pokemon.description
    }
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_image_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
