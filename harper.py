from services import GitHubService
import json
import argparse

from configuration import Configuration

""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.

Credit: https://stackoverflow.com/questions/18478287/making-object-json-serializable-with-regular-encoder/18561055#18561055
"""
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default # Replace it.

def writeOutput(results: dict):
    json_object = json.dumps(results, indent = 4) 
    with open('output.json', 'w') as file:
        file.write(json_object)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="GitHub Personal Access Token")
    args = parser.parse_args()
    if not args.token:
        print('Please retry with a GitHub PAT token specified with the `--token TOKEN` argument')
        return
    
    service = GitHubService(args.token)
    results = []
    config = Configuration()
    for repository in config.data:
        result = service.generateNotification(repository)
        results.append(result)
    writeOutput(results)

if __name__ == "__main__":
    main()
