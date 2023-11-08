import sqlite3
import textwrap

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import (logfunc, tsv, timeline, is_platform_windows, open_sqlite_file_readonly,
                               convert_apple_epoch)

def get_netusage(files_found, report_folder, seeker, wrap_text, timezone_offset):
    
    for file_found in files_found:
        file_found = str(file_found)
        if not file_found.endswith('.sqlite'):
            continue # Skip all other files
    
        if 'netusage' in file_found:
            cursor = open_sqlite_file_readonly(file_found)
            cursor.execute('''
                select
                    ZLIVEUSAGE.ZTIMESTAMP,
                    ZPROCESS.ZFIRSTTIMESTAMP,
                    ZPROCESS.ZTIMESTAMP,
                    ZPROCESS.ZBUNDLENAME,
                    ZPROCESS.ZPROCNAME,
                    case ZLIVEUSAGE.ZKIND
                        when 0 then 'Process'
                        when 1 then 'App'
                    end as usage_kind,
                    ZLIVEUSAGE.ZWIFIIN,
                    ZLIVEUSAGE.ZWIFIOUT,
                    ZLIVEUSAGE.ZWWANIN,
                    ZLIVEUSAGE.ZWWANOUT,
                    ZLIVEUSAGE.ZWIREDIN,
                    ZLIVEUSAGE.ZWIREDOUT
                from ZLIVEUSAGE
                left join ZPROCESS on ZPROCESS.Z_PK = ZLIVEUSAGE.Z_PK
            ''')

            all_rows = cursor.fetchall()
            usageentries = len(all_rows)
            if usageentries > 0:
                report = ArtifactHtmlReport('Network Usage (netusage) - App Data')
                report.start_artifact_report(report_folder, 'Network Usage (netusage) - App Data')
                report.add_script()
                data_headers = ('Last Connect Timestamp','First Usage Timestamp',
                                'Last Usage Timestamp','Bundle Name',
                                'Process Name','Type',
                                'Wifi In (Bytes)','Wifi Out (Bytes)',
                                'Mobile/WWAN In (Bytes)','Mobile/WWAN Out (Bytes)',
                                'Wired In (Bytes)','Wired Out (Bytes)')
                data_list = []
                for row in all_rows:
                    data_list.append((
                        (convert_apple_epoch(row['ZTIMESTAMP']), 'datetime'),
                        (convert_apple_epoch(row['ZFIRSTTIMESTAMP']), 'datetime'),
                        (convert_apple_epoch(row['ZTIMESTAMP']), 'datetime'),
                        row['ZBUNDLENAME'],
                        row['ZPROCNAME'],
                        row['usage_kind'],
                        row['ZWIFIIN'],
                        row['ZWIFIOUT'],
                        row['ZWWANIN'],
                        row['ZWWANOUT'],
                        row['ZWIREDIN'],
                        row['ZWIREDOUT']
                    ))

                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Network Usage (netusage) - App Data'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Network Usage (netusage) - App Data'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Network Usage (netusage) - App Data data available')
            
            cursor.execute('''
                select
                    ZNETWORKATTACHMENT.ZFIRSTTIMESTAMP,
                    ZNETWORKATTACHMENT.ZTIMESTAMP,
                    ZNETWORKATTACHMENT.ZIDENTIFIER,
                    case ZNETWORKATTACHMENT.ZKIND
                        when 1 then 'Wifi'
                        when 2 then 'Cellular'
                    end as net_kind,
                    ZLIVEROUTEPERF.ZBYTESIN,
                    ZLIVEROUTEPERF.ZBYTESOUT,
                    ZLIVEROUTEPERF.ZCONNATTEMPTS,
                    ZLIVEROUTEPERF.ZCONNSUCCESSES,
                    ZLIVEROUTEPERF.ZPACKETSIN,
                    ZLIVEROUTEPERF.ZPACKETSOUT
                from ZNETWORKATTACHMENT
                left join ZLIVEROUTEPERF on ZLIVEROUTEPERF.Z_PK = ZNETWORKATTACHMENT.Z_PK
            ''')

            all_rows = cursor.fetchall()
            usageentries = len(all_rows)
            if usageentries > 0:

                report = ArtifactHtmlReport('Network Usage (netusage) - Connections')
                report.start_artifact_report(report_folder, 'Network Usage (netusage) - Connections')
                report.add_script()
                data_headers = ('First Connection Timestamp','Last Connection Timestamp','Network Name','Cell Tower ID/Wifi MAC','Network Type','Bytes In','Bytes Out','Connection Attempts','Connection Successes','Packets In','Packets Out') # Don't remove the comma, that is required to make this a tuple as there is only 1 element
                data_list = []
                for row in all_rows:

                    if row['ZIDENTIFIER'] is not None:
                        netname, id_mac = row['ZIDENTIFIER'].split('-')
                    else:
                        netname, id_mac = '', ''

                    data_list.append((
                        (convert_apple_epoch(row['ZFIRSTTIMESTAMP']), 'datetime'),
                        (convert_apple_epoch(row['ZTIMESTAMP']), 'datetime'),
                        netname,
                        id_mac,
                        row['net_kind'],
                        row['ZBYTESIN'],
                        row['ZBYTESOUT'],
                        row['ZCONNATTEMPTS'],
                        row['ZCONNSUCCESSES'],
                        row['ZPACKETSIN'],
                        row['ZPACKETSOUT']
                    ))


                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Network Usage (netusage) - Connections'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Network Usage (netusage) - Connections'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Network Usage (netusage) - Connections data available')
            

        if 'DataUsage' in file_found:
            cursor = open_sqlite_file_readonly(file_found)
            cursor.execute('''
                select
                    ZLIVEUSAGE.ZTIMESTAMP as live_timestamp,
                    ZPROCESS.ZFIRSTTIMESTAMP,
                    ZPROCESS.ZTIMESTAMP as process_timestamp,
                    ZPROCESS.ZBUNDLENAME,
                    ZPROCESS.ZPROCNAME,
                    case ZLIVEUSAGE.ZKIND
                        when 0 then 'Process'
                        when 1 then 'App'
                        else ZLIVEUSAGE.ZKIND
                    end as live_kind,
                    ZLIVEUSAGE.ZWIFIIN,
                    ZLIVEUSAGE.ZWIFIOUT,
                    ZLIVEUSAGE.ZWWANIN,
                    ZLIVEUSAGE.ZWWANOUT
                from ZLIVEUSAGE
                left join ZPROCESS on ZPROCESS.Z_PK = ZLIVEUSAGE.Z_PK
            ''')

            all_rows = cursor.fetchall()
            usageentries = len(all_rows)
            if usageentries > 0:
                report = ArtifactHtmlReport('Network Usage (DataUsage) - App Data')
                report.start_artifact_report(report_folder, 'Network Usage (DataUsage) - App Data')
                report.add_script()
                data_headers = ('Last Connect Timestamp','First Usage Timestamp','Last Usage Timestamp',
                                'Bundle Name','Process Name','Type',
                                'Wifi In (Bytes)','Wifi Out (Bytes)','Mobile/WWAN In (Bytes)',
                                'Mobile/WWAN Out (Bytes)')
                data_list = []
                for row in all_rows:
                    data_list.append((
                        (convert_apple_epoch(row['live_timestamp']), 'datetime'),
                        (convert_apple_epoch(row['ZFIRSTTIMESTAMP']), 'datetime'),
                        (convert_apple_epoch(row['process_timestamp']), 'datetime'),
                        row['ZBUNDLENAME'],
                        row['ZPROCNAME'],
                        row['live_kind'],
                        row['ZWIFIIN'],
                        row['ZWIFIOUT'],
                        row['ZWWANIN'],
                        row['ZWWANOUT']
                    ))

                report.write_artifact_data_table(data_headers, data_list, file_found)
                report.end_artifact_report()
                
                tsvname = f'Network Usage (DataUsage) - App Data'
                tsv(report_folder, data_headers, data_list, tsvname)
                
                tlactivity = f'Network Usage (DataUsage) - App Data'
                timeline(report_folder, tlactivity, data_list, data_headers)
            else:
                logfunc('No Network Usage (DataUsage) - App Data data available')
            

__artifacts__ = {
    "netusage": (
        "Network Usage",
        ('**/netusage.sqlite*','**/DataUsage.sqlite*'),
        get_netusage)
}