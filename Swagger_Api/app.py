from flask import Flask, jsonify, request, render_template
from flask_restx import Api, Resource, fields, Namespace
import json
import os
import requests

app = Flask(__name__)

# Configure Swagger UI
api = Api(
    app,
    version='1.0',
    title='Space Exploration API',
    description='A comprehensive API for space exploration data including planets, rockets, astronauts, telescopes, space agencies, and terminology.\n\n**Designed and Developed by Aradhya Pavan**',
    doc='/swagger/',
    prefix='/api',
    contact='Aradhya Pavan'
)


# NASA Images API configuration
NASA_IMAGES_API_BASE = "https://images-api.nasa.gov"

def search_nasa_images(query="", year="", page=1, page_size=20):
    """Search NASA Images API"""
    try:
        params = {
            'q': query if query else 'space',
            'media_type': 'image',
            'page': page,
            'page_size': page_size
        }
        
        if year:
            params['year_start'] = year
            params['year_end'] = year
            
        response = requests.get(f"{NASA_IMAGES_API_BASE}/search", params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        items = []
        
        if 'collection' in data and 'items' in data['collection']:
            for item in data['collection']['items']:
                if 'data' in item and len(item['data']) > 0:
                    item_data = item['data'][0]
                    image_info = {
                        'nasa_id': item_data.get('nasa_id', ''),
                        'title': item_data.get('title', 'Untitled'),
                        'description': item_data.get('description', ''),
                        'date_created': item_data.get('date_created', ''),
                        'center': item_data.get('center', ''),
                        'keywords': item_data.get('keywords', []),
                        'photographer': item_data.get('photographer', ''),
                        'location': item_data.get('location', ''),
                        'href': item.get('href', ''),
                        'thumbnail': ''
                    }
                    
                    # Get thumbnail URL
                    if 'links' in item:
                        for link in item['links']:
                            if link.get('rel') == 'preview':
                                image_info['thumbnail'] = link.get('href', '')
                                break
                    
                    items.append(image_info)
        
        return {
            'items': items,
            'total': data.get('collection', {}).get('metadata', {}).get('total_hits', 0)
        }
        
    except requests.RequestException as e:
        print(f"Error fetching NASA images: {e}")
        return {'items': [], 'total': 0}

# Data loading functions
def load_space_terms():
    try:
        with open('data/space_terminology.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['space_terms']
    except FileNotFoundError:
        return []

def load_space_agencies():
    try:
        with open('data/space_agencies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['space_agencies']
    except FileNotFoundError:
        return []

def load_planets():
    try:
        with open('data/planets.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['planets']
    except FileNotFoundError:
        return []

def load_rockets():
    try:
        with open('data/rockets.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['rockets']
    except FileNotFoundError:
        return []

def load_astronauts():
    try:
        with open('data/astronauts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['astronauts']
    except FileNotFoundError:
        return []

def load_telescopes():
    try:
        with open('data/telescopes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['telescopes']
    except FileNotFoundError:
        return []

def load_museums():
    try:
        with open('data/space_museams.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['space_museums']
    except FileNotFoundError:
        return []

def load_notable_people():
    try:
        with open('data/notable_peoples.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['notable_space_contributors']
    except FileNotFoundError:
        return []

# Define namespaces
terms_ns = Namespace('terms', description='Space terminology operations')
agencies_ns = Namespace('agencies', description='Space agencies operations')
planets_ns = Namespace('planets', description='Planets information')
rockets_ns = Namespace('rockets', description='Rockets and launch vehicles')
astronauts_ns = Namespace('astronauts', description='Astronauts and cosmonauts')
telescopes_ns = Namespace('telescopes', description='Telescopes and observatories')
museums_ns = Namespace('museums', description='Space museums and centers')
people_ns = Namespace('people', description='Notable space contributors')
images_ns = Namespace('images', description='Space images from NASA')

api.add_namespace(terms_ns)
api.add_namespace(agencies_ns)
api.add_namespace(planets_ns)
api.add_namespace(rockets_ns)
api.add_namespace(astronauts_ns)
api.add_namespace(telescopes_ns)
api.add_namespace(museums_ns)
api.add_namespace(people_ns)
api.add_namespace(images_ns)

# Define response models
term_model = api.model('Term', {
    'id': fields.String(required=True, description='Term identifier'),
    'term': fields.String(required=True, description='Term name'),
    'short_description': fields.String(required=True, description='Brief description'),
    'detailed_description': fields.String(required=True, description='Detailed description'),
    'category': fields.String(required=True, description='Term category'),
    'keywords': fields.List(fields.String, description='Related keywords')
})

agency_model = api.model('Agency', {
    'id': fields.String(required=True, description='Agency identifier'),
    'name': fields.String(required=True, description='Agency name'),
    'full_name': fields.String(required=True, description='Full agency name'),
    'country': fields.String(required=True, description='Country'),
    'type': fields.String(required=True, description='Agency type'),
    'description': fields.String(required=True, description='Agency description'),
    'founded': fields.String(description='Year founded'),
    'headquarters': fields.String(description='Headquarters location')
})

planet_model = api.model('Planet', {
    'id': fields.String(required=True, description='Planet identifier'),
    'name': fields.String(required=True, description='Planet name'),
    'type': fields.String(required=True, description='Planet type'),
    'description': fields.String(required=True, description='Planet description'),
    'distance_from_sun': fields.String(description='Distance from sun'),
    'orbital_period': fields.String(description='Orbital period'),
    'rotation_period': fields.String(description='Rotation period'),
    'moons': fields.Integer(description='Number of moons')
})

rocket_model = api.model('Rocket', {
    'id': fields.String(required=True, description='Rocket identifier'),
    'name': fields.String(required=True, description='Rocket name'),
    'type': fields.String(required=True, description='Rocket type'),
    'description': fields.String(required=True, description='Rocket description'),
    'manufacturer': fields.String(description='Manufacturer'),
    'first_flight': fields.String(description='First flight date'),
    'status': fields.String(description='Current status')
})

astronaut_model = api.model('Astronaut', {
    'id': fields.String(required=True, description='Astronaut identifier'),
    'name': fields.String(required=True, description='Astronaut name'),
    'country': fields.String(required=True, description='Country'),
    'agency': fields.String(required=True, description='Space agency'),
    'type': fields.String(required=True, description='Astronaut type'),
    'description': fields.String(required=True, description='Astronaut description'),
    'missions': fields.List(fields.String, description='Missions participated')
})

telescope_model = api.model('Telescope', {
    'id': fields.String(required=True, description='Telescope identifier'),
    'name': fields.String(required=True, description='Telescope name'),
    'year': fields.Integer(description='Year built/launched'),
    'type': fields.String(required=True, description='Telescope type'),
    'country': fields.String(description='Country'),
    'agency': fields.String(description='Agency or organization'),
    'inventor': fields.String(description='Inventor or creator'),
    'status': fields.String(description='Current status'),
    'budget': fields.String(description='Budget information'),
    'aperture': fields.String(description='Telescope aperture'),
    'description': fields.String(required=True, description='Telescope description'),
    'key_discoveries': fields.List(fields.String, description='Key discoveries made'),
    'image_url': fields.String(description='Image URL')
})

museum_model = api.model('Museum', {
    'name': fields.String(required=True, description='Museum name'),
    'country': fields.String(required=True, description='Country'),
    'city_or_region': fields.String(required=True, description='City or region'),
    'famous_for': fields.String(required=True, description='What the museum is famous for'),
    'established_year': fields.Integer(description='Year established'),
    'annual_visitors': fields.Integer(description='Annual visitor count'),
    'additional_info': fields.String(description='Additional information')
})

notable_person_model = api.model('NotablePerson', {
    'name': fields.String(required=True, description='Person name'),
    'country': fields.String(required=True, description='Country'),
    'birth_date': fields.String(description='Birth date'),
    'death_date': fields.String(description='Death date (if applicable)'),
    'contribution': fields.String(required=True, description='Contribution to space exploration'),
    'known_for': fields.String(required=True, description='What they are known for'),
    'awards': fields.List(fields.String, description='Awards received'),
    'notable_works': fields.List(fields.String, description='Notable works'),
    'institutions': fields.List(fields.String, description='Associated institutions'),
    'public_image': fields.String(description='Public image URL')
})

image_model = api.model('Image', {
    'nasa_id': fields.String(required=True, description='NASA image identifier'),
    'title': fields.String(required=True, description='Image title'),
    'description': fields.String(description='Image description'),
    'date_created': fields.String(description='Creation date'),
    'center': fields.String(description='NASA center'),
    'keywords': fields.List(fields.String, description='Keywords'),
    'photographer': fields.String(description='Photographer'),
    'location': fields.String(description='Location'),
    'href': fields.String(description='Link to image data'),
    'thumbnail': fields.String(description='Thumbnail URL')
})

# Space Terms API
@terms_ns.route('/')
class TermsList(Resource):
    @terms_ns.doc('get_terms')
    @terms_ns.param('letter', 'Filter by starting letter')
    @terms_ns.param('search', 'Search in term name, description, or category')
    @terms_ns.marshal_list_with(term_model)
    def get(self):
        """Get all space terms with optional filtering"""
        terms = load_space_terms()
        
        # Filter by letter if provided
        letter = request.args.get('letter', '').upper()
        if letter:
            terms = [term for term in terms if term['term'].upper().startswith(letter)]
        
        # Filter by search query if provided
        search_query = request.args.get('search', '').lower()
        if search_query:
            terms = [term for term in terms if 
                    search_query in term['term'].lower() or 
                    search_query in term['short_description'].lower() or
                    search_query in term['category'].lower()]
        
        # Sort alphabetically
        terms.sort(key=lambda x: x['term'].lower())
        
        return terms

@terms_ns.route('/<string:term_id>')
class Term(Resource):
    @terms_ns.doc('get_term')
    @terms_ns.marshal_with(term_model)
    def get(self, term_id):
        """Get a specific term by ID"""
        terms = load_space_terms()
        term = next((t for t in terms if t['id'] == term_id), None)
        
        if term:
            return term
        else:
            api.abort(404, f'Term {term_id} not found')

@terms_ns.route('/categories')
class Categories(Resource):
    @terms_ns.doc('get_categories')
    def get(self):
        """Get all available term categories"""
        terms = load_space_terms()
        categories = list(set(term['category'] for term in terms))
        categories.sort()
        return categories

@terms_ns.route('/alphabet')
class AlphabetStats(Resource):
    @terms_ns.doc('get_alphabet_stats')
    def get(self):
        """Get term count for each letter of the alphabet"""
        terms = load_space_terms()
        alphabet_stats = {}
        
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            count = len([term for term in terms if term['term'].upper().startswith(letter)])
            alphabet_stats[letter] = count
        
        return alphabet_stats

# Space Agencies API
@agencies_ns.route('/')
class AgenciesList(Resource):
    @agencies_ns.doc('get_agencies')
    @agencies_ns.param('type', 'Filter by agency type')
    @agencies_ns.param('country', 'Filter by country')
    @agencies_ns.param('search', 'Search in agency name, full name, country, or description')
    @agencies_ns.marshal_list_with(agency_model)
    def get(self):
        """Get all space agencies with optional filtering"""
        agencies = load_space_agencies()
        
        # Filter by type if provided
        agency_type = request.args.get('type', '').lower()
        if agency_type and agency_type != 'all':
            agencies = [agency for agency in agencies if agency['type'].lower() == agency_type]
        
        # Filter by country if provided
        country = request.args.get('country', '')
        if country and country != 'all':
            agencies = [agency for agency in agencies if agency['country'].lower() == country.lower()]
        
        # Filter by search query if provided
        search_query = request.args.get('search', '').lower()
        if search_query:
            agencies = [agency for agency in agencies if 
                       search_query in agency['name'].lower() or 
                       search_query in agency['full_name'].lower() or
                       search_query in agency['country'].lower() or
                       search_query in agency['description'].lower()]
        
        # Sort alphabetically
        agencies.sort(key=lambda x: x['name'].lower())
        
        return agencies

@agencies_ns.route('/<string:agency_id>')
class Agency(Resource):
    @agencies_ns.doc('get_agency')
    @agencies_ns.marshal_with(agency_model)
    def get(self, agency_id):
        """Get a specific agency by ID"""
        agencies = load_space_agencies()
        agency = next((a for a in agencies if a['id'] == agency_id), None)
        
        if agency:
            return agency
        else:
            api.abort(404, f'Agency {agency_id} not found')

# Planets API
@planets_ns.route('/')
class PlanetsList(Resource):
    @planets_ns.doc('get_planets')
    @planets_ns.param('type', 'Filter by planet type')
    @planets_ns.param('search', 'Search in planet name, description, or type')
    @planets_ns.marshal_list_with(planet_model)
    def get(self):
        """Get all planets with optional filtering"""
        planets = load_planets()
        
        # Filter by type if provided
        planet_type = request.args.get('type', '').lower()
        if planet_type and planet_type != 'all':
            planets = [planet for planet in planets if planet['type'].lower() == planet_type]
        
        # Filter by search query if provided
        search_query = request.args.get('search', '').lower()
        if search_query:
            planets = [planet for planet in planets if 
                      search_query in planet['name'].lower() or 
                      search_query in planet['description'].lower() or
                      search_query in planet['type'].lower()]
        
        # Sort by distance from sun (inner to outer)
        distance_order = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        planets.sort(key=lambda x: distance_order.index(x['id']) if x['id'] in distance_order else 999)
        
        return planets

@planets_ns.route('/<string:planet_id>')
class Planet(Resource):
    @planets_ns.doc('get_planet')
    @planets_ns.marshal_with(planet_model)
    def get(self, planet_id):
        """Get a specific planet by ID"""
        planets = load_planets()
        planet = next((p for p in planets if p['id'] == planet_id), None)
        
        if planet:
            return planet
        else:
            api.abort(404, f'Planet {planet_id} not found')

# Rockets API
@rockets_ns.route('/')
class RocketsList(Resource):
    @rockets_ns.doc('get_rockets')
    @rockets_ns.param('type', 'Filter by rocket type')
    @rockets_ns.param('search', 'Search in rocket name, description, or type')
    @rockets_ns.marshal_list_with(rocket_model)
    def get(self):
        """Get all rockets with optional filtering"""
        rockets = load_rockets()
        
        # Filter by type if provided
        rocket_type = request.args.get('type', '').lower()
        if rocket_type and rocket_type != 'all':
            rockets = [rocket for rocket in rockets if rocket['type'].lower() == rocket_type]
        
        # Filter by search query if provided
        search_query = request.args.get('search', '').lower()
        if search_query:
            rockets = [rocket for rocket in rockets if 
                      search_query in rocket['name'].lower() or 
                      search_query in rocket['description'].lower() or
                      search_query in rocket['type'].lower()]
        
        # Sort alphabetically
        rockets.sort(key=lambda x: x['name'].lower())
        
        return rockets

@rockets_ns.route('/<string:rocket_id>')
class Rocket(Resource):
    @rockets_ns.doc('get_rocket')
    @rockets_ns.marshal_with(rocket_model)
    def get(self, rocket_id):
        """Get a specific rocket by ID"""
        rockets = load_rockets()
        rocket = next((r for r in rockets if r['id'] == rocket_id), None)
        
        if rocket:
            return rocket
        else:
            api.abort(404, f'Rocket {rocket_id} not found')

# Astronauts API
@astronauts_ns.route('/')
class AstronautsList(Resource):
    @astronauts_ns.doc('get_astronauts')
    @astronauts_ns.param('country', 'Filter by country')
    @astronauts_ns.param('type', 'Filter by astronaut type')
    @astronauts_ns.param('search', 'Search in astronaut name, description, country, or agency')
    @astronauts_ns.marshal_list_with(astronaut_model)
    def get(self):
        """Get all astronauts with optional filtering"""
        astronauts = load_astronauts()
        
        # Filter by country if provided
        country = request.args.get('country', '')
        if country and country != 'all':
            astronauts = [astronaut for astronaut in astronauts if astronaut['country'].lower() == country.lower()]
        
        # Filter by agency type if provided
        agency_type = request.args.get('type', '').lower()
        if agency_type and agency_type != 'all':
            astronauts = [astronaut for astronaut in astronauts if astronaut['type'].lower() == agency_type]
        
        # Filter by search query if provided
        search_query = request.args.get('search', '').lower()
        if search_query:
            astronauts = [astronaut for astronaut in astronauts if 
                         search_query in astronaut['name'].lower() or 
                         search_query in astronaut['description'].lower() or
                         search_query in astronaut['country'].lower() or
                         search_query in astronaut['agency'].lower()]
        
        # Sort alphabetically by name
        astronauts.sort(key=lambda x: x['name'].lower())
        
        return astronauts

@astronauts_ns.route('/<string:astronaut_id>')
class Astronaut(Resource):
    @astronauts_ns.doc('get_astronaut')
    @astronauts_ns.marshal_with(astronaut_model)
    def get(self, astronaut_id):
        """Get a specific astronaut by ID"""
        astronauts = load_astronauts()
        astronaut = next((a for a in astronauts if a['id'] == astronaut_id), None)
        
        if astronaut:
            return astronaut
        else:
            api.abort(404, f'Astronaut {astronaut_id} not found')

# Telescopes API
@telescopes_ns.route('/')
class TelescopesList(Resource):
    @telescopes_ns.doc('get_telescopes')
    @telescopes_ns.param('type', 'Filter by telescope type')
    @telescopes_ns.param('country', 'Filter by country')
    @telescopes_ns.param('search', 'Search in telescope name, description, country, or inventor')
    @telescopes_ns.marshal_list_with(telescope_model)
    def get(self):
        """Get all telescopes with optional filtering"""
        telescopes = load_telescopes()
        
        # Filter by type if provided
        telescope_type = request.args.get('type', '').lower()
        if telescope_type and telescope_type != 'all':
            telescopes = [telescope for telescope in telescopes if telescope['type'].lower() == telescope_type]
        
        # Filter by country if provided
        country = request.args.get('country', '')
        if country and country != 'all':
            telescopes = [telescope for telescope in telescopes if telescope.get('country', '').lower() == country.lower()]
        
        # Filter by search query if provided
        search_query = request.args.get('search', '').lower()
        if search_query:
            telescopes = [telescope for telescope in telescopes if 
                         search_query in telescope['name'].lower() or 
                         search_query in telescope.get('description', '').lower() or
                         search_query in telescope.get('country', '').lower() or
                         search_query in telescope.get('inventor', '').lower()]
        
        # Sort by year (newest first)
        telescopes.sort(key=lambda x: x.get('year', 0), reverse=True)
        
        return telescopes

@telescopes_ns.route('/<string:telescope_id>')
class Telescope(Resource):
    @telescopes_ns.doc('get_telescope')
    @telescopes_ns.marshal_with(telescope_model)
    def get(self, telescope_id):
        """Get a specific telescope by ID"""
        telescopes = load_telescopes()
        telescope = next((t for t in telescopes if t['id'] == telescope_id), None)
        
        if telescope:
            return telescope
        else:
            api.abort(404, f'Telescope {telescope_id} not found')

# Museums API
@museums_ns.route('/')
class MuseumsList(Resource):
    @museums_ns.doc('get_museums')
    @museums_ns.param('country', 'Filter by country')
    @museums_ns.param('search', 'Search in museum name, country, city, or what they are famous for')
    @museums_ns.marshal_list_with(museum_model)
    def get(self):
        """Get all space museums with optional filtering"""
        museums = load_museums()
        
        # Filter by country if provided
        country = request.args.get('country', '')
        if country and country != 'all':
            museums = [museum for museum in museums if museum['country'].lower() == country.lower()]
        
        # Filter by search query if provided
        search_query = request.args.get('search', '').lower()
        if search_query:
            museums = [museum for museum in museums if 
                      search_query in museum['name'].lower() or 
                      search_query in museum['country'].lower() or
                      search_query in museum['city_or_region'].lower() or
                      search_query in museum['famous_for'].lower()]
        
        # Sort by annual visitors (highest first)
        museums.sort(key=lambda x: x.get('annual_visitors', 0), reverse=True)
        
        return museums

@museums_ns.route('/<string:museum_name>')
class Museum(Resource):
    @museums_ns.doc('get_museum')
    @museums_ns.marshal_with(museum_model)
    def get(self, museum_name):
        """Get a specific museum by name"""
        museums = load_museums()
        # Replace URL encoding and normalize name for search
        museum_name_normalized = museum_name.replace('%20', ' ').replace('_', ' ').lower()
        museum = next((m for m in museums if m['name'].lower() == museum_name_normalized), None)
        
        if museum:
            return museum
        else:
            api.abort(404, f'Museum "{museum_name}" not found')

# Notable People API
@people_ns.route('/')
class PeopleList(Resource):
    @people_ns.doc('get_people')
    @people_ns.param('country', 'Filter by country')
    @people_ns.param('search', 'Search in person name, country, contribution, or known for')
    @people_ns.marshal_list_with(notable_person_model)
    def get(self):
        """Get all notable space contributors with optional filtering"""
        people = load_notable_people()
        
        # Filter by country if provided
        country = request.args.get('country', '')
        if country and country != 'all':
            people = [person for person in people if person['country'].lower() == country.lower()]
        
        # Filter by search query if provided
        search_query = request.args.get('search', '').lower()
        if search_query:
            people = [person for person in people if 
                     search_query in person['name'].lower() or 
                     search_query in person['country'].lower() or
                     search_query in person['contribution'].lower() or
                     search_query in person['known_for'].lower()]
        
        # Sort alphabetically by name
        people.sort(key=lambda x: x['name'].lower())
        
        return people

@people_ns.route('/<string:person_name>')
class Person(Resource):
    @people_ns.doc('get_person')
    @people_ns.marshal_with(notable_person_model)
    def get(self, person_name):
        """Get a specific notable person by name"""
        people = load_notable_people()
        # Replace URL encoding and normalize name for search
        person_name_normalized = person_name.replace('%20', ' ').replace('_', ' ').lower()
        person = next((p for p in people if p['name'].lower() == person_name_normalized), None)
        
        if person:
            return person
        else:
            api.abort(404, f'Person "{person_name}" not found')

# Images API
@images_ns.route('/')
class ImagesList(Resource):
    @images_ns.doc('get_images')
    @images_ns.param('search', 'Search query for images')
    @images_ns.param('year', 'Filter by year')
    @images_ns.param('page', 'Page number (default: 1)')
    @images_ns.param('page_size', 'Items per page (default: 20)')
    def get(self):
        """Get space images from NASA API"""
        # Get query parameters
        search_query = request.args.get('search', '')
        year = request.args.get('year', '')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        
        # Search NASA Images API
        result = search_nasa_images(search_query, year, page, page_size)
        
        return result

# Index route for the awesome homepage with dynamic stats
@app.route('/')
def index():
    """Serve the awesome index page with real data counts"""
    # Get actual counts from data files
    try:
        terms_count = len(load_space_terms())
        agencies_count = len(load_space_agencies()) 
        planets_count = len(load_planets())
        rockets_count = len(load_rockets())
        astronauts_count = len(load_astronauts())
        telescopes_count = len(load_telescopes())
        museums_count = len(load_museums())
        people_count = len(load_notable_people())
        
        # Count unique countries
        countries = set()
        for agency in load_space_agencies():
            if 'country' in agency:
                countries.add(agency['country'])
        for astronaut in load_astronauts():
            if 'country' in astronaut:
                countries.add(astronaut['country'])
        for person in load_notable_people():
            if 'country' in person:
                countries.add(person['country'])
        for museum in load_museums():
            if 'country' in museum:
                countries.add(museum['country'])
        
        countries_count = len(countries)
        total_data_points = terms_count + agencies_count + planets_count + rockets_count + astronauts_count + telescopes_count + museums_count + people_count
        
        stats = {
            'terms': terms_count,
            'agencies': agencies_count,
            'planets': planets_count,
            'rockets': rockets_count,
            'astronauts': astronauts_count,
            'telescopes': telescopes_count,
            'museums': museums_count,
            'people': people_count,
            'countries': countries_count,
            'total': total_data_points
        }
        
        return render_template('index.html', stats=stats)
    except Exception as e:
        print(f"Error loading stats: {e}")
        # Fallback to default stats
        return render_template('index.html')

if __name__ == "__main__":
    app.run()
