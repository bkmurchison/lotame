from typing import Any, Dict, List
from unittest.mock import patch, call

import lotame
import pytest

from lotame.credentials import Credentials
from lotame.services.firehose import FirehoseService


@patch('lotame.services.firehose.Api')
def test_firehose_service_init_with_api_arg(mock_api):
    svc = FirehoseService(mock_api)
    svc.api == mock_api


@patch('lotame.services.firehose.Api')
def test_firehose_service_init_default_arg(mock_api):
    svc = FirehoseService()
    svc.api = mock_api


@pytest.fixture
def firehose_feeds_url() -> str:
    return Credentials.DEFAULT_BASE_URL + FirehoseService.FIREHOSE_FEEDS


@pytest.fixture
def feed_id_245() -> int:
    return 245


@pytest.fixture
def feed_id_246() -> int:
    return 246


@pytest.fixture
def firehose_feed_245(feed_id_245) -> Dict[str, Any]:
    return {"id": feed_id_245,
            "clientId": 2987,
            "type": "3pd",
            "profileType": "cookie",
            "metadataFile": "http://domain/path/to/file"
            }


@pytest.fixture
def firehose_feed_246(feed_id_246) -> Dict[str, Any]:
    return {"id": feed_id_246,
            "clientId": 2987,
            "type": "client",
            "profileType": "mobile",
            "metadataFile": "http://domain/path/to/file"
            }


@pytest.fixture
def firehose_feed_data(firehose_feed_245, firehose_feed_246) -> List[Dict[str, Any]]:
    return [firehose_feed_245, firehose_feed_246]


@pytest.fixture
def firehose_feeds_resp(firehose_feed_data) -> Dict[str, Any]:
    return {"feeds": firehose_feed_data}


@patch.object(lotame.utils, 'build_url')
@patch('lotame.services.firehose.Api')
def test_get_feeds(mock_api,
                   mock_build_url,
                   firehose_feeds_url,
                   firehose_feeds_resp,
                   firehose_feed_data):
    mock_build_url.return_value = firehose_feeds_url
    mock_api.get.return_value = firehose_feeds_resp

    svc = FirehoseService(mock_api)
    rsp = svc.get_feeds()
    assert rsp == firehose_feed_data


@pytest.fixture
def feeds_update_data_245_empty(feed_id_245) -> Dict[str, Any]:
    return {'files': [],
            'id': feed_id_245,
            'metaDataFile': 'http://domain/path/to/file'
            }


@pytest.fixture
def feeds_update_data_245(feed_id_245) -> Dict[str, Any]:
    return {'files': ['d95dff17-5932-4aa5-9ad5-584871e267a8.gz',
                      '009fda44-f681-4bed-8951-3bd0e08b5f6c.gz',
                      '9c5a66b5-a2a3-4841-8b75-bfd4f085553d.gz',
                      ],
            'id': feed_id_245,
            'location': 's3://lotame-firehose/1234/na/cookie',
            'metaDataFile': 'http://domain/path/to/file'
            }


@pytest.fixture
def s3_creds() -> Dict[str, Any]:
    return {'secretAccessKey': 'blah',
            'sessionToken': 'blah',
            'expiration': 9999999999999,
            'accessKeyId': 'blah'
            }


@pytest.fixture
def firehose_feeds_update_param_245(feed_id_245) -> Dict[str, Any]:
    return {FirehoseService.FEED_ID: feed_id_245}


@pytest.fixture
def firehose_feeds_update_data_245_empty(feeds_update_data_245_empty,
                                         s3_creds) -> Dict[str, Any]:
    return {'feeds': [feeds_update_data_245_empty], 's3creds': s3_creds}


@pytest.fixture
def firehose_feeds_update_data_245(feeds_update_data_245, s3_creds) -> Dict[str, Any]:
    return {'feeds': [feeds_update_data_245], 's3creds': s3_creds}


@pytest.fixture
def firehose_feeds_update_param_246(feed_id_246) -> Dict[str, Any]:
    return {FirehoseService.FEED_ID: feed_id_246}


@pytest.fixture
def feeds_update_data_246_empty(feed_id_246) -> Dict[str, Any]:
    return {'files': [],
            'id': feed_id_246,
            'metaDataFile': 'http://domain/path/to/file'
            }


@pytest.fixture
def feeds_update_data_246(feed_id_246) -> Dict[str, Any]:
    return {'files': ['d95dff17-5932-4aa5-9ad5-584871e267a8.gz',
                      '009fda44-f681-4bed-8951-3bd0e08b5f6c.gz',
                      '9c5a66b5-a2a3-4841-8b75-bfd4f085553d.gz',
                      ],
            'id': feed_id_246,
            'location': 's3://lotame-firehose/1234/na/cookie',
            'metaDataFile': 'http://domain/path/to/file'
            }


