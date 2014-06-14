# -*- coding: utf-8 -*- 

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.validators import (ignore_missing,
                                      keep_extras,
                                      not_empty,
                                      empty,
                                      ignore,
                                      if_empty_same_as,
                                      not_missing,
                                      ignore_empty
                                     )
import ckanext.odpat_form.lib.dgvat_helper as dgvat_helper

import logging


log = logging.getLogger(__name__)


class OdpatDatasetFormPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''opendataportal Dataset Form.

    '''
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config):

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, 'public')

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')

    def before_map(self, map):
        log.fatal('before map')
        map.connect('/dataset/new', controller='ckanext.odpat_form.controllers.odpat:OdpatPackageController', action='new')
        map.connect('/dataset/edit/{id}', controller='ckanext.odpat_form.controllers.odpat:OdpatPackageController', action='edit')
        map.connect('/dataset/{id}.{format}', controller='ckanext.odpat_form.controllers.odpat:OdpatPackageController', action='read')
        map.connect('/dataset/{id}', controller='ckanext.odpat_form.controllers.odpat:OdpatPackageController', action='read')
        return map

    def after_map(self, map):
        log.fatal('after map')
        return map

    def get_helpers(self):
        log.fatal('get Helpers')
        return { 'categories': dgvat_helper.categorization, 
                 'frequencies': dgvat_helper.update_frequency,  
                 'get_basic_metadata_fields': dgvat_helper.get_basic_metadata_fields,
                 'get_extended_metadata_fields': dgvat_helper.get_extended_metadata_fields,
                 'get_resource_metadata_fields': dgvat_helper.get_resource_metadata_fields,
                 'get_extras_element': dgvat_helper.get_extras_element,
                 'get_extras_from_basic': dgvat_helper.get_extras_from_basic,
                 'get_label_by_field': dgvat_helper.get_label_by_field,
                 'get_cat_by_id': dgvat_helper.get_categorization_by_id,
                }

    def _modify_package_schema(self, schema):
        schema.update({
            'schema_name': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'maintainer_link': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'schema_language': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'schema_characterset': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'date_released': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'begin_datetime': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'end_datetime': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'metadata_linkage': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'attribute_description': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'publisher': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'geographic_toponym': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'geographic_bbox': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'lineage_quality': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'en_title_and_desc': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'license_citation':[toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'metadata_identifier':[toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'metadata_modified':[toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'date_updated':[toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'publishing_date':[toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'publishing_state':[toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'log_message': [toolkit.get_validator('ignore_missing')],
            'update_frequency': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'categorization': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')]
        })

        schema['resources'].update({
                    'language':[toolkit.get_validator('ignore_missing')],
                    'characterset':[toolkit.get_validator('ignore_missing')],
                })
        return schema

    def create_package_schema(self):
        schema = super(OdpatDatasetFormPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(OdpatDatasetFormPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(OdpatDatasetFormPlugin, self).show_package_schema()
        schema['resources'].update({
                    'language':[toolkit.get_validator('ignore_missing')],
                    'characterset':[toolkit.get_validator('ignore_missing')],
                })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
