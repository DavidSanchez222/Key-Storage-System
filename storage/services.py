import csv, os

from storage.model import Container

class Service:
    
    def __init__(self, table_name):
        self.table_name = table_name

    
    def creating_container(self, page):
        with open(self.table_name, mode = 'a') as f:
            writer = csv.DictWriter(f, fieldnames = Container.schema())
            writer.writerow(page.to_dict())

    def list_containers(self):
        with open(self.table_name, mode = 'r') as f:
            reader = csv.DictReader(f, fieldnames = Container.schema())
            return list(reader)

    def update_container(self, updated_container):
        containers = self.list_containers()
        
        updated_containers = []

        for container in containers:
            if container['uid'] == updated_container.uid:
                updated_containers.append(updated_container.to_dict())
            else:
                updated_containers.append(container)

        self._save_to_disk(updated_containers)

    
    def _save_to_disk(self, containers):
        tmp_table_name = self.table_name + '.tmp'
        with open(tmp_table_name, mode = 'w') as f:
            writer = csv.DictWriter(f, fieldnames = Container.schema())
            writer.writerows(containers)

        os.remove(self.table_name)
        os.rename(tmp_table_name, self.table_name)


    def delete_container(self, container_uid):
        containers = self.list_containers()
        
        updated_containers = [containers for container in containers if container['uid'] != container_uid]

        self._save_to_disk(updated_containers)