@pytest.fixture
def firehose_feeds_update_data_246_empty(feeds_update_data_246_empty,
                                         s3_creds) -> Dict[str, Any]:
    return {'feeds': [feeds_update_data_246_empty], 's3creds': s3_creds}


@pytest.fixture
def firehose_feeds_update_data_246(
        feeds_update_data_246, s3_creds
) -> Dict[str, Any]:
    return {'feeds': [feeds_update_data_246], 's3creds': s3_creds}


@pytest.fixture
def firehose_feeds_update_data_empty(
        firehose_feeds_update_data_245_empty,
        firehose_feeds_update_data_246_empty) -> List[Dict[str, Any]]:
    return [firehose_feeds_update_data_245_empty,
            firehose_feeds_update_data_246_empty]


@pytest.fixture
def firehose_feeds_update_data_partial_empty(
        firehose_feeds_update_data_245,
        firehose_feeds_update_data_246_empty) -> List[Dict[str, Any]]:
    return [firehose_feeds_update_data_245,
            firehose_feeds_update_data_246_empty]


@pytest.fixture
def firehose_feeds_update_data(
        firehose_feeds_update_data_245,
        firehose_feeds_update_data_246) -> List[Dict[str, Any]]:
    return [firehose_feeds_update_data_245, firehose_feeds_update_data_246]


@pytest.fixture
def firehose_feeds_updates_url() -> str:
    return Credentials.DEFAULT_BASE_URL + FirehoseService.FIREHOSE_UPDATES


@pytest.fixture
def firehose_feeds_updates_url_245(firehose_feeds_updates_url, feed_id_245) -> str:
    return firehose_feeds_updates_url + f"?{FirehoseService.FEED_ID}={feed_id_245}"


@pytest.fixture
def firehose_feeds_updates_url_246(firehose_feeds_updates_url, feed_id_246) -> str:
    return firehose_feeds_updates_url + f"?{FirehoseService.FEED_ID}={feed_id_246}"


@patch.object(lotame.utils, 'build_url')
@patch('lotame.services.firehose.Api')
def test_get_updates_for_feed_id(mock_api,
                                 mock_build_url,
                                 feed_id_246,
                                 firehose_feeds_updates_url_246,
                                 firehose_feeds_update_data_246):
    mock_build_url.return_value = firehose_feeds_updates_url_246
    mock_api.get.return_value = firehose_feeds_update_data_246

    svc = FirehoseService(mock_api)
    rsp = svc.get_updates_for_feed(feed_id=feed_id_246)

    get_calls = [call(firehose_feeds_updates_url_246)]
    assert mock_api.get.has_calls(get_calls)
    assert rsp == firehose_feeds_update_data_246


@patch.object(lotame.utils, 'build_url')
@patch('lotame.services.firehose.Api')
def test_get_updates_for_feed_id_empy_data(mock_api,
                                           mock_build_url,
                                           feed_id_245,
                                           firehose_feeds_updates_url_245,
                                           feeds_update_data_245_empty):
    mock_build_url.return_value = firehose_feeds_updates_url_245
    mock_api.get.return_value = firehose_feeds_update_data_245

    svc = FirehoseService(mock_api)
    rsp = svc.get_updates_for_feed(feed_id=feed_id_245)

    get_calls = [call(firehose_feeds_updates_url_245)]
    assert mock_api.get.has_calls(get_calls)
    assert rsp == firehose_feeds_update_data_245


@patch('lotame.services.firehose.Api')
def test_get_updates_for_all_feeds(mock_api,
                                   feed_id_245,
                                   feed_id_246,
                                   firehose_feed_245,
                                   firehose_feed_246,
                                   firehose_feeds_updates_url,
                                   firehose_feeds_updates_url_245,
                                   firehose_feeds_updates_url_246,
                                   firehose_feeds_update_data,
                                   firehose_feeds_update_data_245,
                                   firehose_feeds_update_data_246):
    mock_api.get.side_effect = [firehose_feeds_update_data_245,
                                firehose_feeds_update_data_246]

    svc = FirehoseService(mock_api)
    rsp = svc.get_updates_for_feeds(feeds=[firehose_feed_245, firehose_feed_246])

    # calling anyOrder=False to be explicit that the calls MUST have occurred in the
    # order specified in the calls array
    get_calls = [call(firehose_feeds_updates_url_245),
                 call(firehose_feeds_updates_url_246)]
    assert mock_api.get.has_calls(get_calls, any_order=False)
    assert rsp == firehose_feeds_update_data


