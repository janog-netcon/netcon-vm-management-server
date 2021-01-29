def create_startup_script(user_id, password):
    address = "127.0.0.1"
    URL = "http://" + address + "/api"
    lab_name = "contest"

    startup_script  = '#! /bin/bash\n'
    startup_script += '/usr/sbin/useradd ' + user_id + ' -m -s /bin/bash -k /etc/skel/netcon-user\n'
    #startup_script += 'gpasswd -a ' + user_id + ' sudo\n'
    startup_script += 'echo "' + user_id + ':' + password + '" | chpasswd\n'
    # ssh config if necessary
    #startup_script += 'sudo sed -i "/^[^#]*PasswordAuthentication[[:space:]]no/c\PasswordAuthentication yes" /etc/ssh/sshd_config\n'
    #startup_script += 'sudo service sshd restart'
    startup_script += 'sleep 10s\n'
    startup_script += 'curl -s -b eve-ng_user.cookie -c eve-ng_user.cookie -X POST -d \'{"username":"j47-staff","password":"BLAH"}\' ' + URL + '/auth/login \n'

    ### login create user
    #startup_script += 'curl -s -b eve-ng_user.cookie -c eve-ng_user.cookie -X POST -d \'{"username":"' + user_id + '","password":"' + password + '"}\' ' + URL + '/auth/login \n'
    ### open lab as create user
    startup_script += 'curl -s -b eve-ng_user.cookie -c eve-ng_user.cookie -X GET -H \'Content-type: application/json\' ' + URL + '/labs/' + lab_name + '.unl/topology \n'
    ### vm on eve-ng boot as create user
    startup_script += 'curl -s -b eve-ng_user.cookie -c eve-ng_user.cookie -X GET -H \'Content-type: application/json\' ' + URL + '/labs/' + lab_name + '.unl/nodes/start \n'
    startup_script += 'rm eve-ng_user.cookie'

    return startup_script
