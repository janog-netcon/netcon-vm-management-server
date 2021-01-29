import sys
import pytest
sys.path.append('.') # Run $ python path/to/test.py
from src.service import vm_management_service 
from src.client import gce_client, db_client
from src.nginx import nginx
from src.generator import string_generator
from src import config

machine_image_name = "problem-sc0"
problem_id = "74acef6e-395f-11eb-adc1-0242ac120002"
user_id = "j47-user"
get_random_string_with_symbol_response = "blah_123"
vm_create_instance_response = {
    "name": "problem-sc0-blah",
    "machine_image_name": "problem-sc0",
    "status": "STAGING"
}
get_random_string_response = "blah123"
proxy_domain_suffix = ".proxy.netcon.janog.gr.jp"
vm_get_instance_response = {
    "networkInterfaces": [
        {
            "accessConfigs": [
                {
                    "natIP": "10.210.53.123"
                }
            ]
        }
    ]
}
expected = {
    "response": {
        "instance_name": "problem-sc0-blah",
        "machine_image_name": "problem-sc0",
        "domain": "blah123.proxy.netcon.janog.gr.jp",
        "status": "STAGING",
        "problem_id": "74acef6e-395f-11eb-adc1-0242ac120002",
        "user_id": "j47-user",
        "password": "blah_123"
    }
}

@pytest.mark.parametrize(("get_random_string_with_symbol_response", "vm_create_instance_response", "get_random_string_response", "proxy_domain_suffix", "vm_get_instance_response", "expected"), [
    (get_random_string_with_symbol_response, vm_create_instance_response, get_random_string_response, proxy_domain_suffix, vm_get_instance_response, expected)
])
def test_create_instance(mocker, get_random_string_with_symbol_response, vm_create_instance_response, get_random_string_response, proxy_domain_suffix, vm_get_instance_response, expected):
    get_random_string_with_symbol = mocker.patch.object(string_generator, "get_random_string_with_symbol", return_value=get_random_string_with_symbol_response)
    create_instance = mocker.patch.object(gce_client, "create_instance", return_value=vm_create_instance_response)
    get_random_string = mocker.patch.object(string_generator, "get_random_string", return_value=get_random_string_response)
    get_proxy_domain_suffix = mocker.patch.object(config, "get_proxy_domain_suffix", return_value=proxy_domain_suffix)
    get_instance = mocker.patch.object(gce_client, "get_instance", return_value=vm_get_instance_response)
    add_domain = mocker.patch.object(nginx, "add_domain", return_value=None)
    post_problem_environments = mocker.patch.object(db_client, "post_problem_environments", return_value=None)

    actual = vm_management_service.create_instance(machine_image_name, problem_id)

    get_random_string_with_symbol.assert_called_once()
    create_instance.assert_called_once_with(machine_image_name, user_id, get_random_string_with_symbol_response)
    get_random_string.assert_called_once()
    get_proxy_domain_suffix.assert_called_once()
    get_instance.assert_called_once_with(vm_create_instance_response["name"])
    add_domain.assert_called_once_with(get_random_string_response + proxy_domain_suffix, [vm_get_instance_response["networkInterfaces"][0]["accessConfigs"][0]["natIP"]])
    post_problem_environments.assert_called()

    assert actual == expected

vm_get_instance_response = {
    "networkInterfaces": [
        {
            "accessConfigs": [
                {}
            ]
        }
    ]
}
expected = {
    "error": {
        "code": "500",
        "description": "Internal Server Error: The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
    }
}
@pytest.mark.parametrize(("get_random_string_with_symbol_response", "vm_create_instance_response", "get_random_string_response", "proxy_domain_suffix", "vm_get_instance_response", "expected"), [
    (get_random_string_with_symbol_response, vm_create_instance_response, get_random_string_response, proxy_domain_suffix, vm_get_instance_response, expected)
])
def test_create_instance_raises_external_ip(mocker, get_random_string_with_symbol_response, vm_create_instance_response, get_random_string_response, proxy_domain_suffix, vm_get_instance_response, expected):
    get_random_string_with_symbol = mocker.patch.object(string_generator, "get_random_string_with_symbol", return_value=get_random_string_with_symbol_response)
    create_instance = mocker.patch.object(gce_client, "create_instance", return_value=vm_create_instance_response)
    get_random_string = mocker.patch.object(string_generator, "get_random_string", return_value=get_random_string_response)
    get_proxy_domain_suffix = mocker.patch.object(config, "get_proxy_domain_suffix", return_value=proxy_domain_suffix)
    get_instance = mocker.patch.object(gce_client, "get_instance", return_value=vm_get_instance_response)
    delete_instance = mocker.patch.object(vm_management_service, "delete_instance")

    with pytest.raises(Exception) as excinfo:
        vm_management_service.create_instance(machine_image_name, problem_id)

    get_random_string_with_symbol.assert_called_once()
    create_instance.assert_called_once_with(machine_image_name, user_id, get_random_string_with_symbol_response)
    get_random_string.assert_called_once()
    get_proxy_domain_suffix.assert_called_once()
    get_instance.assert_called_with(vm_create_instance_response["name"])
    delete_instance.assert_called_once()

    assert "500" in str(excinfo.value)

if __name__ == '__main__':
    pytest.main(['-v', __file__])