@patch.object(lotame.utils, 'build_url')
@patch('lotame.services.firehose.Api')
def test_get_updates_with_defaulted_args(mock_api,
                                         mock_build_url,
                                         firehose_feeds_url,
                                         firehose_feeds_updates_url_245,
                                         firehose_feeds_updates_url_246,
                                         firehose_feeds_update_param_245,
                                         firehose_feeds_update_param_246,
                                         firehose_feeds_resp,
                                         firehose_feeds_update_data,
                                         firehose_feeds_update_data_245,
                                         firehose_feeds_update_data_246):
    mock_build_url.side_effect = [firehose_feeds_url,
                                  firehose_feeds_updates_url_245,
                                  firehose_feeds_updates_url_246]
    mock_api.get.side_effect = [firehose_feeds_resp,
                                firehose_feeds_update_data_245,
                                firehose_feeds_update_data_246]
    svc = FirehoseService(mock_api)
    rsp = svc.get_updates()

    build_url_calls = [call(FirehoseService.FIREHOSE_FEEDS, {}),
                       call(FirehoseService.FIREHOSE_UPDATES, firehose_feeds_update_param_245),
                       call(FirehoseService.FIREHOSE_UPDATES, firehose_feeds_update_param_246)]
    assert mock_build_url.hasCalls(build_url_calls, any_order=False)

    get_calls = [call(firehose_feeds_url),
                 call(firehose_feeds_updates_url_245),
                 call(firehose_feeds_updates_url_246)]
    assert mock_api.get.hasCalls(get_calls, any_order=False)

    assert rsp == firehose_feeds_update_data


@patch.object(lotame.utils, 'build_url')
@patch('lotame.services.firehose.Api')
def test_get_updates_with_defaulted_args_no_data(mock_api,
                                                 mock_build_url,
                                                 firehose_feeds_url,
                                                 firehose_feeds_updates_url_245,
                                                 firehose_feeds_updates_url_246,
                                                 firehose_feeds_update_param_245,
                                                 firehose_feeds_update_param_246,
                                                 firehose_feeds_resp,
                                                 firehose_feeds_update_data_empty,
                                                 firehose_feeds_update_data_245_empty,
                                                 firehose_feeds_update_data_246_empty):
    mock_build_url.side_effect = [firehose_feeds_url,
                                  firehose_feeds_updates_url_245,
                                  firehose_feeds_updates_url_246]
    mock_api.get.side_effect = [firehose_feeds_resp,
                                firehose_feeds_update_data_245_empty,
                                firehose_feeds_update_data_246_empty]
    svc = FirehoseService(mock_api)
    rsp = svc.get_updates()

    build_url_calls = [call(FirehoseService.FIREHOSE_FEEDS, {}),
                       call(FirehoseService.FIREHOSE_UPDATES, firehose_feeds_update_param_245),
                       call(FirehoseService.FIREHOSE_UPDATES, firehose_feeds_update_param_246)]
    assert mock_build_url.hasCalls(build_url_calls, any_order=False)

    get_calls = [call(firehose_feeds_url),
                 call(firehose_feeds_updates_url_245),
                 call(firehose_feeds_updates_url_246)]
    assert mock_api.get.hasCalls(get_calls, any_order=False)

    assert rsp == firehose_feeds_update_data_empty


@patch.object(lotame.utils, 'build_url')
@patch('lotame.services.firehose.Api')
def test_get_updates_with_defaulted_args_partial_data(mock_api,
                                                      mock_build_url,
                                                      firehose_feeds_url,
                                                      firehose_feeds_updates_url_245,
                                                      firehose_feeds_updates_url_246,
                                                      firehose_feeds_update_param_245,
                                                      firehose_feeds_update_param_246,
                                                      firehose_feeds_resp,
                                                      firehose_feeds_update_data_partial_empty,
                                                      firehose_feeds_update_data_245,
                                                      firehose_feeds_update_data_246_empty):
    mock_build_url.side_effect = [firehose_feeds_url,
                                  firehose_feeds_updates_url_245,
                                  firehose_feeds_updates_url_246]
    mock_api.get.side_effect = [firehose_feeds_resp,
                                firehose_feeds_update_data_245,
                                firehose_feeds_update_data_246_empty]
    svc = FirehoseService(mock_api)
    rsp = svc.get_updates()

    build_url_calls = [call(FirehoseService.FIREHOSE_FEEDS, {}),
                       call(FirehoseService.FIREHOSE_UPDATES, firehose_feeds_update_param_245),
                       call(FirehoseService.FIREHOSE_UPDATES, firehose_feeds_update_param_246)]
    assert mock_build_url.hasCalls(build_url_calls, any_order=False)

    get_calls = [call(firehose_feeds_url),
                 call(firehose_feeds_updates_url_245),
                 call(firehose_feeds_updates_url_246)]
    assert mock_api.get.hasCalls(get_calls, any_order=False)

    assert rsp == firehose_feeds_update_data_partial_empty
