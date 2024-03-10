import logging
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

XML_FILE = 'db.xml'

def init_xml_db():
    try:
        ET.parse(XML_FILE)
        logger.info("XML database loaded successfully.")
    except Exception as e:
        logger.error("Error loading XML database: %s", e)
        root = ET.Element('data')
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)
        logger.info("New XML database created.")

def safe_execution(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logger.error("Error executing %s: %s", function.__name__, e)
            return f"An error occurred: {e}"
    return wrapper

@safe_execution
def add_note_to_xml(topic_name, note_name, text):
    current_timestamp = datetime.now().strftime("%m/%d/%y - %H:%M:%S")

    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    topic_element = find_or_create_topic(root, topic_name)

    if topic_element is not None:
        note_element = ET.SubElement(topic_element, 'note', {'name': note_name})
        ET.SubElement(note_element, 'text').text = text
        ET.SubElement(note_element, 'timestamp').text = current_timestamp
        tree.write(XML_FILE)
        return f"Note '{note_name}' added to topic '{topic_name}' with timestamp {current_timestamp}."
    else:
        return f"Topic '{topic_name}' not found."

@safe_execution
def get_notes_by_topic(topic_name):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    for topic in root.findall('topic'):
        if topic.get('name') == topic_name:
            return [ET.tostring(note, encoding='unicode') for note in topic.findall('note')]
    return []

@safe_execution
def search_wikipedia(topic_name):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {'action': 'query', 'list': 'search', 'srsearch': topic_name, 'format': 'json'}
    response = requests.get(base_url, params=params)
    data = response.json()

    if data['query']['search']:
        first_result = data['query']['search'][0]
        return f"https://en.wikipedia.org/wiki/{first_result['title'].replace(' ', '_')}"
    return "No Wikipedia article found."

@safe_execution
def append_wikipedia_to_topic(topic_name, wikipedia_url):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    topic_element = find_or_create_topic(root, topic_name)

    if topic_element:
        current_time = datetime.now().strftime("%m/%d/%y - %H:%M:%S")
        note_element = ET.SubElement(topic_element, 'note', {'name': 'Wikipedia Link'})
        ET.SubElement(note_element, 'text').text = f"Wikipedia link: {wikipedia_url}"
        ET.SubElement(note_element, 'timestamp').text = current_time
        tree.write(XML_FILE)
        return f"Wikipedia link added to topic '{topic_name}' with timestamp {current_time}."
    else:
        return f"Topic '{topic_name}' not found."

def find_or_create_topic(root, topic_name):
    for topic in root.findall('topic'):
        if topic.get('name') == topic_name:
            return topic
    return ET.SubElement(root, 'topic', {'name': topic_name})

def main():
    init_xml_db()
    with ThreadedXMLRPCServer(('localhost', 8000), allow_none=True) as server:
        logger.info("Server listening on port 8000...")

        server.register_function(add_note_to_xml, 'add_note')
        server.register_function(get_notes_by_topic, 'get_notes')
        server.register_function(search_wikipedia, 'wikipedia_search')
        server.register_function(append_wikipedia_to_topic, 'append_wikipedia_to_topic')

        server.serve_forever()

if __name__ == "__main__":
    main()
