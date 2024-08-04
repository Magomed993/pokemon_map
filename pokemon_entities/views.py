import folium
import json

from django.utils import timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon, PokemonEntity, PokemonElementType


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        popup=folium.Popup(f'Покемон: {name}\nШирота: {lat}\nДолгота: {lon}'),
        icon=icon,
    ).add_to(folium_map)


def get_image_url(request, pokemon):
    if pokemon.image:
        return request.build_absolute_uri(pokemon.image.url)
    return DEFAULT_IMAGE_URL


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=now, disappeared_at__gte=now)
    for pokemon in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon.lat,
            pokemon.lon,
            pokemon.pokemon.title,
            get_image_url(request, pokemon.pokemon)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
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
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    entity_specific_pokemon = PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lte=now, disappeared_at__gte=now)

    previous_evolution = {}
    if pokemon.previous_evolution:
        previous_evolution = {
            "title_ru": pokemon.previous_evolution.title,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": get_image_url(request, pokemon.previous_evolution),
        }

    next_pokemon = pokemon.next_evolutions.first()
    next_evolution = {}
    if next_pokemon:
        next_evolution = {
            "title_ru": next_pokemon.title,
            "pokemon_id": next_pokemon.id,
            "img_url": get_image_url(request, next_pokemon),
        }

    pokemon_data = {
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "img_url": get_image_url(request, pokemon),
        "description": pokemon.description,
        "previous_evolution": previous_evolution,
        'next_evolution': next_evolution,
        'element_type': [],
    }

    for elem in pokemon.element_type.all():
        strong_against = [strong_element.title for strong_element in elem.strong_against.all()]
        pokemon_data["element_type"].append({"img": get_image_url(request, elem),
                                             "title": elem.title,
                                             'strong_against': strong_against})

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in entity_specific_pokemon:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.title,
            get_image_url(request, pokemon_entity.pokemon)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
