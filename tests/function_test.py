import unittest
from ivod.origin import ivod_downloader as origin_ivod_downloader
from ivod.origin import ivod_single_downloader as origin_ivod_single_downloader

import ivod_downloader
import ivod_single_downloader


class TestVODResults(unittest.TestCase):

    def test_get_movie_by_date(self):
        origin = origin_ivod_downloader.get_movie_by_date(8, '2014-10-09')
        current = ivod_downloader.get_movie_by_date(8, '2014-10-09')

        self.assertTrue(current)
        self.assertEqual(origin, current)

    def test_get_date_list(self):
        origin = origin_ivod_downloader.get_date_list(
            8,
            '2014-03-01',
            '2014-10-01')
        current = ivod_downloader.get_date_list(8, '2014-03-01', '2014-10-01')

        self.assertTrue(current)
        self.assertEqual(origin, current)

    def test_get_movie_by_date(self):
        origin = origin_ivod_downloader.get_movie_by_date(8, '2014-10-01')
        current = ivod_downloader.get_movie_by_date(8, '2014-10-01')

        self.assertTrue(current)
        self.assertEqual(origin, current)

    def test_get_movie_url(self):
        origin = origin_ivod_downloader.get_movie_url('74035', 'clip')
        current = ivod_downloader.get_movie_url('74035', 'clip')

        self.assertTrue(current)
        self.assertEqual(origin, current)


class TestVODSingleResults(unittest.TestCase):

    def setUp(self):
        self.download_url_args = []

    def _mock_adobe_hds_downloader(self, manifest, filename):
        self.download_url_args += [(manifest, filename)]

    def test_single_downloader(self):
        origin_ivod_single_downloader.download_adobe_hds = self._mock_adobe_hds_downloader
        ivod_single_downloader.download_adobe_hds = self._mock_adobe_hds_downloader

        origin_ivod_single_downloader.download_from_url(
            'http://ivod.ly.gov.tw/Play/VOD/76394/300K')
        ivod_single_downloader.download_from_url(
            'http://ivod.ly.gov.tw/Play/VOD/76394/300K')

        self.assertTrue(self.download_url_args[0])
        self.assertEqual(self.download_url_args[0], self.download_url_args[1])
