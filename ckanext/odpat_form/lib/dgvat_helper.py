# -*- coding: utf-8 -*- 
import logging
from datetime import datetime

log = logging.getLogger(__name__)


def map_license(license, default = 'cc-by'):
    if license == u'Creative Commons Namensnennung 3.0 Österreich':
      return 'cc-by'
    if license == 'CC-BY-3.0':
      return 'cc-by'
    log.info("helper: map_license() could not find license for %s - is returning default" % license)
    return default

def map_update_frequency(freq):
    if freq:
        #freq = unicode(freq, 'utf8')
        found = [item for item in update_frequency if freq in item]
        if found:
            return found[0][0]
    return None

def get_update_frequency_by_id(freq_id):
    if freq_id:
        return (item[1] for item in update_frequency if freq_id in item).next()
    return None        

def map_categorization(cat):
    if cat:
        cat = unicode(cat, 'utf8')
        for c in categorization:
            if t[0] == cat:
                return t[1]
            elif t[1] == cat:
                return t[1]
    return None

def get_categorization_by_id(cat_id):
    if cat_id:
        return (c[0] for c in categorization if c[1] == cat_id).next()
    return None



def map_metadata_field(field):
    if field:
        for f in metadata_fields:
            if f[0] == field:
                return f[1]
    return None

def get_metadata_field_by_id(field_id):
    if field_id:
        for f in metadata_fields:
            if f[0] == field_id:
                return f[2]
    return None

def get_basic_metadata_fields():
    fields = [item for item in metadata_fields if not item[2].startswith('resources:') and not item[2].startswith('extras:') and item[3] == 'show']
    return fields

def get_extended_metadata_fields():
    fields = [item for item in metadata_fields if item[2].startswith('extras:') and item[3] == 'show']
    return fields

def get_resource_metadata_fields():
    fields = [item for item in metadata_fields if item[2].startswith('resources:') and item[3] == 'show']
    return fields

def get_extras_element(extras, element):
    el = element.replace('extras:', '')
    found = (item[u'value'] for item in extras if item[u'key'] == el).next()
    if el == 'update_frequency':
        return get_update_frequency_by_id(found)
    elif el == 'categorization':
        cat = found.replace('{', '').replace('}', '').split(',')
        catList = ''
        for c in cat:
            catList += get_categorization_by_id(c) + ", "
        return catList[:-2]
    return found

def get_extras_from_basic(pkg, element):
    el = element.replace('extras:', '')
    found = pkg.get(el)
    if el == 'update_frequency':
        return get_update_frequency_by_id(found)
    elif el == 'categorization':
        if found:
            cat = found.replace('{', '').replace('}', '').split(',')
            catList = ''
            for c in cat:
                catList += get_categorization_by_id(c) + ", "
            return catList[:-2]
    elif el == 'begin_datetime' or el == 'end_datetime' or el == 'metadata_modified':
        if found:
            return datetime.strptime(found, "%Y-%m-%dT%H:%M:%S").strftime("%d.%m.%Y %H:%M:%S")
    elif el == 'metadata_identifier':
        if found:
            return found
        else: 
            return pkg.get('id')
    return found  

def get_label_by_field(label):
  return (item[1] for item in metadata_fields if label in item).next()


update_frequency = [('', '', ''),
                    ('continual', 'kontinuierlich', 'kontinuierlich'),
                    ('daily', u'täglich', 'taeglich'),
                    ('weekly', u'wöchentlich', 'woechentlich'),
                    ('fortnightly', u'14-tägig', '14-taegig'),
                    ('monthly', 'monatlich', 'monatlich'),
                    ('quarterly', 'quartalsweise', 'quartalsweise'),
                    ('biannually', u'halbjährlich', 'halbjaehrlich'),
                    ('annually', u'jährlich', 'jaehrlich'),
                    ('asNeeded', 'nach Bedarf', 'bei Bedarf'),
                    ('irregular', u'unregelmäßig', 'unregelmaessig'),
                    ('notPlanned', 'nicht geplant', 'nicht geplant'),
                    ('unknown', 'unbekannt', 'unbekannt'),]


