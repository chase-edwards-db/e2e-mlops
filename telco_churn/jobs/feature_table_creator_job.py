import os

from telco_churn.common import Workload
from telco_churn.feature_table_creator import FeatureTableCreator
from telco_churn.utils.logger_utils import get_logger

_logger = get_logger()


class FeatureTableCreatorJob(Workload):

    def _get_data_ingest_params(self) -> dict:
        return self.conf['data_ingest_params']

    def _get_data_prep_params(self) -> dict:
        return self.conf['data_prep_params']

    def _get_feature_store_params(self) -> dict:
        return {'database_name': self.env_vars['feature_store_database_name'],
                'table_name': self.env_vars['feature_store_table_name'],
                'primary_keys': self.env_vars['feature_store_table_primary_keys'],
                'description': self.env_vars['feature_store_table_description']}

    def _get_labels_table_params(self) -> dict:
        return {'database_name': self.env_vars['labels_table_database_name'],
                'table_name': self.env_vars['labels_table_name'],
                'label_col': self.env_vars['labels_table_label_col'],
                'dbfs_path': self.env_vars['labels_table_dbfs_path']}

    def launch(self) -> None:
        """
        Launch FeatureStoreTableCreator job
        """
        _logger.info('Launching FeatureTableCreator job')
        _logger.info(f'Running feature-table-creation pipeline in {self.env_vars["DEPLOYMENT_ENV"]} environment')
        FeatureTableCreator(data_ingest_params=self._get_data_ingest_params(),
                            data_prep_params=self._get_data_prep_params(),
                            feature_store_params=self._get_feature_store_params(),
                            labels_table_params=self._get_labels_table_params()).run()
        _logger.info('FeatureTableCreator job finished!')


if __name__ == '__main__':
    job = FeatureTableCreatorJob()
    job.launch()
