import glob
import os
import pathlib
import plistlib
import sqlite3
import scripts.artifacts.artGlobals #use to get iOS version -> iOSversion = scripts.artifacts.artGlobals.versionf
from packaging import version #use to search per version number

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import (logfunc, tsv, timeline, is_platform_windows,
                               open_sqlite_file_readonly, convert_apple_epoch)

def get_interactionCcontacts(files_found, report_folder, seeker, wrap_text, timezone_offset):
    for file_found in files_found:
        file_found = str(file_found)
        
        if file_found.endswith('.db'):
            break
    
    cursor = open_sqlite_file_readonly(file_found)
    
    iOSversion = scripts.artifacts.artGlobals.versionf
    if version.parse(iOSversion) >= version.parse("10"):
        cursor.execute('''
            select
                zinteractions.zstartdate,
                zinteractions.zenddate,
                zinteractions.zbundleid,
                zcontacts.zdisplayname,
                zcontacts.zidentifier,
                zinteractions.zdirection,
                zinteractions.zisresponse,
                zinteractions.zrecipientcount,
                zinteractions.zcreationdate,
                zcontacts.zcreationdate,
                zinteractions.zcontenturl
            from
                zinteractions 
            left join
                zcontacts 
                on zinteractions.zsender = zcontacts.z_pk        
        ''')
        
    all_rows = cursor.fetchall()
    usageentries = len(all_rows)
    if usageentries > 0:
        data_list = []
        
        if version.parse(iOSversion) >= version.parse("10"):
            for row in all_rows:
                data_list.append((
                    (convert_apple_epoch(row['zstartdate']), 'datetime'),
                    (convert_apple_epoch(row['zenddate']), 'datetime'),
                    row['zbundleid'],
                    row['zdisplayname'],
                    (row['zidentifier'], 'phonenumber'),
                    row['zdirection'],
                    row['zisresponse'],
                    row['zrecipientcount'],
                    (convert_apple_epoch(row['zcreationdate']), 'datetime'),
                    (convert_apple_epoch(row['zcreationdate']), 'datetime'),
                    row['zcontenturl']
                ))

            report = ArtifactHtmlReport('InteractionC')
            report.start_artifact_report(report_folder, 'Contacts')
            report.add_script()
            data_headers = ('Start Date','End Date','Bundle ID','Display Name','Identifier','Direction',
                            'Is Response','Recipient Count','Zinteractions Creation Date',
                            'Zcontacs Creation Date','Content URL')
            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = 'InteractionC Contacts'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = 'InteractionC Contacts'
            timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc('No data available in InteractionC Contacts')
        
    if version.parse(iOSversion) >= version.parse("10"):
        cursor.execute('''
            select
                zinteractions.ZCREATIONDATE,
                ZINTERACTIONS.zbundleid,
                ZINTERACTIONS.ztargetbundleid,
                ZINTERACTIONS.zuuid,
                ZATTACHMENT.zcontenttext,
                ZATTACHMENT.zuti,
                ZATTACHMENT.zcontenturl
            from zinteractions
            inner join z_1interactions on zinteractions.z_pk = z_1interactions.z_3interactions
            inner join zattachment on z_1interactions.z_1attachments = zattachment.z_pk
        ''')
        
    all_rows = cursor.fetchall()
    usageentries = len(all_rows)
    if usageentries > 0:
        data_list = []
        
        if version.parse(iOSversion) >= version.parse("10"):
            for row in all_rows:
                data_list.append((
                    (convert_apple_epoch(row['ZCREATIONDATE']), 'datetime'),
                    row['zbundleid'],
                    row['ztargetbundleid'],
                    row['zuuid'],
                    row['zcontenttext'],
                    row['zuti'],
                    row['zcontenturl']
                ))
            
            report = ArtifactHtmlReport('InteractionC')
            report.start_artifact_report(report_folder, 'Attachments')
            report.add_script()
            data_headers = ('Creation Date', 'Bundle ID', 'Target Bundle ID', 'ZUUID',
                            'Content Text', 'Uniform Type ID', 'Content URL')
            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = 'InteractionC Attachments'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = 'InteractionC Attachments'
            timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc('No data available in InteractionC Attachments')
    

    return
    
__artifacts__ = {
    "interactionCcontacts": (
        "InteractionC",
        ('**/interactionC.db*'),
        get_interactionCcontacts)
}