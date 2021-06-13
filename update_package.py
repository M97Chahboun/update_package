import yaml
import requests
from lxml import etree
from io import StringIO

def getNewVersion(pkg_name):
    url = f'https://pub.dev/packages/{pkg_name}'
    with requests.get(url) as req:
        doc = etree.parse(StringIO(req.text), etree.HTMLParser()).getroot()
        title = doc.xpath('//h1[@class="title"]')[0].text.strip()
        return '^' + (title.split(' ')[1])


if __name__ == "__main__":
    filename = 'pubspec.yaml'
    new_map = None
    with open(filename, 'r') as _f:
        docs = yaml.load(_f, Loader=yaml.FullLoader)
        deps = docs['dependencies']
        for package_name, old_version in deps.items():
            if package_name == 'flutter':
                continue
            last_version = getNewVersion(package_name)
            print(f'{package_name}: {last_version}')