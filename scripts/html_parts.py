# Variables in page_header = {title}
# 
page_header = \
"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title>{0}</title>
        <!-- Dark mode -->
        <link rel="stylesheet" href="_elements/dark-mode.css">
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.11.2/css/all.css">
        <!-- Google Fonts Roboto -->
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap">
        <!-- Bootstrap core CSS -->
        <link rel="stylesheet" href="_elements/MDB-Free_4.13.0/css/bootstrap.min.css">
        <!-- Material Design Bootstrap - TOGGLE THIS FOR ALTERNATE DESIGN!-->
        <link rel="stylesheet" href="_elements/MDB-Free_4.13.0/css/mdb.min.css">
        <!-- Your custom styles (optional) -->
        <link rel="stylesheet" href="_elements/dashboard.css">
        <link rel="stylesheet" href="_elements/chats.css">
        
        <!-- Datetime libs for dynamic display - Moment.js, Moment Timezone -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/moment-timezone/0.5.34/moment-timezone-with-data.min.js"></script>
        
        <!-- MDBootstrap Datatables  -->
        <link rel="stylesheet" href="_elements/MDB-Free_4.13.0/css/addons/datatables.min.css" rel="stylesheet">

        <!-- Icons -->
        <!--script src="https://unpkg.com/feather-icons/dist/feather.min.js"></script-->
        <script src="_elements/feather.min.js"></script>
    </head>
    <body>
"""
# body_part_1 includes fixed navbar at top and starting tags for rest of page
# Variables = {version_info}
body_start = \
"""
    <!-- Start your project here-->
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
        <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">{0}</a>
        <div class="custom-control custom-switch">
            <input type="checkbox" class="custom-control-input" id="darkSwitch" />
            <label class="custom-control-label mr-2" for="darkSwitch" style="color:white">Dark Switch</label>
        </div>
        <script src="_elements/dark-mode-switch.js"></script>
    </nav>

    <div class="container-fluid">
        <div class="row">
"""
body_sidebar_setup = \
"""
            <nav class="col-md-2 d-none d-md-block bg-light sidebar">
                <div class="sidebar-sticky" id="sidebar_id">
                    <ul class="nav flex-column">
"""
# The 'active' class must be set only for the current page, it will highlight that entry in blue
#   class="nav-link active"
# Below is sample data, use own generated data!
body_sidebar_dynamic_data = \
"""
                        <h6 class="sidebar-heading justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                            Saved reports
                        </h6>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="home"></span> Report Home
                            </a>
                        </li>
                        <h6 class="sidebar-heading justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                            Recent Activity
                        </h6>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="activity"></span> RecentActivity_0
                            </a>
                        </li>
                        <h6 class="sidebar-heading justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                            Script Logs
                        </h6>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="archive"></span> Processed Files Log
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="archive"></span> Screen Output
                            </a>
                        </li>
                        <h6 class="sidebar-heading justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                            Usage Stats
                        </h6>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="bar-chart-2"></span> UsageStats_0
                            </a>
                        </li>
                        <h6 class="sidebar-heading justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                            Wellbeing
                        </h6>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="layers"></span> Events
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                <span data-feather="user"></span> Wellbeing Account
                            </a>
                        </li>
"""
body_sidebar_dynamic_data_placeholder = '<!--__INSERT-NAV-BAR-DATA-HERE__-->'
body_sidebar_trailer = \
"""
                    </ul>
                    <br /><br />
                </div>
            </nav>
"""

body_main_header = \
"""
            <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
"""
# Variable {title}, {description}
body_main_data_title = \
"""
                <div class="justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="display-5">{0}</h1>
                    <h6 class="animated fadeIn mb-3">{1}</h6>
                </div>
"""
body_spinner = \
"""
                <div id="mySpinner" class="spinner-border text-info float-right" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
"""
body_infinite_loading_bar = \
"""
                <div id ="infiniteLoading" class="progress md-progress primary-color-dark">
                    <div class="indeterminate"></div>
                </div>
"""
# body_main_data is a placeholder, replace content with real data
body_main_data = \
"""
                <h5>All dates and times are in UTC unless stated otherwise.</h5>
                <div class="alert alert-warning" role="alert">
                    All dates and times are in UTC unless noted otherwise!
                </div>
                <p class="note note-primary mb-4">
                    All dates and times are in UTC unless noted otherwise!
                </p>
                <h2>Case</h2>
                <div class="table-responsive">
                    <table class="table table-bordered table-hover table-sm" width="70%">
                        <tbody>
                            <tr>
                                <td>Extraction Location</td>
                                <td>N:\aleapp_images\Pixel 5</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="androidevents">
                    <h1>Android Events</h1>
                    <h1>Android Events</h1>
                </div>
