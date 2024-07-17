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
      return Response({'content': 'Missing HTML content'}, status=status.HTTP_400_BAD_REQUEST)

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
      return Response({'content': 'Missing HTML content'}, status=status.HTTP_400_BAD_REQUEST)

    minified_html = minify(html_content, remove_comments=True)
    
    # Return the minified HTML  
    return Response({'content': minified_html})





class CSSBeautifierView(APIView):
  def post(self, request:Request):
    # Get the CSS content from the request body
    css_content = request.data.get('css')
    if not css_content:
      return Response({'content': 'Missing CSS content'}, status=status.HTTP_400_BAD_REQUEST)

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
      return Response({'content': 'Missing CSS content'}, status=status.HTTP_400_BAD_REQUEST)

    # Use cssmin to minify the CSS
    minified_css = cssmin(css_content)

    # Return the minified CSS
    return Response({'content': minified_css})

class JavaScriptMinifierView(APIView):
  def post(self, request:Request):
    # Get the JavaScript content from the request body
    javascript_content = request.data.get('javascript')
    if not javascript_content:
      return Response({'content': 'Missing JavaScript content'}, status=status.HTTP_400_BAD_REQUEST)

    minified_javascript = jsmin(javascript_content)

    # Return the minified JavaScript
    return Response({'content': minified_javascript})


class JavaScriptBeautifierView(APIView):
  def post(self, request:Request):
    # Get the JavaScript content from the request body
    javascript_content = request.data.get('javascript')
    if not javascript_content:
      return Response({'content': 'Missing JavaScript content'}, status=status.HTTP_400_BAD_REQUEST)

    # Use jsformatter to beautify the JavaScript
    beautified_javascript = jsbeautifier.beautify(javascript_content)

    # Return the beautified JavaScript
    return Response({'content': beautified_javascript})

