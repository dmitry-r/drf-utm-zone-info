import subprocess

import os

from converters.gis_converter.helper.default_postgres import get_default_postgres_wrapper
from utils import changed_dir


def boostrap(pbf_file_path):
    with changed_dir(os.path.dirname(__file__)):
        bootstrapper = BootStrapper(pbf_file_path=pbf_file_path)
        bootstrapper.bootstrap()


class BootStrapper:
    def __init__(self, pbf_file_path, limit_ram_usage=True):
        self._pbf_file_path = pbf_file_path
        self._postgres = get_default_postgres_wrapper()
        self._limit_ram_usage = limit_ram_usage
        self._script_base_dir = os.path.abspath(os.path.dirname(__file__))
        self._terminal_style_path = os.path.join(self._script_base_dir, 'styles', 'terminal.style')
        self._style_path = os.path.join(self._script_base_dir, 'styles', 'style.lua')

    def bootstrap(self):
        self._reset_database()
        self._convert_osm_pbf_to_postgres()
        self._setup_db_functions()
        self._harmonize_database()
        self._filter_data()

    def _reset_database(self):
        self._postgres.drop_db()
        self._postgres.create_db()
        self._setup_db()

    def _setup_db(self):
        self._postgres.create_extension("hstore")
        self._postgres.create_extension("postgis")

    def _convert_osm_pbf_to_postgres(self):
        db_name = self._postgres.get_db_name()
        postgres_user = self._postgres.get_user()

        osm_2_pgsql_command = [
            'osm2pgsql',
            '--create',
            '--extra-attributes',
            '--database', db_name,
            '--prefix', 'osm',
            '--style', self._terminal_style_path,
            '--tag-transform-script', self._style_path,
            '--number-processes', '8',
            '--username', postgres_user,
            '--hstore-all',
            '--input-reader', 'pbf',
            self._pbf_file_path,
        ]

        if self._limit_ram_usage:
            insert_pos = osm_2_pgsql_command.index('--extra-attributes')
            osm_2_pgsql_command.insert(insert_pos, '--slim')

        subprocess.check_call(osm_2_pgsql_command)

    def _setup_db_functions(self):
        create_function_sql_path = os.path.join(self._script_base_dir, 'sql', 'create_functions.sql')
        self._postgres.execute_psql(sql_file_path=create_function_sql_path)

    def _harmonize_database(self):
        cleanup_sql_path = os.path.join(self._script_base_dir, 'sql', 'sweeping_data.sql')
        self._postgres.execute_psql(sql_file_path=cleanup_sql_path)

    def _filter_data(self):
        filter_sql_scripts_ordered = [
            'drop_and_recreate.sql',
            'address.sql',
            'adminarea_boundary.sql',
            'building.sql',
            'landuse.sql',
            'military.sql',
            'natural.sql',
            'nonop.sql',
            'geoname.sql',
            'pow.sql',
            'poi.sql',
            'misc.sql',
            'transport.sql',
            'railway.sql',
            'road.sql',
            'route.sql',
            'traffic.sql',
            'utility.sql',
            'water.sql',
            'create_view.sql',
        ]
        base_dir = os.path.join(self._script_base_dir, 'sql', 'filter')
        for filter_script in filter_sql_scripts_ordered:
            filter_script_path = os.path.join(base_dir, filter_script)
            self._postgres.execute_psql(sql_file_path=filter_script_path)