"""
# tabs code for Case information in index.html
# Variables are {case_table_code}, {script_run_log}, {processed_file_list}
tabs_code = \
"""
    <ul class="nav nav-tabs" id="myTab" role="tablist">
        <li class="nav-item">
            <a class="nav-link active" id="case-tab" data-toggle="tab" href="#case" role="tab" aria-controls="case" 
                aria-selected="true">Details</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" id="device-list-tab" data-toggle="tab" href="#device" role="tab" aria-controls="device" 
                aria-selected="false">Device details</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" id="run-log-tab" data-toggle="tab" href="#run" role="tab" aria-controls="run" 
                aria-selected="false">Script run log</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" id="files-list-tab" data-toggle="tab" href="#files" role="tab" aria-controls="files" 
                aria-selected="false">Processed files list</a>
        </li>
    </ul>
    <div class="tab-content" id="myTabContent">
        <div class="tab-pane fade show active" id="case" role="tabpanel" aria-labelledby="case-tab"><br />{}</div>
        <div class="tab-pane fade" id="device" role="tabpanel" aria-labelledby="device-tab"><br />{}</div>
        <div class="tab-pane fade text-monospace" id="run" role="tabpanel" aria-labelledby="script-run-tab"><br />{}</div>
        <div class="tab-pane fade" id="files" role="tabpanel" aria-labelledby="profile-tab"><br />{}</div>
    </div>
"""

# card for timezone display settings
card_timezone_settings = \
"""
<div class="card bg-white" style="padding: 20px;">
    <h3 class="card-title">Date and Time Display Settings</h3>
    <div class="card-body">
        <div id="currentSettings">
            <p>Currently Selected Timezone: <span id="currentTimezone">UTC</span></p>
            <p>Currently Selected Format: <span id="currentFormat">MMMM Do YYYY, h:mm:ss a</span></p>
            <p>Current Time in ISO Format: <span id="currentTimeISO"></span></p>
            <p>Current Time with applied format: <span id="currentTimeFormatted"></span></p>
        </div>
        <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#timezoneModal">
            Change Timezone
        </button>
        <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#formatModal">
            Change Format
        </button>
    </div>
</div>
"""

# modal window for timezone selection
modal_timezone = \
"""
            <!-- TimeZone Modal -->
<div class="modal fade" id="timezoneModal" tabindex="-1" role="dialog" aria-labelledby="timezoneModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="timezoneModalLabel">Select Timezone</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <input type="text" id="timezoneSearch" placeholder="Search for a timezone" class="form-control">
        <div id="timezoneList">
          <!-- List of timezones will be populated here -->
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" id="saveTimezone">Save changes</button>
      </div>
    </div>
  </div>
</div>
"""

# modal window for datetime format
modal_datetime_format = \
"""
<!-- DateTime Format Modal -->
<div class="modal fade" id="formatModal" tabindex="-1" role="dialog" aria-labelledby="formatModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="formatModalLabel">Select Date and Time Format</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <select id="formatOptions" class="form-control">
          <option value="MMMM Do YYYY, h:mm:ss a ZZ">January 1st 2023, 12:00:00 am +0000</option>
          <option value="YYYY-MM-DD HH:mm:ss ZZ">2023-01-15 00:00:00 +0000</option>
          <option value="YYYY-MM-DD h:mm:ss a ZZ">2023-01-15 12:00:00 am +0000</option>
          <option value="MM/DD/YYYY h:mm:ss a ZZ">01/15/2023 12:00:00 am +0000</option>
          <option value="MM/DD/YYYY HH:mm:ss ZZ">01/15/2023 00:00:00 +0000</option>
          <option value="DD/MM/YYYY h:mm:ss a ZZ">15/01/2023 12:00:00 am +0000</option>
          <option value="DD/MM/YYYY HH:mm:ss ZZ">15/01/2023 00:00:00 +0000</option>
          <!-- ... other common format options -->
        </select>
        <input type="text" id="customFormat" placeholder="Or enter your custom format" class="form-control">
        <p id="formatExplanation" style="margin-top: 10px;">
            Custom Format Instructions: <br>
            - YYYY: 4-digit year (e.g., 2023) <br>
            - MM: 2-digit month (e.g., 01 for January) <br>
            - DD: 2-digit day of the month (e.g., 01 for the first day of the month) <br>
            - HH: 2-digit hour in 24-hour format (e.g., 00 for midnight) <br>
            - hh: 2-digit hour in 12-hour format (e.g., 12 for noon) <br>
            - mm: 2-digit minute (e.g., 00 for the first minute of the hour) <br>
            - ss: 2-digit second (e.g., 00 for the first second of the minute) <br>
            - a: am/pm <br>
            - ZZ: timezone offset (e.g., +0000 for UTC) <br>
        </p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" id="saveFormat">Save changes</button>
      </div>
    </div>
  </div>
