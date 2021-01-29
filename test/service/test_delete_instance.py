import sys
import pytest
sys.path.append('.') # Run $ python path/to/test.py
from src.service import vm_management_service 
from src.client import gce_client, db_client 
from src.nginx import nginx

get_problem_environments_by_name = [
    {
        "host": "domain"
    },
    {
        "host": "domain"
    }
]

expected = {
    "response": {
        "is_deleted": "true"
    }
}

@pytest.mark.parametrize(("get_problem_environments_by_name", "expected"), [
    (get_problem_environments_by_name, expected)
])
def test_delete_instance(mocker, get_problem_environments_by_name, expected):
    instance_name = "problem-sc0-blah"

    delete_problem_environments = mocker.patch.object(db_client, "delete_problem_environments", return_value=None)
    delete_instance = mocker.patch.object(gce_client, "delete_instance", return_value=None)
    get_problem_environments_by_name = mocker.patch.object(db_client, "get_problem_environments_by_name", return_value=get_problem_environments_by_name)
    remove_domain = mocker.patch.object(nginx, "remove_domain", return_value=None)

    actual = vm_management_service.delete_instance(instance_name)

    delete_problem_environments.assert_called_once_with(instance_name)
    delete_instance.assert_called_once_with(instance_name)
    get_problem_environments_by_name.assert_called_once_with(instance_name)
    remove_domain.assert_called_once()
    
    assert actual == expected

if __name__ == '__main__':
    pytest.main(['-v', __file__])