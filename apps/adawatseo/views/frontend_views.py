import csv
import json
from xml.etree import ElementTree as ET

import jsbeautifier
from bs4 import BeautifulSoup
from cssbeautifier import beautify
from cssmin import cssmin
from htmlmin import minify
from jsmin import jsmin
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HTMLBeautifierView(APIView):
  def post(self, request:Request):
    # Get the HTML content from the request body
    html_content = request.data.get('html')
    if not html_content:
      return Response({'content': 'Missing HTML content'}, )

    # Use BeautifulSoup to beautify the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    beautified_html = soup.prettify()

    # Return the beautified HTML
    return Response({'content': beautified_html})






class HTMLMinifierView(APIView):
  def post(self, request:Request):
    # Get the HTML content from the request body
    html_content = request.data.get('html')
    if not html_content:
      return Response({'content': 'Missing HTML content'}, )

    minified_html = minify(html_content, remove_comments=True)
    
    # Return the minified HTML  
    return Response({'content': minified_html})





class CSSBeautifierView(APIView):
  def post(self, request:Request):
    # Get the CSS content from the request body
    css_content = request.data.get('css')
    if not css_content:
      return Response({'content': 'Missing CSS content'}, )

    # Use cssbeautifier to beautify the CSS
    beautified_css = beautify(css_content,
    {
        'indent_size':1,
'indent_with_tabs':True,
'end_with_newline':True,
'newline_between_rules':False,
'indent_empty_lines':True,
    })

    # Return the beautified CSS
    return Response({'content': beautified_css})




class CSSMinifierView(APIView):
  def post(self, request:Request):
    # Get the CSS content from the request body
    css_content = request.data.get('css')
    if not css_content:
      return Response({'content': 'Missing CSS content'}, )

    # Use cssmin to minify the CSS
    minified_css = cssmin(css_content)

    # Return the minified CSS
    return Response({'content': minified_css})

class JavaScriptMinifierView(APIView):
  def post(self, request:Request):
    # Get the JavaScript content from the request body
    javascript_content = request.data.get('javascript')
    if not javascript_content:
      return Response({'content': 'Missing JavaScript content'}, )

    minified_javascript = jsmin(javascript_content)

    # Return the minified JavaScript
    return Response({'content': minified_javascript})


class JavaScriptBeautifierView(APIView):
  def post(self, request:Request):
    # Get the JavaScript content from the request body
    javascript_content = request.data.get('javascript')
    if not javascript_content:
      return Response({'content': 'Missing JavaScript content'}, )

    # Use jsformatter to beautify the JavaScript
    beautified_javascript = jsbeautifier.beautify(javascript_content)

    # Return the beautified JavaScript
    return Response({'content': beautified_javascript})




class JSONFormatterView(APIView):
  def post(self, request:Request):
    # Get the JSON data from the request body
    json_data = request.data.get('json')
    if not json_data:
      return Response({'error': 'Missing JSON data'}, )

    try:
      # Parse the JSON data (check if it's already valid JSON)
      parsed_json = json.loads(json_data)
    except json.JSONDecodeError as e:
      return Response({'content': f'Invalid JSON data: {str(e)}'}, )

    # Format the JSON data with indentation
    formatted_json = json.dumps(parsed_json, indent=4)

    # Return the formatted JSON
    return Response({'content': formatted_json})

class JSONValidatorView(APIView):
  def post(self, request:Request):
    # Get the JSON data from the request body
    json_data = request.data.get('json')
    if not json_data:
      return Response({'error': 'Missing JSON data'}, )

    try:
      # Parse the JSON data (check if it's already valid JSON)
      parsed_json = json.loads(json_data)
    except json.JSONDecodeError as e:
      return Response({'content': f'Invalid JSON data: {str(e)}'}, )

    return Response({'content': 'JSON is valid'})


class JSONMinifierView(APIView):
  def post(self, request:Request):
    # Get the JSON data from the request body
    json_data = request.data.get('json')
    if not json_data:
      return Response({'error': 'Missing JSON data'}, )

    try:
      # Parse the JSON data (check if it's already valid JSON)
      parsed_json = json.loads(json_data)
    except json.JSONDecodeError as e:
      return Response({'content': f'Invalid JSON data: {str(e)}'}, )

    # Format the JSON data with indentation
    formatted_json = json.dumps(parsed_json, separators=(',',':'))

    # Return the formatted JSON
    return Response({'content': formatted_json})


