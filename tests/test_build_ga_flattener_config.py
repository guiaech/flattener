from tests.test_base import BaseUnitTest
from cfconfigbuilder.main import FlattenerDatasetConfig
from cfconfigbuilder.main import FlattenerDatasetConfigStorage
from cfconfigbuilderps.main import FlattenerDatasetConfig as FlattenerDatasetConfigPS
from cfconfigbuilderps.main import FlattenerDatasetConfigStorage as FlattenerDatasetConfigStoragePS


# TODO: question: what's the diff between these two unit tests?

class TestCFBuildFlattenerGaDatasetConfig(BaseUnitTest):

    def test_build_flattener_ga_dataset_config(self):
        # generate config and upload it to GCS
        config = FlattenerDatasetConfig()
        store = FlattenerDatasetConfigStorage()
        json_config = config.get_ga_datasets()
        json_config = config.add_intraday_info_into_config(json_config)
        store.upload_config(config=json_config)
        # check
        self.assertIsInstance(json_config, dict)
        if json_config.keys():
            for key, value in json_config.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, dict)
        self.assertTrue(True)

    def test_build_flattener_ga_dataset_config_add_intraday_schedule(self):
        # generate config and upload it to GCS
        config = FlattenerDatasetConfig()
        store = FlattenerDatasetConfigStorage()
        json_config = config.get_ga_datasets()
        json_config = config.add_intraday_info_into_config(json_config, intraday_schedule=15)
        store.upload_config(config=json_config)
        # check
        self.assertIsInstance(json_config, dict)
        if json_config.keys():
            for key, value in json_config.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, dict)
        self.assertTrue(True)

    def test_build_flattener_ga_dataset_config_ps(self):
        # generate config and upload it to GCS
        config = FlattenerDatasetConfigPS()
        store = FlattenerDatasetConfigStoragePS()
        json_config = config.get_ga_datasets()
        json_config = config.add_intraday_info_into_config(json_config)
        store.upload_config(config=json_config)
        # check
        self.assertIsInstance(json_config, dict)
        if json_config.keys():
            for key, value in json_config.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, dict)
        self.assertTrue(True)
