# Photos.sqlite Migrations - UserEventAgent
# Author:  John Hyla
# Version: 1.0.0
#
#   Description:
#   Parses migration records found in the Photos.sqlite database. May assist in determining history of iOS versions history
#   Based on SQL Queries written by Scott Koenig https://theforensicscooter.com/
#   https://github.com/ScottKjr3347/iOS_Local_PL_Photos.sqlite_Queries/blob/main/iOS16/iOS16_LPL_Phsql_MigrationHistory.txt
#


from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, kmlgen, timeline, is_platform_windows, generate_thumbnail, \
    open_sqlite_file_readonly, convert_apple_epoch
from scripts.builds_ids import OS_build


def get_photosMigration(files_found, report_folder, seeker, wrap_text, timezone_offset):
    for file_found in files_found:
        file_found = str(file_found)

        if file_found.endswith('.sqlite'):
            break
      

    cursor = open_sqlite_file_readonly(file_found)
    cursor.execute("""
        SELECT 
            zMigrationHistory.Z_PK,
            zMigrationHistory.Z_ENT AS 'zMigrationHistory-zENT',
            zMigrationHistory.Z_OPT AS 'zMigrationHistory-zOPT',
            zMigrationHistory.ZMIGRATIONDATE,
            zMigrationHistory.ZINDEX,
            CASE zMigrationHistory.ZMIGRATIONTYPE
                WHEN 0 THEN '0-StillTesting'
                WHEN 1 THEN '1-StillTesting'
                WHEN 2 THEN '2-iOS Update-2'
                WHEN 3 THEN '3-iOS History Start/Factory Reset-3'
                ELSE 'Unknown-New-Value!: ' || zMigrationHistory.ZMIGRATIONTYPE || ''
            END AS 'Migration_Type',
            zMigrationHistory.ZFORCEREBUILDREASON,
            zMigrationHistory.ZSOURCEMODELVERSION,
            zMigrationHistory.ZMODELVERSION,
            zMigrationHistory.ZOSVERSION,
            zMigrationHistory.ZORIGIN,
            zMigrationHistory.ZSTOREUUID,
            zMigrationHistory.ZGLOBALKEYVALUES
        FROM ZMIGRATIONHISTORY zMigrationHistory
        ORDER BY zMigrationHistory.ZMIGRATIONDATE
    """)
    all_rows = cursor.fetchall()
    usageentries = len(all_rows)
    data_list = []
    counter = 0
    if usageentries > 0:
        for row in all_rows:
            ios_version = row['ZOSVERSION'] + ' - ' + OS_build[row['ZOSVERSION']]


            data_list.append((
                (convert_apple_epoch(row['ZMIGRATIONDATE']), 'datetime'),
                row['ZINDEX'],
                row['Migration_Type'],
                row['ZFORCEREBUILDREASON'],
                row['ZSOURCEMODELVERSION'],
                row['ZMODELVERSION'],
                ios_version,
                row['ZORIGIN'],
                row['ZSTOREUUID']
            ))

            counter += 1

        description = ''
        report = ArtifactHtmlReport('Photos.sqlite Migrations')
        report.start_artifact_report(report_folder, 'Migrations', description)
        report.add_script()
        data_headers = ('Date', 'Index', 'Type', 'Force Rebuild Reason', 'Source Model Version',
                        'Model Version', 'Build/iOS Version', 'Origin', 'Store UUID')
        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()

        tsvname = 'Photos-sqlite Migrations'
        tsv(report_folder, data_headers, data_list, tsvname)

        tlactivity = 'Photos-sqlite Migrations'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No data available for Photos.sqlite metadata')

    return



__artifacts__ = {
    "photosMigration": (
        "Photos",
        ('**/Photos.sqlite*'),
        get_photosMigration)
}