</div>
"""
# thank you note , at bottom of index.html
thank_you_note = \
"""
                <br /><br /><br />
                <div class="text-center">
                    <br />
                    <div class="card bg-white mb-3" style="max-width: 500px; margin:auto">
                        <div class="row no-gutters">
                            <center><div class="col-md-4">
                                <img src="_elements/logo.jpg" class="card-img" alt="DFIR">
                            </div>
                            <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title">Thank you for using iLEAPP</h5>
                                <p class="card-text">
                                    Support open source and report any bugs!
                                </p>
                                <!--Github-->
                                <a class="btn-floating btn-git" type="button" role="button" href="https://github.com/abrignoni/ileapp" target="_blank"><i class="fab fa-github"></i> Project Home </a>
                                <p class="card-text fadeIn"><small class="text-muted">iLEAPP Team</small></p>
                            </div>
                            </div></center>
                        </div>
                    </div>
                    <br />
                    <br />
                </div><!--end text-center area-->
"""

# Variable: HTML List of individual contributors (for index.html)
credits_block = \
"""
    <div class="alert alert-light mb-4 bg-white" style="border-style: none">
        <h4 class="text-center">iLEAPP contributors</h4>
        <ul class="list-group" style="max-width: 500px; margin:auto">
            {}
        </ul>
    </div>
"""
blog_icon = '<i class="fab fa-blogger-b fa-fw"></i>'
twitter_icon = '<i class="fab fa-twitter fa-fw"></i>'
github_icon = '<i class="fab fa-github fa-fw"></i>'
blank_icon = '<i class="fab fa-fw"></i>'
individual_contributor = \
"""
            <li class="list-group-item d-flex justify-content-between align-items-center bg-white"><i class="fas fa-medal"></i>{}
                <span>
                    {}
                </span>
            </li>
"""
""" sample contibutor data..
                    <a href="{}" target="_blank"><i class="fab fa-blogger-b fa-fw"></i></a> &nbsp;
                    <a href="{}" target="_blank"><i class="fab fa-twitter fa-fw"></i></a> &nbsp;
                    <a href="{}" target="_blank"><i class="fab fa-github fa-fw"></i></a>
"""
body_main_trailer = \
"""
            </main>
        </div>
    </div>
"""

body_end = \
"""
    <!-- End your project here-->

    <!-- jQuery -->
    <script type="text/javascript" src="_elements/MDB-Free_4.13.0/js/jquery.min.js"></script>
    <!-- Bootstrap tooltips -->
    <script type="text/javascript" src="_elements/MDB-Free_4.13.0/js/popper.min.js"></script>
    <!-- Bootstrap core JavaScript -->
    <script type="text/javascript" src="_elements/MDB-Free_4.13.0/js/bootstrap.js"></script>
    <!-- MDB core JavaScript -->
    <script type="text/javascript" src="_elements/MDB-Free_4.13.0/js/mdb.min.js"></script>
    <!-- Your custom scripts -->
    <!-- MDBootstrap Datatables  -->
    <script type="text/javascript" src="_elements/MDB-Free_4.13.0/js/addons/datatables.min.js"></script>
    <script>
        feather.replace()
    </script>
"""
nav_bar_script = \
"""
    <script>
        feather.replace();
        var element = document.getElementById("sidebar_id");
        var searchParams = new URLSearchParams(window.location.search);
        if (searchParams.has('navpos')) {
            var nav_pos = parseInt(searchParams.get('navpos'));
            if (!isNaN(nav_pos))
                element.scrollTop = nav_pos;
        }
    </script>
