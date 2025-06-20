"""
Container export functionality for pushing created containers to Docker registries.
"""

import docker
import json
import os
from typing import Dict, List

class ContainerExporter:
    def __init__(self, config_path: str = "config.json"):
        self.client = docker.from_env()
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def tag_container(self, container_id: str, service_name: str) -> str:
        """Tag a container for registry push"""
        registry = self.config.get("registry", {})
        tag = f"{registry.get('default_registry', 'docker.io')}/{registry.get('tag_prefix', 'demo')}-{service_name}:{registry.get('version', 'latest')}"
        
        container = self.client.containers.get(container_id)
        container.commit(repository=tag.split(':')[0], tag=tag.split(':')[1])
        return tag
    
    def push_to_registry(self, tag: str, registry_auth: Dict = None) -> bool:
        """Push tagged container to registry"""
        try:
            self.client.images.push(tag, auth_config=registry_auth)
            return True
        except Exception as e:
            print(f"Failed to push {tag}: {e}")
            return False
    
    def export_all_containers(self, container_ids: Dict[str, str]) -> Dict[str, str]:
        """Export all application containers to registry"""
        exported_tags = {}
        for service_name, container_id in container_ids.items():
            tag = self.tag_container(container_id, service_name)
            if self.push_to_registry(tag):
                exported_tags[service_name] = tag
                print(f"✅ Exported {service_name}: {tag}")
            else:
                print(f"❌ Failed to export {service_name}")
        return exported_tags