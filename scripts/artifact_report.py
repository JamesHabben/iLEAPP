import html
import json
import os
import datetime
import inspect
from datetime import timezone, timedelta
from dateutil import parser
from scripts.html_parts import *
from scripts.ilapfuncs import is_platform_windows
from scripts.version_info import aleapp_version

class ArtifactHtmlReport:

    def __init__(self, artifact_name, artifact_category=''):
        self.report_file = None
        self.report_file_path = ''
        self.script_code = ''
        self.artifact_name = artifact_name
        self.artifact_category = artifact_category # unused

    def __del__(self):
        if self.report_file:
            self.end_artifact_report()

    def start_artifact_report(self, report_folder, artifact_file_name, artifact_description=''):
        '''Creates the report HTML file and writes the artifact name as a heading'''
        self.report_file = open(os.path.join(report_folder, f'{artifact_file_name}.temphtml'), 'w', encoding='utf8')
        self.report_file.write(page_header.format(f'iLEAPP - {self.artifact_name} report'))
        self.report_file.write(body_start.format(f'iLEAPP {aleapp_version}'))
        self.report_file.write(body_sidebar_setup)
        self.report_file.write(body_sidebar_dynamic_data_placeholder) # placeholder for sidebar data
        self.report_file.write(body_sidebar_trailer)
        self.report_file.write(body_main_header)
        self.report_file.write(body_main_data_title.format(f'{self.artifact_name} report', artifact_description))
        self.report_file.write(body_spinner) # Spinner till data finishes loading
        #self.report_file.write(body_infinite_loading_bar) # Not working!

    def add_script(self, script=''):
        '''Adds a default script or the script supplied'''
        if script:
            self.script_code += script + nav_bar_script_footer
        else:
            self.script_code += default_responsive_table_script + nav_bar_script_footer

    def write_artifact_data_table(
        self,
        data_headers,
        data_list,
        source_path,
        write_total=True,
        write_location=True,
        html_escape=True,
        cols_repeated_at_bottom=True,
        table_responsive=True,
        table_style='',
        table_id='dtBasicExample',
        html_no_escape=[]
    ):
        ''' Writes info about data, then writes the table to html file
            Parameters
            ----------
            data_headers   : List/Tuple of table column names

            data_list      : List/Tuple of lists/tuples which contain rows of data

            source_path    : Source path of data

            write_total    : Toggles whether to write out a line of total rows written

            write_location : Toggles whether to write the location of data source

            html_escape    : If True (default), then html special characters are encoded

            cols_repeated_at_bottom : If True (default), then col names are also at the bottom of the table

            table_responsive : If True (default), div class is table_responsive

            table_style    : Specify table style like "width: 100%;"

            table_id       : Specify an identifier string, which will be referenced in javascript

            html_no_escape  : if html_escape=True, list of columns not to escape
        '''

        if (not self.report_file):
            raise ValueError('Output report file is closed/unavailable!')

        def format_value(input_value):
            if isinstance(input_value, tuple) and len(input_value) == 2:
                value, data_type = input_value

                if data_type == 'datetime':
                    # Format as full date and time value
                    if isinstance(value, str):
                        formats = [
                            '%Y-%m-%d %H:%M:%S.%f',  # With fractional seconds
                            '%Y-%m-%d %H:%M:%S',     # Without fractional seconds
                            '%Y-%m-%dT%H:%M:%SZ'     # iso format without fractional seconds
                        ]
                        for date_format in formats:
                            try:
                                value = datetime.datetime.strptime(value, date_format).replace(tzinfo=timezone.utc)
                            except ValueError:
                                continue

                    if isinstance(value, datetime.datetime):
                        return f'<td data-sort="{value.isoformat()}"><div data-datetime="{value.isoformat()}"></div></td>'
                    else:
                        return f'<td>{value}</td>'

                elif data_type == 'date':
                    # Format as only the date component
                    if isinstance(value, str):
                        date_obj = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                    else:
                        date_obj = value
                    return f'<td data-sort="{date_obj.isoformat()}"><div data-date="{date_obj.isoformat()}"></div></td>'

                elif data_type == 'time':
                    # Format as no date only time, using 24-hour format for sorting
                    try:
                        time_obj = parser.parse(value).time()
                    except ValueError:
                        return f'<td>{value}</td>'
                    time_value = time_obj.strftime('%H:%M:%S')
                    return f'<td data-sort="{time_value}"><div data-time="{time_value}"></div></td>'

                elif data_type == 'phonenumber':
                    return f'<td><div data-phonenumber="{value}"></div></td>'

                elif data_type == 'color':
                    return f'<td><div data-color="{value}"></div></td>'

                else:
                    return f'<td>{value}</td>'

            elif input_value in [None, 'N/A']:
                return '<td></td>'
            else:
                return '<td>' + html.escape(str(input_value)) + '</td>'


        num_entries = len(data_list)
        if write_total:
            self.write_minor_header(f'Total number of entries: {num_entries}', 'h6')
        if write_location:
            if is_platform_windows():
                source_path = source_path.replace('/', '\\')
            if source_path.startswith('\\\\?\\'):
                source_path = source_path[4:]
            self.write_lead_text(f'{self.artifact_name} located at: {source_path}')

        self.report_file.write('<br />')

        if table_responsive:
            self.report_file.write("<div class='table-responsive'>")

        table_head = '<table id="{}" class="table table-striped table-bordered table-xsm" cellspacing="0" {}>' \
                     '<thead>'.format(table_id, (f'style="{table_style}"') if table_style else '')
        self.report_file.write(table_head)
        self.report_file.write(
            '<tr>' + ''.join(
                (f'<th>{html.escape(str(header))}</th>' for header in data_headers)
            ) + '</tr>'
        )
        self.report_file.write('</thead><tbody>')

        def format_value_for_json(input_value):
            if isinstance(input_value, tuple) and len(input_value) == 2:
                value, data_type = input_value
                # Return an object with value and type
                return {'value': str(value), 'type': data_type}
            return str(input_value)  # Return the value directly for standard types

        json_data_string = ''
        if table_responsive:
            json_data = []
            for row in data_list:
                json_row = [format_value_for_json(value) for value in row]
                json_data.append(json_row)

            json_data_string = json.dumps(json_data, ensure_ascii=False)
            # self.report_file.write(f'<script>var jsonData = {json_data_string};</script>')
        else:
            for row in data_list:
                row_content = []
                for value, header in zip(row, data_headers):
                    if html_escape or header in html_no_escape:
                        row_content.append(f'<td>{html.escape(str(value))}</td>')
                    else:
                        row_content.append(f'<td>{value}</td>')
                row_html = '<tr>' + ''.join(row_content) + '</tr>'
                self.report_file.write(row_html)

        self.report_file.write('</tbody>')
        if cols_repeated_at_bottom:
            self.report_file.write('<tfoot><tr>' + ''.join(
                ('<th>{}</th>'.format(html.escape(str(x))) for x in data_headers)) + '</tr></tfoot>')
        self.report_file.write('</table>')
        if table_responsive:
            self.report_file.write(f'<script>var jsonData = {json_data_string};</script>')
            self.report_file.write("</div>")

    def add_section_heading(self, heading, size='h2'):
        heading = html.escape(heading)
        data = '<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">' \
               '    <{0} class="{0}">{1}</{0}>' \
               '</div>'
        self.report_file.write(data.format(size, heading))

    def write_minor_header(self, heading, heading_tag=''):
        heading = html.escape(heading)
        if heading_tag:
            self.report_file.write(f'<{heading_tag}>{heading}</{heading_tag}>')
        else:
            self.report_file.write(f'<h3 class="h3">{heading}</h3>')

    def write_lead_text(self, text):
        self.report_file.write(f'<p class="lead">{text}</p>')

    def write_raw_html(self, code):
        self.report_file.write(code)

    def get_calling_script_name(self):
        # Get the frame of the current code execution
        current_frame = inspect.currentframe()
        # Get the caller's frame (the script that imported the module)
        caller_frame = inspect.getouterframes(current_frame, 2)[2]
        # Extract the file name (script name) from the caller's frame
        script_name = os.path.basename(caller_frame.filename)
        html_string = f'<div class="module_name">Module Filename: {script_name}</div>'
        return html_string

    def end_artifact_report(self):
        if self.report_file:
            self.report_file.write(
                self.get_calling_script_name() +
                body_main_trailer +
                body_end +
                self.script_code +
                page_footer
            )
            self.report_file.close()
            self.report_file = None

        
