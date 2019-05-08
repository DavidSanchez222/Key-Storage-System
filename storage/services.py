import csv, os, click

from storage.model import Container

class StorageService:
    
    def __init__(self, table_name):
        self.table_name = table_name

    
    def create_container(self, page):
        with open(self.table_name, mode = 'a') as f:
            writer = csv.DictWriter(f, fieldnames = Container.schema())
            writer.writerow(page.to_dict())

    def list_containers(self, option):
        with open(self.table_name, mode = 'r') as f:
            all_read = csv.DictReader(f, fieldnames = Container.schema())
            if option:
                containers = self.list_containers(False)
                currents_containers = [container for container in containers if container['deleted_at'] == '0']
                return currents_containers
            else:
                return list(all_read)
                    

    def update_container(self, updated_container):
        containers = self.list_containers(False)
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


    def delete_container(self, updated_container):
        containers = self.list_containers(False)
        updated_containers = [containers for container in containers if container['uid'] != updated_container.uid]

        self._save_to_disk(updated_containers)

    
    def search(self, name_page):
        container_list = self.list_containers(True)
        containers = [container for container in container_list if container['name_page'] == name_page]
        return containers