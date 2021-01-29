import sys
import pytest
sys.path.append('.') # Run $ python path/to/test.py
from src.service import vm_management_service 
from src.client import gce_client, db_client 
from src.nginx import nginx

instance_name = "problem-sc0-blah"

expected = {
    "response": {
        "is_rebooted": "true"
    }
}
@pytest.mark.parametrize(("expected"), [
    (expected)
])
def test_delete_instance(mocker, expected):
    stop_instance = mocker.patch.object(gce_client, "stop_instance", return_value=None)
    start_instance = mocker.patch.object(gce_client, "start_instance", return_value=None)

    actual = vm_management_service.reboot_instance(instance_name)

    stop_instance.assert_called_once_with(instance_name)
    start_instance.assert_called_once_with(instance_name)

    assert actual == expected

@pytest.mark.parametrize(("expected"), [
    (expected)
])
def test_delete_instance_raises(mocker, expected):
    stop_instance = mocker.patch.object(gce_client, "stop_instance", side_effect=SystemError)
    start_instance = mocker.patch.object(gce_client, "start_instance", return_value=None)

    actual = vm_management_service.reboot_instance(instance_name)
    
    stop_instance.assert_called_once_with(instance_name)
    start_instance.assert_called_once_with(instance_name)

    assert actual == expected

if __name__ == '__main__':
    pytest.main(['-v', __file__])