class XMLToJSONView(APIView):
  def post(self, request:Request):
    # Get the XML data from the request body
    xml_data = request.data.get('xml')
    if not xml_data:
      return Response({'content': 'Missing XML data'}, )

    try:
      # Parse the XML data
      root = ET.fromstring(xml_data)
    except ET.ParseError as e:
      return Response({'content': f'Invalid XML data: {str(e)}'}, )

    # Convert the XML element tree to a dictionary
    json_data = self.xml_to_dict(root)

    # Return the JSON data
    return Response({'content': json.dumps(json_data)})

  def xml_to_dict(self, xml_element):
    """
    Recursive function to convert an XML element to a Python dictionary
    """
    tag = xml_element.tag
    text = xml_element.text
    attributes = xml_element.attrib

    # Handle child elements
    children = []
    for child in xml_element:
      child_data = self.xml_to_dict(child)
      if isinstance(child_data, list):
        children.extend(child_data)
      else:
        children.append(child_data)

    # Construct the dictionary
    if children:
      if text:
        data = {'text': text, 'children': children}
      else:
        data = children
    else:
      if text:
        data = text
      else:
        data = attributes

    return {tag: data}




class CSVToJSONView(APIView):
  def post(self, request:Request):
    # Get the CSV data from the request body
    csv_data = request.data.get('csv')
    if not csv_data:
      return Response({'content': 'Missing CSV data'}, )

    try:
      # Read the CSV data from a string (assuming it's sent as a string)
      reader = csv.reader(csv.StringIO(csv_data))
      # Extract the header row (optional)
      headers = next(reader)

      # Convert CSV rows to dictionaries
      json_data = []
      for row in reader:
        if headers:
          # Create a dictionary using headers and row values
          json_data.append(dict(zip(headers, row)))
        else:
          # Create a dictionary with numeric keys (if no headers)
          json_data.append(dict(enumerate(row)))

    except csv.Error as e:
      return Response({'content': f'Invalid CSV data: {str(e)}'}, )

    # Return the JSON data
    return Response({'content': json.dumps(json_data)})






class TSVToJSONView(APIView):
  def post(self, request:Request):
    # Get the TSV data from the request body
    tsv_data = request.data.get('tsv')
    if not tsv_data:
      return Response({'content': 'Missing TSV data'}, )

    try:
      # Read the TSV data from a string (assuming it's sent as a string)
      reader = csv.reader(csv.StringIO(tsv_data), delimiter='\t')  # Specify tab delimiter
      # Extract the header row (optional)
      headers = next(reader)

      # Convert TSV rows to dictionaries
      json_data = []
      for row in reader:
        if headers:
          # Create a dictionary using headers and row values
          json_data.append(dict(zip(headers, row)))
        else:
          # Create a dictionary with numeric keys (if no headers)
          json_data.append(dict(enumerate(row)))

    except csv.Error as e:
      return Response({'content': f'Invalid TSV data: {str(e)}'}, )

    # Return the JSON data
    return Response({'content': json.dumps(json_data)})




class JSONToXMLView(APIView):
  def post(self, request:Request):
    # Get the JSON data from the request body
    json_data = request.data.get('json')
    if not json_data:
      return Response({'content': 'Missing JSON data'}, )

    try:
      # Parse the JSON data
      data = json.loads(json_data)
    except json.JSONDecodeError as e:
      return Response({'content': f'Invalid JSON data: {str(e)}'}, )

    # Convert the JSON data to an XML element tree
    root = self.json_to_xml(data)

    # Generate the XML string from the element tree
    xml_data = ET.tostring(root, encoding='utf-8').decode('utf-8')

    # Return the XML data
    return Response({'content': xml_data})

  def json_to_xml(self, data):
    """
    Recursive function to convert a Python dictionary to an XML element tree
    """
    if isinstance(data, (str, int, float, bool)):
      print(data)
      return ET.Element('value', data)  # Handle basic data types
    elif isinstance(data, list):
      # Create a parent element for the list
      parent = ET.Element(self.get_tag_name(data))
      # Convert each item in the list to an XML element and append to parent
      for item in data:
        child = self.json_to_xml(item)
        parent.append(child)
      return parent
    elif isinstance(data, dict):
      # Create a parent element for the dictionary
      parent = ET.Element(self.get_tag_name(data))
      # Convert each key-value pair to a child element and append to parent
      for key, value in data.items():
        child = self.json_to_xml(value)
        child.tag = key  # Set the element tag to the key
        parent.append(child)
      return parent
    else:
      # Handle unsupported data types (optional: raise exception or return empty element)
      return ET.Element('unsupported_type')  # Placeholder for unsupported types

  def get_tag_name(self, data):
    """
    Function to determine the tag name for a list or dictionary (optional)
    """
    # You can customize the logic here to generate meaningful tag names
    # Based on your data structure or key names in the dictionary
    if isinstance(data, list):
      return 'item'  # Default tag name for list elements
    elif isinstance(data, dict):
      return 'data'  # Default tag name for dictionary elements (can be customized)
    return 'element'  # Default fallback






