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


def get_metadata_description_by_id(id):
  return (item[4] for item in metadata_fields if id == item[0]).next()  


def get_metadata_example_by_id(id):
  return (item[5] for item in metadata_fields if id == item[0]).next()    

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

metadata_fields = [('metadata_identifier', 'Eindeutiger Identifikator', 'extras:metadata_identifier', 'show', u'Eindeutiger Identifikator für den Metadatensatz. Der Eintrag beschreibt die eindeutige Identifikation für einen Metadatensatz. Es sollte eine UUID (nach RFC:4122) gewählt werden. ', '550e8400-e29b-11d4-a716-446655441234'),
                   ('metadata_modified', 'Datum des Metadatensatzes', 'metadata_modified', 'show', u'Datum, an dem der Metadatensatz erzeugt bzw. aktualisiert wurde. Die Datumsangabe erfolgt gemäß ÖNORM ISO 8601 YYYY-MM-DD. ', '2011-05-22'),
                   ('title', 'Titel', 'title', 'hide', u'Titel des beschriebenen Metadatensatzes bzw. des Dokumentes, Datensatzes und Dienstes', u'Pendlerstatistik Linz 2010'),
                   ('description', 'Beschreibung', 'notes', 'hide', 'Inhaltliche Beschreibung des Datensatzes, Dienstes oder Dokuments.', u'Hauptwohnsitzbevölkerung der Stadt Linz für das Jahr 2010 gruppiert nach Geschlecht, Alter etc.. '),
                   ('categorization', 'Kategorie', 'extras:categorization', 'show','Kategorisierung des Datensatzes, Dienstes oder Dokuments. ','Gesundheit '),
                   ('keywords', 'Schlagworte', 'tags', 'hide', 'Beschlagwortung des Datensatzes, Dienstes oder Dokuments. ', u'Habitatmodell, Braunbär, Ursus arctos '),
                   ('resource_url', 'Datensatz, Dienst oder Dokument Link', 'resources:url', u'URL für den Zugriff auf den Datensatz, Dienst oder das Dokument. ', 'http://www.wien.gv.at/statistik/ogd/b05-countrybirth-vie-dc.csv'),
                   ('resource_format', 'Datensatz, Dienst oder Dokument Format', 'resources:format', 'show', u'Angabe zum Format des Datensatzes, Dienstes oder des Dokuments. Diese ist als Dateiformat, Download- oder Service- Link anzugeben.', 'csv'),
                   ('maintainer', 'Datenverantwortliche Stelle', 'maintainer', 'show', u'Bezeichnung bzw. Name der für den Datensatz, Dienst oder das Dokument zuständigen Organisation bzw. Person ', 'Magistrat Wien - Magistratsabteilung 33 - Wien Leuchtet; '),
                   ('license', 'Lizenz', 'license_title', 'show', u'Rechtliche Nutzungsinformationen für die Verwendung des Datensatzes, Dienstes oder Dokuments. ', u'Creative Commons Namensnennung 3.0 Österreich'),
                   ('begin_datetime', 'Zeitliche Ausdehnung (Anfang)', 'extras:begin_datetime', 'show', u'Element zur Erfassung des Beginns der Gültigkeit eines Datensatzes, Dienstes oder Dokuments', '2008-12-23T22:30:12 '),
                   ('schema_name', 'Bezeichnung der Metadatenstruktur', 'extras:schema_name', 'show', u'Name der Metadatenstruktur', 'OGD Austria Metadata 2.2 '),
                   ('schema_language', 'Sprache des Metadatensatzes', 'extras:schema_language', 'show', u'ISO 639-2 dreistelliger ISO Sprachcode für den Metadatensatz', 'ger'),
                   ('schema_characterset', 'Character Set Code des Metadatensatzes', 'extras:schema_characterset', 'show', u'Characterset Code zur Beschreibung des Metadatensatzes nach ISO\IEC 10646-1 ', 'utf8'),
                   ('metadata_linkage', u'Weiterführende Metadaten', 'extras:metadata_linkage', 'show', u'Verweis zu weiterführenden Informationen zum Datensatz bzw. Dienst. Verweise auf Datensätze, die im Dokument benutzt oder interpretiert werden.', 'http://data.wien.gv.at/pdf/wienerlinien-echtzeitdaten-dokumentation.pdf '),
                   ('attribute_description', 'Attributbeschreibung', 'extras:attribute_description', 'show', u'Beschreibung der Attributinformation des Datensatzes bzw. Dienstes', u'ADRESSE: Adresse (Straßenname, Orientierungsnummer); OEFFNUNGSZEITEN1-6: Öffnungszeiten; TELEFON: Telefonnummer, DISTRICT_CODE: Gemeindebezirkskennzahl, ACCOUNTS_TRANSFER: Laufende Transferzahlungen '),
                   ('maintainer_link', 'Kontaktseite der datenverantwortlichen Stelle', 'extras:maintainer_link', 'show', u'Kontaktseite der datenverantwortlichen Stelle ', 'http://www.wien.gv.at/freizeit/bildungjugend/ '),
                   ('resource_name', 'Datensatz, Dienst oder Dokument Bezeichner', 'resources:name', 'show', u'Bezeichner für den einzelnen Datensatz bzw. Dienst oder das einzelne Dokument. Das Attribut korrespondiert mit dem Metadaten – Datensatz oder Dienst Link', u'Hauptwohnsitzbevölkerung'),
                   ('resource_created', u'Datensatz, Dienst oder Dokument Veröffentlichungsdatum', 'resources:created', 'show', u'Datum der Veröffentlichung des Datensatzes, Dienstes oder Dokuments. ', '2011-03-21 ( YYYY-MM-DD) '),
                   ('resource_lastmodified', u'Datensatz, Dienst oder Dokument Änderungsdatum', 'resources:last_modified', 'show', u'Datum der letzten Aktualisierung des Datensatzes, Dienstes oder Dokuments. ', '2012-01-15 ( YYYY-MM-DD ) '),
                   ('publisher', u'Veröffentlichende Stelle', 'extras:publisher', 'show', u'Bezeichnung bzw. Name der Organisation der den Metadatensatz veröffentlicht.', 'Land Tirol'),
                   ('geographic_toponym', 'Geographische Abdeckung/Lage', 'extras:geographic_toponym', 'show', u'Geographische Ortsidentifikation eines Datensatzes, Dienstes oder Dokuments ', 'Linz'),
                   ('geographic_bbox', 'Geographische Ausdehnung', 'extras:geographic_bbox', 'show',u'Dokumentation der geographischen Ausdehnung eines Datensatzes, Dienstes oder Dokuments mit der Definition eines umrahmenden Rechtecks.','POLYGON ((-180.00 -90.00,180.00 -90.00,180.00 90.00, -180.00 90.00, -180.00 -90.00)) '),
                   ('end_datetime', 'Zeitliche Ausdehnung (Ende)', 'extras:end_datetime', 'show', u'Ende der Gültigkeit eines Datensatzes, Dienstes oder Dokuments.', '2009-11-23T20:36:00'),
                   ('update_frequency', 'Aktualisierungszyklus', 'extras:update_frequency', 'show', u'Menschenlesbare Frequenz der Aktualisierung des Datensatzes, Dienstes bzw. Dokuments. ', 'monatlich'),
                   ('lineage_quality', u'Datenqualität/Herkunft ', 'extras:lineage_quality', 'show',u'Menschenlesbare Beschreibung der Qualitäts- und oder Entstehungsgenese des Datensatzes oder Dienstes. zB die Methode der Erhebung', u'Der Datensatz wurde basierend auf der ÖK50, Stand 2011 digitalisiert. Es wurden alle Waldbestände für die Gemeinde Kopfing erfasst. '),
                   ('en_title_and_desc', 'Titel und Beschreibung Englisch ', 'extras:en_title_and_desc', 'show', u'Englische Angabe von Titel und Beschreibung des Datensatzes, Dienstes oder Dokuments', 'Population of Vienna 2010. Contains the population of permanent residents of Vienna and it’s districts as a moving average in the census period 1st January 2010 to 31st December 2012 '),
                   ('resource_size', u'Größe des Datensatzes, Dienstes oder Dokuments', 'resources:size', 'show', u'Dateigröße.', '899652'),
                   ('license_citation', 'Lizenz Zitat', 'extras:license_citation', 'show',u'Die richtige Namensnennung (CC-BY) der Datenquelle laut den Nutzungsbedingungen des jeweiligen Datenportals. Entspricht dem Feld "Datenquelle" von OGD-Metadaten – 1.1. ', u'Datenquelle: CC-BY-3.0: Stadt Linz - data.linz.gv.at'),
                   ('resource_language', 'Sprache des Datensatzes, Dienstes oder Dokuments', 'resources:language', 'show', u'ISO 639-2 dreistelliger ISO Sprachcode für den Datensatz, Dienst oder das Dokument ', 'ger'),
                   ('resource_encoding', 'Character Set Code des Datensatzes, Dienstes oder Dokuments', 'resources:characterset', 'show', u'Characterset Code des Datensatzes oder Dienstes nach ISO 19115:2003', 'utf8'),
                   ('metadata_original_portal', u'Link zu den ursprünglichen Metadaten', 'extras:metadata_original_portal', 'show', u'Link auf das originale Metadatenblatt. ', 'Link auf das originale Metadatenblatt. '),
                   ('maintainer_email', 'Datenverantwortliche Stelle – E-Mailkontakt', 'maintainer_email', 'show', u'E-Mail Kontaktadresse der für den Datensatz, den Dienst oder das Dokument zuständigen Organisation bzw. Person', 'poststelle.magistratsabteilung33@wien.gv.at'),               
                  ]