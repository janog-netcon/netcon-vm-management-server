class instances_list_response:
    def __init__(self, id, name, status, external_ip):
        self.id = id
        self.name = name
        self.status = status
        self.external_ip = external_ip
        
    def toObject(self):
        return {
            "request_id": self.id,
            "name": self.name,
            "status": self.status,
            "external_ip": self.external_ip
        }