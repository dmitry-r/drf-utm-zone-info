from unittest.mock import patch

from django.test import TestCase

from converters.boundaries import BBox, PolyfileForCountry
from countries.models import Country
from tests.osm_test_helpers import POLYFILE_TEST_FILE_PATH


class TestBBox(TestCase):
    def test_init_when_parameters_are_missing_raises_type_error(self):
        self.assertRaises(TypeError, BBox, west=0, south=0, east=0)
        self.assertRaises(TypeError, BBox, west=0, south=0, north=0)
        self.assertRaises(TypeError, BBox, west=0, east=0, north=0)
        self.assertRaises(TypeError, BBox, south=0, east=0, north=0)
        self.assertRaises(TypeError, BBox, north=0)
        self.assertRaises(TypeError, BBox, east=0)
        self.assertRaises(TypeError, BBox, south=0)
        self.assertRaises(TypeError, BBox, west=0)

    def test_initializing_when_all_given_parameters_are_set_works(self):
        # shouldn't raise an error
        BBox(west=0, south=0, east=0, north=0)

    @patch.dict(
        'converters.converter_settings.OSMAXX_CONVERSION_SERVICE',
        PBF_PLANET_FILE_PATH='/path/to/planet-latest.osm.pbf',
    )
    @patch('subprocess.call', return_value=0)
    def test_cut_pbf_calls_osmconvert_correctly(self, sp_call_mock):
        # tests are using sample data from monaco
        bbox = BBox(west=1.23, south=-4.56, east=7.89, north=0.12)
        output_filename = 'outfile.pbf'
        bbox.cut_pbf(output_filename)
        sp_call_mock.assert_called_with(
            "osmconvert --out-pbf -o=outfile.pbf -b=1.23,-4.56,7.89,0.12 /path/to/planet-latest.osm.pbf".split(),
        )


class TestCountryPolyFile(TestCase):
    def test_init_when_parameters_are_missing_raises_type_error(self):
        self.assertRaises(TypeError, PolyfileForCountry)

    def test_initializing_when_all_given_parameters_are_set_works(self):
        poly_file_path = Country.objects.first().polyfile.path
        # shouldn't raise an error
        PolyfileForCountry(country_polyfile_path=poly_file_path)

    @patch.dict(
        'converters.converter_settings.OSMAXX_CONVERSION_SERVICE',
        PBF_PLANET_FILE_PATH='/path/to/planet-latest.osm.pbf',
    )
    @patch('subprocess.call', return_value=0)
    def test_cut_pbf_calls_osmconvert_correctly(self, sp_call_mock):
        # tests are using sample data from monaco
        poly_file_path = Country.objects.first().polyfile.path
        polyfile = PolyfileForCountry(country_polyfile_path=poly_file_path)
        output_filename = 'outfile.pbf'
        polyfile.cut_pbf(output_filename)
        sp_call_mock.assert_called_with(
            [
                "osmconvert",
                "--out-pbf",
                "-o=outfile.pbf",
                "-B={0}".format(POLYFILE_TEST_FILE_PATH),
                "/path/to/planet-latest.osm.pbf",
            ]
        )


# TODO: What if output filename contains spaces?
# TODO: What if path to planet file contains spaces?
