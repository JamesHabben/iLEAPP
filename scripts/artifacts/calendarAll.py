import glob
import os
import sys
import stat
import pathlib
import plistlib
import sqlite3
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, open_sqlite_file_readonly, convert_apple_epoch


def get_calendarAll(files_found, report_folder, seeker, wrap_text, timezone_offset):
	file_found = str(files_found[0])
	#os.chmod(file_found, 0o0777)
	cursor = open_sqlite_file_readonly(file_found)
	cursor.execute(
		"""
		select 
			rowid,
			title,
			flags,
			color,
			symbolic_color_name,
			external_id,
			self_identity_email,
			sharing_status,
			shared_owner_name,
			shared_owner_address,
			subcal_url
		from Calendar
		"""
	)

	all_rows = cursor.fetchall()
	usageentries = len(all_rows)
	data_list = []    
	if usageentries > 0:
		for row in all_rows:
			data_list.append((
				row['rowid'],
				row['title'],
				row['flags'],
				(row['color'], 'color'),
				row['symbolic_color_name'],
				row['external_id'],
				row['self_identity_email'],
				row['subcal_url'],
				row['sharing_status'],
				row['shared_owner_name'],
				row['shared_owner_address']
			))
	
		description = ''
		report = ArtifactHtmlReport('Calendar Names')
		report.start_artifact_report(report_folder, 'Calendar Names', description)
		report.add_script()
		data_headers = ('Row ID', 'Title','Flags','Color','Symbolic Color Name',
						'External ID','Self Identity Email', 'Remote URL', 'Sharing Status',
						'Shared Owner Name', 'Shared Owner Email')
		report.write_artifact_data_table(data_headers, data_list, file_found)
		report.end_artifact_report()
		
		tsvname = 'Calendar Names'
		tsv(report_folder, data_headers, data_list, tsvname)
	else:
		logfunc('No data available for Calendar Names')
	
	cursor.execute(
		"""
		SELECT 
			start_date,
			start_tz,
			end_date,
			end_tz,
			all_day,
			summary,
			calendar_id,
			title,
			last_modified
		FROM CalendarItem
		INNER JOIN calendar ON calendar_id = calendar.rowid
		ORDER BY start_date;
		"""
	)

	all_rows = cursor.fetchall()
	usageentries = len(all_rows)
	data_list = []    
	if usageentries > 0:
		for row in all_rows:
			if row['all_day'] == 1:
				start_value = (convert_apple_epoch(row['start_date']), 'date')
				end_value = (convert_apple_epoch(row['end_date']), 'date')
			else:
				start_value = (convert_apple_epoch(row['start_date']), 'datetime')
				end_value = (convert_apple_epoch(row['end_date']), 'datetime')
			data_list.append((
				start_value,
				row['start_tz'],
				end_value,
				row['end_tz'],
				row['all_day'],
				row['summary'],
				row['calendar_id'],
				row['title'],
				(convert_apple_epoch(row['last_modified']), 'datetime')
			))
	
		description = ''
		report = ArtifactHtmlReport('Calendar Items')
		report.start_artifact_report(report_folder, 'Calendar Items', description)
		report.add_script()
		data_headers = ('Start Date','Start Timezone','End Date','End Timezone',
						'All Day?','Summary','Calendar ID','Calendar Name','Last Modified')
		report.write_artifact_data_table(data_headers, data_list, file_found)
		report.end_artifact_report()
		
		tsvname = 'Calendar Items'
		tsv(report_folder, data_headers, data_list, tsvname)
		
		tlactivity = 'Calendar Items'
		timeline(report_folder, tlactivity, data_list, data_headers)
	else:
		logfunc('No data available for Calendar Items')
	
	cursor.execute(
		"""
		SELECT
			display_name,
			address,
			first_name,
			last_name
		from Identity
		"""
	)

	all_rows = cursor.fetchall()
	usageentries = len(all_rows)
	data_list = []    
	if usageentries > 0:
		for row in all_rows:
			data_list.append((
				row['display_name'],
				row['address'],
				row['first_name'],
				row['last_name']
			))
	
		description = ''
		report = ArtifactHtmlReport('Calendar Identity')
		report.start_artifact_report(report_folder, 'Calendar Identity', description)
		report.add_script()
		data_headers = ('Display Name','Address','First Name','Last Name')     
		report.write_artifact_data_table(data_headers, data_list, file_found)
		report.end_artifact_report()
		
		tsvname = 'Calendar Identity'
		tsv(report_folder, data_headers, data_list, tsvname)
	else:
		logfunc('No data available for Calendar Identity')

__artifacts__ = {
    "calendarall": (
        "Calendar",
        ('**/Calendar.sqlitedb'),
        get_calendarAll)
}