# Module Description: Parses and extract Voicemail
# Authors: @JohannPLW, @AlexisBrignoni
# Date: 2023-10-01
# Artifact version: 0.0.3
# Requirements: none

from os.path import basename, dirname
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, open_sqlite_file_readonly, media_to_html, convert_unix_epoch


def get_voicemail(files_found, report_folder, seeker, wrap_text, timezone_offset):

    files_found = [file for file in files_found 
                   if basename(dirname(file)) == "Voicemail"]

    for file_found in files_found:
        if file_found.endswith('voicemail.db'):
            voicemail_db = str(file_found)

            cursor = open_sqlite_file_readonly(voicemail_db)
            cursor.execute('''
                SELECT 
                    voicemail.date,
                    voicemail.sender,
                    voicemail.receiver,
                    map.account AS 'ICCID receiver',
                    strftime('%H:%M:%S', voicemail.duration, 'unixepoch') AS 'Duration',
                    voicemail.ROWID
                FROM voicemail
                LEFT OUTER JOIN map ON voicemail.label = map.label
                WHERE voicemail.trashed_date = 0 AND voicemail.flags != 75
            ''')

            all_rows = cursor.fetchall()
            usageentries = len(all_rows)
            if usageentries > 0:
                data_list = []
                for row in all_rows:
                    audio_file = f'{row["ROWID"]}.amr'
                    audio_tag = media_to_html(audio_file, files_found, report_folder)
                    data_list.append((
                        (convert_unix_epoch(row['date']), 'datetime'),
                        row['sender'],
                        row['receiver'],
                        row['ICCID receiver'],
                        row['Duration'],
                        audio_tag
                    ))

                report = ArtifactHtmlReport('Voicemail')
                report.start_artifact_report(report_folder, 'Voicemail')
                report.add_script()
                data_headers = ('Timestamp', 'Sender', 'Receiver', 'ICCID receiver', 'Duration', 'Audio File')
                report.write_artifact_data_table(data_headers, data_list, dirname(file_found), html_no_escape=['Audio File'])
                report.end_artifact_report()

                tsvname = 'Voicemail'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = 'Voicemail'
                timeline(report_folder, tlactivity, data_list, data_headers)

            else:
                logfunc('No voicemail found')


            cursor.execute('''
                SELECT 
                    voicemail.date,
                    voicemail.sender,
                    voicemail.receiver,
                    map.account AS 'ICCID receiver',
                    strftime('%H:%M:%S', voicemail.duration, 'unixepoch') AS 'Duration',
                    CASE voicemail.trashed_date
                        WHEN 0 THEN ""
                        ELSE datetime('2001-01-01', voicemail.trashed_date || ' seconds')
                    END AS 'Trashed date',
                    voicemail.ROWID
                FROM voicemail
                LEFT OUTER JOIN map ON voicemail.label = map.label
                WHERE voicemail.trashed_date != 0 OR voicemail.flags = 75
            ''')

            # Deleted Voicemail
            all_rows = cursor.fetchall()
            usageentries = len(all_rows)
            if usageentries > 0:
                data_list = []
                for row in all_rows:
                    audio_file = f'{row[6]}.amr'
                    audio_tag = media_to_html(audio_file, files_found, report_folder)
                    data_list.append((
                        (convert_unix_epoch(row['date']), 'datetime'),
                        row['sender'],
                        row['receiver'],
                        row['ICCID receiver'],
                        row['Duration'],
                        row['Trashed date'],
                        audio_tag
                    ))

                report = ArtifactHtmlReport('Deleted voicemail')
                report.start_artifact_report(report_folder, 'Deleted voicemail')
                report.add_script()
                data_headers = ('Date and time', 'Sender', 'Receiver', 'ICCID receiver', 'Duration', 'Trashed date', 'Audio File')
                report.write_artifact_data_table(data_headers, data_list, dirname(file_found), html_no_escape=['Audio File'])
                report.end_artifact_report()

                tsvname = 'Deleted voicemail'
                tsv(report_folder, data_headers, data_list, tsvname)

                tlactivity = 'Deleted voicemail'
                timeline(report_folder, tlactivity, data_list, data_headers)

            else:
                logfunc('No deleted voicemail found')

    return

__artifacts__ = {
    "voicemail": (
        "Call History",
        ('**/Voicemail/voicemail.db','**/Voicemail/*.amr'),
        get_voicemail)
}