
from typing import List, AnyStr, Dict, Any

class DisplayFormat(object):
    marker = "<!-- insert here -->"

    @staticmethod
    def html_table(input_list: List[Dict[AnyStr, AnyStr]]) -> AnyStr:
        if len(input_list) > 0:
            table_html = '<table><tr><th>'
            table_html += '</th><th>'.join([key for key, _ in input_list[0].items()])
            table_html += '</th>'
            for row in input_list:
                table_html += '<tr>'
                for _, value in row.items():
                    table_html += f'<td>{str(value)}</td>'
                table_html += '</tr>'

            table_html += '</table>'
            return table_html
        else:
            return "<h4>Empty list</h4>"

    @staticmethod
    def html_insert(html_filename: AnyStr, html_table: AnyStr) -> AnyStr:
        with open(html_filename, 'r') as f:
            html_page = f.read()
        updated_html_page = html_page.replace(DisplayFormat.marker, html_table)
        return updated_html_page