"""

nav_bar_script_footer = \
"""
    <script>
        var elemScrollTop = document.getElementById("sidebar_id").scrollTop.toString();
        document.addEventListener("DOMContentLoaded", function() {
            var element = document.getElementById("sidebar_id");
            element.addEventListener("scroll", function() {
                elemScrollTop = document.getElementById("sidebar_id").scrollTop.toString();
            });
        });
        $('a.nav-link').click(function(e) {
            e.preventDefault();
            location.href = $(this).attr('href') + "?navpos=" + elemScrollTop;
        });
    </script>
"""
default_responsive_table_script = \
"""
    <script>
        $(document).ready(function() {
            $('.table').DataTable({
                "aLengthMenu": [[ 15, 50, 100, -1 ], [ 15, 50, 100, "All" ]],
            });
            $('.dataTables_length').addClass('bs-select');
            $('#mySpinner').remove();
            //$('#infiniteLoading').remove();
        });
    </script>
"""


timezone_scripts = \
"""
<script>
    // timezone and date format javascript
    $(document).ready(function() {
        var timezones = moment.tz.names();
        populateTimezoneList(timezones);
        updateCurrentTimeInfo();

        // Event handler for the timezone modal search input
        $('#timezoneSearch').on('input', function() {
            var searchTerm = $('#timezoneSearch').val().toLowerCase();
            console.log("search term ", searchTerm)
            $('.timezone-item').each(function() {
                var timezone = $(this).data('timezone').toLowerCase();
                if (timezone.includes(searchTerm)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        });

        // Event handler to select a timezone when clicked
        $('#timezoneList').on('click', '.timezone-item', function () {
            var selectedTimezone = $(this).data('timezone');
            $('#timezoneSearch').val(selectedTimezone);
            $('#timezoneModal').modal('hide');
            $('#currentTimezone').text(selectedTimezone);
            localStorage.setItem('timezone', selectedTimezone);
            updateCurrentTimeInfo();
            updateDates();
        });

        $('#saveFormat').on('click', function () {
            var selectedFormat = $('#formatOptions').val();

            // If the user has entered a custom format, use that instead
            var customFormat = $('#customFormat').val();
            if (customFormat) {
                selectedFormat = customFormat;
            }

            $('#currentFormat').text(selectedFormat);
            localStorage.setItem('format', selectedFormat);

            updateCurrentTimeInfo();
            updateDates();

            $('#formatModal').modal('hide');

        });

        var savedTimezone = localStorage.getItem('timezone');
        var savedFormat = localStorage.getItem('format');

        if (savedTimezone) {
            $('#currentTimezone').text(savedTimezone);
        }

        if (savedFormat) {
            $('#currentFormat').text(savedFormat);
        }

        updateCurrentTimeInfo();
        updateDates();
    });

    function populateTimezoneList(timezones) {
        var timezoneList = $('#timezoneList');
        timezones.forEach(function(timezone) {
            timezoneList.append('<div class="timezone-item" data-timezone="' + timezone + '">' + timezone + '</div>');
        });
    }

    function updateCurrentTimeInfo() {
        var currentTimezone = $('#currentTimezone').text();
        var currentFormat = $('#currentFormat').text();

        // Get the current time in the selected timezone
        var currentTime = moment.tz(currentTimezone);

        // Update the HTML elements with the current time information
        $('#currentTimeISO').text(currentTime.format());
        $('#currentTimeFormatted').text(currentTime.format(currentFormat));
    }

    function updateDates() {
        // Get the currently selected timezone and format
        var savedTimezone = localStorage.getItem('timezone') || 'UTC';
        var savedFormat = localStorage.getItem('format') || 'MMMM Do YYYY, h:mm:ss a';
    
        // Select all divs with a data-timestamp attribute
        const dateDivs = document.querySelectorAll('div[data-timestamp]');
    
        dateDivs.forEach(div => {
            // Get the timestamp from the data attribute
            const timestamp = div.getAttribute('data-timestamp');
    
            // Convert and format the timestamp using Moment.js
            const formattedDate = moment.tz(timestamp, savedTimezone).format(savedFormat);
    
            // Update the content of the div to display the formatted date
            div.textContent = formattedDate;
        });
    }


        // Call the function to update the dates when the page loads
        window.addEventListener('load', updateDates);
    </script>
"""

page_footer = \
"""
    </body>
</html>
"""