class JSONToCSVView(APIView):
  def post(self, request:Request):
    # Get the JSON data from the request body
    json_data = request.data.get('json')
    if not json_data:
      return Response({'content': 'Missing JSON data'}, )

    try:
      # Parse the JSON data
      data = json.loads(json_data)
    except json.JSONDecodeError as e:
      return Response({'content': f'Invalid JSON data: {str(e)}'}, )

    # Check if the data is a list of dictionaries (expected for CSV)
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
      return Response({'content': 'Invalid JSON format. Expecting a list of dictionaries.'}, )

    # Extract headers from the first dictionary (assuming consistent structure)
    headers = list(data[0].keys())

    # Create a CSV string using a StringIO buffer
    csv_buffer = csv.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(headers)  # Write header row

    # Write data rows to the CSV buffer
    for row in data:
      row_data = [row.get(header) for header in headers]  # Handle missing keys
      writer.writerow(row_data)

    # Get the CSV data as a string from the buffer
    csv_data = csv_buffer.getvalue()

    # Return the CSV data
    return Response({'content': csv_data})



class JSONToTextView(APIView):
  def post(self, request:Request):
    # Get the JSON data from the request body
    json_data = request.data.get('json')
    if not json_data:
      return Response({'content': 'Missing JSON data'}, )

    try:
      # Parse the JSON data
      data = json.loads(json_data)
    except json.JSONDecodeError as e:
      return Response({'content': f'Invalid JSON data: {str(e)}'}, )

    # Choose a conversion approach (consider options below)
    text_data = self.convert_json_to_text_basic(data)  # Basic approach (replace with your chosen method)

    # Return the text data
    return Response({'content': text_data})

  def convert_json_to_text_basic(self, data):
    """
    Basic conversion approach: traverses JSON structure and builds text representation
    """
    # Implement your text generation logic here based on data type and structure
    # This example provides a simple placeholder for key-value pairs
    if isinstance(data, dict):
      text = ", ".join(f"{key}: {value}" for key, value in data.items())
    elif isinstance(data, list):
      text = ", ".join(str(item) for item in data)
    else:
      text = str(data)  # Handle basic data types
    return text

  # You can define additional conversion methods for lists, nested structures, etc. (optional)



class JSONToTSVView(APIView):
  def post(self, request:Request):
    # Get the JSON data from the request body
    json_data = request.data.get('json')
    if not json_data:
      return Response({'content': 'Missing JSON data'}, )

    try:
      # Parse the JSON data
      data = json.loads(json_data)
    except json.JSONDecodeError as e:
      return Response({'content': f'Invalid JSON data: {str(e)}'}, )

    # Check if the data is a list of dictionaries (expected for TSV)
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
      return Response({'content': 'Invalid JSON format. Expecting a list of dictionaries.'}, )

    # Extract headers from the first dictionary (assuming consistent structure)
    headers = list(data[0].keys())

    # Create a TSV string using a StringIO buffer
    tsv_buffer = csv.StringIO()
    writer = csv.writer(tsv_buffer, delimiter='\t')  # Specify tab delimiter
    writer.writerow(headers)  # Write header row

    # Write data rows to the TSV buffer
    for row in data:
      row_data = [row.get(header) for header in headers]  # Handle missing keys
      writer.writerow(row_data)

    # Get the TSV data as a string from the buffer
    tsv_data = tsv_buffer.getvalue()

    # Return the TSV data
    return Response({'content': tsv_data})
