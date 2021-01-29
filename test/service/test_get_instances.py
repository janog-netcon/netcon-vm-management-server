import sys
import pytest
sys.path.append('.') # Run $ python path/to/test.py
from src.service import vm_management_service 
from src.client import gce_client, db_client 

get_problem_environments_response = [
    {
        "name": "instance_name",
        "machine_image_name": "machine_image_name",
        "host": "domain",
        "status": "RUNNING",
        "id": "problem_id",
        "user": "user_id",
        "password": "password"
    },
    {
        "name": "instance_name2",
        "machine_image_name": "machine_image_name2",
        "host": "domain2",
        "status": "STAGING",
        "id": "problem_id2",
        "user": "user_id2",
        "password": "password2"
    }    
]

expected = {
    "response": [
        {
            "instance_name": "instance_name",
            "machine_image_name": "machine_image_name",
            "domain": "domain",
            "status": "RUNNING",
            "problem_id": "problem_id",
            "user_id": "user_id",
            "password": "password"
        },
        {
            "instance_name": "instance_name2",
            "machine_image_name": "machine_image_name2",
            "domain": "domain2",
            "status": "STAGING",                
            "problem_id": "problem_id2",
            "user_id": "user_id2",
            "password": "password2"
        }
    ]
}

@pytest.mark.parametrize(("get_problem_environments_response", "expected"), [
    (get_problem_environments_response, expected)
])
def test_get_instances(mocker, get_problem_environments_response, expected):
    get_problem_environments = mocker.patch.object(db_client, "get_problem_environments", return_value=get_problem_environments_response)

    actual = vm_management_service.get_instances()

    get_problem_environments.assert_called_once()

    assert actual == expected

if __name__ == '__main__':
    pytest.main(['-v', __file__])