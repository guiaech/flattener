from tests.test_base import BaseUnitTest
import json
from tests.test_base import Context
import base64
from datetime import datetime
from pytz import timezone
from cfintraday.main import manage_intraday_schedule
import google.cloud.logging


class TestManageIntradayFlatteningSchedule(BaseUnitTest):
    c = Context()
    project_id = c.env["project"]
    project_number = c.env["project_number"]
    dataset_id = BaseUnitTest.DATASET

    now = datetime.now(timezone("America/Denver"))
    today = now.date()
    date_shard = today.strftime("%Y%m%d")

    table_type = "events_intraday"

    SAMPLE_LOG_INTRADAY_TABLE_CREATED = {
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "status": {},
            "authenticationInfo": {
                "principalEmail": "firebase-measurement@system.gserviceaccount.com"
            },
            "requestMetadata": {
                "requestAttributes": {},
                "destinationAttributes": {}
            },
            "serviceName": "bigquery.googleapis.com",
            "methodName": "tableservice.insert",
            "authorizationInfo": [
                {
                    "resource": f"projects/{project_id}/datasets/{dataset_id}",
                    "permission": "bigquery.tables.create",
                    "granted": True,
                    "resourceAttributes": {}
                }
            ],
            "resourceName": f"projects/{project_number}/datasets/{dataset_id}/tables",
            "serviceData": {
                "@type": "type.googleapis.com/google.cloud.bigquery.logging.v1.AuditData",
                "tableInsertRequest": {
                    "resource": {
                        "tableName": {
                            "projectId": project_number,
                            "datasetId": dataset_id,
                            "tableId": f"{table_type}_{date_shard}"
                        },
                        "info": {},
                        "view": {},
                        "schemaJson": "{\n  \"fields\": [{\n    \"name\": \"event_date\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_timestamp\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_name\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_params\",\n    \"type\": \"RECORD\",\n    \"mode\": \"REPEATED\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"key\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"value\",\n        \"type\": \"RECORD\",\n        \"mode\": \"NULLABLE\",\n        \"schema\": {\n          \"fields\": [{\n            \"name\": \"string_value\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"int_value\",\n            \"type\": \"INTEGER\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"float_value\",\n            \"type\": \"FLOAT\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"double_value\",\n            \"type\": \"FLOAT\",\n            \"mode\": \"NULLABLE\"\n          }]\n        }\n      }]\n    }\n  }, {\n    \"name\": \"event_previous_timestamp\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_value_in_usd\",\n    \"type\": \"FLOAT\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_bundle_sequence_id\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_server_timestamp_offset\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"user_id\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"user_pseudo_id\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"privacy_info\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"analytics_storage\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"ads_storage\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"uses_transient_token\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"user_properties\",\n    \"type\": \"RECORD\",\n    \"mode\": \"REPEATED\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"key\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"value\",\n        \"type\": \"RECORD\",\n        \"mode\": \"NULLABLE\",\n        \"schema\": {\n          \"fields\": [{\n            \"name\": \"string_value\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"int_value\",\n            \"type\": \"INTEGER\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"float_value\",\n            \"type\": \"FLOAT\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"double_value\",\n            \"type\": \"FLOAT\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"set_timestamp_micros\",\n            \"type\": \"INTEGER\",\n            \"mode\": \"NULLABLE\"\n          }]\n        }\n      }]\n    }\n  }, {\n    \"name\": \"user_first_touch_timestamp\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"user_ltv\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"revenue\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"currency\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"device\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"category\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"mobile_brand_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"mobile_model_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"mobile_marketing_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"mobile_os_hardware_model\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"operating_system\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"operating_system_version\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"vendor_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"advertising_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"language\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"is_limited_ad_tracking\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"time_zone_offset_seconds\",\n        \"type\": \"INTEGER\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"browser\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"browser_version\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"web_info\",\n        \"type\": \"RECORD\",\n        \"mode\": \"NULLABLE\",\n        \"schema\": {\n          \"fields\": [{\n            \"name\": \"browser\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"browser_version\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"hostname\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }]\n        }\n      }]\n    }\n  }, {\n    \"name\": \"geo\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"continent\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"country\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"region\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"city\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"sub_continent\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"metro\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"app_info\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"version\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"install_store\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"firebase_app_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"install_source\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"traffic_source\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"medium\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"source\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"stream_id\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"platform\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_dimensions\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"hostname\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"ecommerce\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"total_item_quantity\",\n        \"type\": \"INTEGER\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"purchase_revenue_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"purchase_revenue\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"refund_value_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"refund_value\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"shipping_value_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"shipping_value\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"tax_value_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"tax_value\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"unique_items\",\n        \"type\": \"INTEGER\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"transaction_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"items\",\n    \"type\": \"RECORD\",\n    \"mode\": \"REPEATED\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"item_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_brand\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_variant\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category2\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category3\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category4\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category5\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"price_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"price\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"quantity\",\n        \"type\": \"INTEGER\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_revenue_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_revenue\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_refund_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_refund\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"coupon\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"affiliation\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"location_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_list_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_list_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_list_index\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"promotion_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"promotion_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"creative_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"creative_slot\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }]\n}"
                    }
                },
                "tableInsertResponse": {
                    "resource": {
                        "tableName": {
                            "projectId": project_id,
                            "datasetId": dataset_id,
                            "tableId": f"{table_type}_{date_shard}"
                        },
                        "info": {},
                        "view": {},
                        "createTime": "2021-10-11T07:00:17.787Z",
                        "schemaJson": "{\n  \"fields\": [{\n    \"name\": \"event_date\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_timestamp\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_name\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_params\",\n    \"type\": \"RECORD\",\n    \"mode\": \"REPEATED\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"key\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"value\",\n        \"type\": \"RECORD\",\n        \"mode\": \"NULLABLE\",\n        \"schema\": {\n          \"fields\": [{\n            \"name\": \"string_value\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"int_value\",\n            \"type\": \"INTEGER\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"float_value\",\n            \"type\": \"FLOAT\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"double_value\",\n            \"type\": \"FLOAT\",\n            \"mode\": \"NULLABLE\"\n          }]\n        }\n      }]\n    }\n  }, {\n    \"name\": \"event_previous_timestamp\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_value_in_usd\",\n    \"type\": \"FLOAT\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_bundle_sequence_id\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_server_timestamp_offset\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"user_id\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"user_pseudo_id\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"privacy_info\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"analytics_storage\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"ads_storage\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"uses_transient_token\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"user_properties\",\n    \"type\": \"RECORD\",\n    \"mode\": \"REPEATED\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"key\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"value\",\n        \"type\": \"RECORD\",\n        \"mode\": \"NULLABLE\",\n        \"schema\": {\n          \"fields\": [{\n            \"name\": \"string_value\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"int_value\",\n            \"type\": \"INTEGER\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"float_value\",\n            \"type\": \"FLOAT\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"double_value\",\n            \"type\": \"FLOAT\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"set_timestamp_micros\",\n            \"type\": \"INTEGER\",\n            \"mode\": \"NULLABLE\"\n          }]\n        }\n      }]\n    }\n  }, {\n    \"name\": \"user_first_touch_timestamp\",\n    \"type\": \"INTEGER\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"user_ltv\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"revenue\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"currency\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"device\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"category\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"mobile_brand_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"mobile_model_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"mobile_marketing_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"mobile_os_hardware_model\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"operating_system\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"operating_system_version\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"vendor_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"advertising_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"language\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"is_limited_ad_tracking\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"time_zone_offset_seconds\",\n        \"type\": \"INTEGER\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"browser\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"browser_version\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"web_info\",\n        \"type\": \"RECORD\",\n        \"mode\": \"NULLABLE\",\n        \"schema\": {\n          \"fields\": [{\n            \"name\": \"browser\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"browser_version\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }, {\n            \"name\": \"hostname\",\n            \"type\": \"STRING\",\n            \"mode\": \"NULLABLE\"\n          }]\n        }\n      }]\n    }\n  }, {\n    \"name\": \"geo\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"continent\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"country\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"region\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"city\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"sub_continent\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"metro\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"app_info\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"version\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"install_store\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"firebase_app_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"install_source\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"traffic_source\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"medium\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"source\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"stream_id\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"platform\",\n    \"type\": \"STRING\",\n    \"mode\": \"NULLABLE\"\n  }, {\n    \"name\": \"event_dimensions\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"hostname\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"ecommerce\",\n    \"type\": \"RECORD\",\n    \"mode\": \"NULLABLE\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"total_item_quantity\",\n        \"type\": \"INTEGER\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"purchase_revenue_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"purchase_revenue\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"refund_value_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"refund_value\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"shipping_value_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"shipping_value\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"tax_value_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"tax_value\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"unique_items\",\n        \"type\": \"INTEGER\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"transaction_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }, {\n    \"name\": \"items\",\n    \"type\": \"RECORD\",\n    \"mode\": \"REPEATED\",\n    \"schema\": {\n      \"fields\": [{\n        \"name\": \"item_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_brand\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_variant\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category2\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category3\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category4\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_category5\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"price_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"price\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"quantity\",\n        \"type\": \"INTEGER\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_revenue_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_revenue\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_refund_in_usd\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_refund\",\n        \"type\": \"FLOAT\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"coupon\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"affiliation\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"location_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_list_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_list_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"item_list_index\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"promotion_id\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"promotion_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"creative_name\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }, {\n        \"name\": \"creative_slot\",\n        \"type\": \"STRING\",\n        \"mode\": \"NULLABLE\"\n      }]\n    }\n  }]\n}",
                        "updateTime": "2021-10-11T07:00:17.844Z"
                    }
                }
            }
        },
        "insertId": "-gms7aed23p8",
        "resource": {
            "type": "bigquery_resource",
            "labels": {
                "project_id": project_id
            }
        },
        "timestamp": "2021-10-11T07:00:17.888767Z",
        "severity": "NOTICE",
        "logName": f"projects/{project_id}/logs/cloudaudit.googleapis.com%2Factivity",
        "receiveTimestamp": "2021-10-11T07:00:17.901039177Z"
    }

    SAMPLE_LOAD_DATA_INTRADAY_TABLE_DELETED = {
        "protoPayload": {
            "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
            "status": {},
            "authenticationInfo": {
                "principalEmail": "firebase-measurement@system.gserviceaccount.com"
            },
            "requestMetadata": {
                "requestAttributes": {},
                "destinationAttributes": {}
            },
            "serviceName": "bigquery.googleapis.com",
            "methodName": "tableservice.delete",
            "authorizationInfo": [
                {
                    "resource": f"projects/{project_id}/datasets/{dataset_id}/tables/events_intraday_{date_shard}",
                    "permission": "bigquery.tables.delete",
                    "granted": True,
                    "resourceAttributes": {}
                }
            ],
            "resourceName": f"projects/{project_number}/datasets/{dataset_id}/tables/{table_type}_{date_shard}"
        },
        "insertId": "-ef5jvyd24ld",
        "resource": {
            "type": "bigquery_resource",
            "labels": {
                "project_id": project_id
            }
        },
        "timestamp": "2021-10-11T16:55:00.193897Z",
        "severity": "NOTICE",
        "logName": f"projects/{project_id}/logs/cloudaudit.googleapis.com%2Factivity",
        "receiveTimestamp": "2021-10-11T16:55:00.433230860Z"
    }

    def test_create_intraday_flattening_schedule(self):
        # This message is what is configured in the

        SAMPLE_PUBSUB_MESSAGE = {'@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage', 'attributes':
            {'origin': 'python-unit-test', 'username': 'gcp'}
            , 'data': base64.b64encode(json.dumps(self.SAMPLE_LOG_INTRADAY_TABLE_CREATED).encode('utf-8'))}
        manage_intraday_schedule(SAMPLE_PUBSUB_MESSAGE)

        self.assertTrue(True)

    def test_delete_intraday_flattening_schedule(self):
        SAMPLE_PUBSUB_MESSAGE = {'@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage', 'attributes':
            {'origin': 'python-unit-test', 'username': 'gcp'}
            , 'data': base64.b64encode(json.dumps(self.SAMPLE_LOAD_DATA_INTRADAY_TABLE_DELETED).encode('utf-8'))}
        manage_intraday_schedule(SAMPLE_PUBSUB_MESSAGE)
        self.assertTrue(True)
        self.assertTrue(True)

    def test_create_intraday_flattening_schedule_trigger_with_log(self):
        # https://medium.com/google-cloud/python-and-stackdriver-logging-2ade460c90e3
        client = google.cloud.logging.Client()
        logger = client.logger('unit_test')
        logger.log_text('unit test starts')
        # logger.log_proto(json.dumps(self.SAMPLE_LOG_INTRADAY_TABLE_CREATED)) # not working , empty log
        # logger.log_proto(self.SAMPLE_LOG_INTRADAY_TABLE_CREATED) #not working google.protobuf.json_format.ParseError: @type is missing when parsing any message.
        logger.log_struct(self.SAMPLE_LOG_INTRADAY_TABLE_CREATED) # most promising test
        # logger.log_text(json.dumps(self.SAMPLE_LOG_INTRADAY_TABLE_CREATED)) # not formatted correctly
        logger.log_text('unit test ends')
