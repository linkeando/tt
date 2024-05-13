import os
import yaml
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenApiLoader:
    def __init__(self, base_directory):
        self.index = 'principal.yaml'
        self.base_directory = base_directory
        self.folders = ['./tags', './components', './paths']
        self.section_processors = {
            'array': self.process_array_section,
            'object': self.process_object_section,
        }
        self.openapi_content = {}

    def load_yaml_files(self):
        main_file_path = os.path.join(self.base_directory, self.index)
        self.openapi_content = self.load_and_merge_yaml(main_file_path)
        for folder in self.folders:
            self.process_directory(os.path.join(self.base_directory, folder))
        return self.openapi_content

    @staticmethod
    def load_and_merge_yaml(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                parsed_yaml = yaml.safe_load(file)
                return parsed_yaml or {}
        except Exception as e:
            logger.error(f"Error while loading YAML file {file_path}: {str(e)}")
            return {}

    def process_directory(self, dir_path):
        try:
            for file in os.listdir(dir_path):
                self.process_file(os.path.join(dir_path, file))
        except Exception as e:
            logger.error(f"Error while processing directory {dir_path}: {str(e)}")

    def process_file(self, file_path):
        try:
            stats = os.stat(file_path)
            if stats.st_mode & 0o4000:  # If it's a directory
                self.process_directory(file_path)
            elif file_path.endswith('.yaml'):
                parsed_yaml = self.load_and_merge_yaml(file_path)
                self.process_and_merge_sections(parsed_yaml)
        except Exception as e:
            logger.error(f"Error while processing file {file_path}: {str(e)}")

    def process_and_merge_sections(self, content):
        for section, data in content.items():
            self.process_section(section, data)

    def process_section(self, section, data):
        processor = self.section_processors.get('array' if isinstance(data, list) else 'object')
        if processor:
            processor(section, data)

    def process_array_section(self, section, data):
        self.openapi_content[section] = (self.openapi_content.get(section, []) + data) if data else []

    def process_object_section(self, section, data):
        self.openapi_content[section] = self.merge_section(self.openapi_content.get(section, {}), data)

    @staticmethod
    def merge_section(existing_data, new_data):
        if isinstance(existing_data, list):
            return existing_data + (new_data or [])
        elif isinstance(existing_data, dict):
            return {**existing_data, **new_data}
        else:
            return new_data or existing_data

    def write_yaml_file(self, file_name, data):
        try:
            file_path = os.path.join(self.base_directory, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, allow_unicode=True)
            logger.info(f"File '{file_name}' generated successfully.")
        except Exception as e:
            logger.error(f"Error while writing YAML file: {str(e)}")