categorization = [('', ''),
                  ('Arbeit', 'arbeit'),
                  (u'Bevölkerung', 'bevoelkerung'),
                  ('Bildung und Forschung', 'bildung-und-forschung'),
                  ('Finanzen und Rechnungswesen', 'finanzen-und-rechnungswesen'),
                  ('Geographie und Planung', 'geographie-und-planung'),
                  ('Gesellschaft und Soziales', 'gesellschaft-und-soziales'),
                  ('Gesundheit', 'gesundheit'),
                  ('Kunst und Kultur', 'kunst-und-kultur'),
                  ('Land und Forstwirtschaft', 'land-und-forstwirtschaft'),
                  ('Sport und Freizeit', 'sport-und-freizeit'),
                  ('Umwelt', 'umwelt'),
                  ('Verkehr und Technik', 'verkehr-und-technik'),
                  ('Verwaltung und Politik', 'verwaltung-und-politik'),
                  ('Wirtschaft und Tourismus', 'wirtschaft-und-tourismus'),]

metadata_fields = [('metadata_identifier', 'Eindeutiger Identifikator', 'extras:metadata_identifier', 'show'),
                   ('metadata_modified', 'Datum des Metadatensatzes', 'metadata_modified', 'show'),
                   ('title', 'Titel', 'title', 'hide'),
                   ('description', 'Beschreibung', 'notes', 'hide'),
                   ('categorization', 'Kategorie', 'extras:categorization', 'show'),
                   ('keywords', 'Schlagworte', 'tags', 'hide'),
                   ('resource_url', 'Datensatz, Dienst oder Dokument Link', 'resources:url'),
                   ('resource_format', 'Datensatz, Dienst oder Dokument Format', 'resources:format', 'show'),
                   ('maintainer', 'Datenverantwortliche Stelle', 'maintainer', 'show'),
                   ('license', 'Lizenz', 'license_title', 'show'),
                   ('begin_datetime', 'Zeitliche Ausdehnung (Anfang)', 'extras:begin_datetime', 'show'),
                   ('schema_name', 'Bezeichnung der Metadatenstruktur', 'extras:schema_name', 'show'),
                   ('schema_language', 'Sprache des Metadatensatzes', 'extras:schema_language', 'show'),
                   ('schema_characterset', 'Character Set Code des Metadatensatzes', 'extras:schema_characterset', 'show'),
                   ('metadata_linkage', u'Weiterführende Metadaten', 'extras:metadata_linkage', 'show'),
                   ('attribute_description', 'Attributbeschreibung', 'extras:attribute_description', 'show'),
                   ('maintainer_link', 'Kontaktseite der datenverantwortlichen Stelle', 'extras:maintainer_link', 'show'),
                   ('resource_name', 'Datensatz, Dienst oder Dokument Bezeichner', 'resources:name', 'show'),
                   ('resource_created', u'Datensatz, Dienst oder Dokument Veröffentlichungsdatum', 'resources:created', 'show'),
                   ('resource_lastmodified', u'Datensatz, Dienst oder Dokument Änderungsdatum', 'resources:last_modified', 'show'),
                   ('publisher', u'Veröffentlichende Stelle', 'extras:publisher', 'show'),
                   ('geographic_toponym', 'Geographische Abdeckung/Lage', 'extras:geographic_toponym', 'show'),
                   ('geographic_bbox', 'Geographische Ausdehnung', 'extras:geographic_bbox', 'show'),
                   ('end_datetime', 'Zeitliche Ausdehnung (Ende)', 'extras:end_datetime', 'show'),
                   ('update_frequency', 'Aktualisierungszyklus', 'extras:update_frequency', 'show'),
                   ('lineage_quality', u'Datenqualität/Herkunft ', 'extras:lineage_quality', 'show'),
                   ('en_title_and_desc', 'Titel und Beschreibung Englisch ', 'extras:en_title_and_desc', 'show'),
                   ('resource_size', u'Größe des Datensatzes, Dienstes oder Dokuments', 'resources:size', 'show'),
                   ('license_citation', 'Lizenz Zitat', 'extras:license_citation', 'show'),
                   ('resource_language', 'Sprache des Datensatzes, Dienstes oder Dokuments', 'resources:language', 'show'),
                   ('resource_encoding', 'Character Set Code des Datensatzes, Dienstes oder Dokuments', 'resources:characterset', 'show'),
                   ('metadata_original_portal', u'Link zu den ursprünglichen Metadaten', 'extras:metadata_original_portal', 'show'),
                   ('maintainer_email', 'Datenverantwortliche Stelle – E-Mailkontakt', 'maintainer_email', 'show'),               
                  ]