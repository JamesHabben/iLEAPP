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
        
        <!-- lib for regional formatting of phone numbers -->
        <script src="https://unpkg.com/libphonenumber-js@1.9.42/bundle/libphonenumber-js.min.js"></script>
        
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
            <p>Selected Timezone: <span id="currentTimezone"></span></p>
            <p>Selected Date Format: <span id="currentDateFormat"></span></p>
            <p>Selected Time Format: <span id="currentTimeFormat"></span></p>
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
<div class="card bg-white" style="padding: 20px;">
    <h3 class="card-title">Phone Number Display Settings</h3>
    <div class="card-body">
        <div id="phoneNumberSettings">
            <div class="custom-control custom-switch">
                <input type="checkbox" class="custom-control-input" id="regionalFormattingSwitch" checked>
                <label class="custom-control-label" for="regionalFormattingSwitch">Enable Regional Formatting</label>
            </div>
        </div>
        <div id="phoneNumberExamples">
            <h5>Formatting Examples:</h5>
            <ul>
                <li>+1 2345678900 → <div data-phonenumber="+12345678900" style="display: inline-block;"></div></li>
                <li>+44 7711123456 → <div data-phonenumber="+447711123456" style="display: inline-block;"></div></li>
                <li>+91 9876543210 → <div data-phonenumber="+919876543210" style="display: inline-block;"></div></li>
                <li>+61 412345678 → <div data-phonenumber="+61412345678" style="display: inline-block;"></div></li>
            </ul>
        </div>
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
        <label for="dateFormatOptions">Date Format:</label>
        <select id="dateFormatOptions" class="form-control mb-3">
          <option value="YYYY-MM-DD">YYYY-MM-DD --> 2023-01-15</option>
          <option value="MMMM Do YYYY">MMMM Do YYYY --> January 15th 2023</option>
          <option value="MM/DD/YYYY">MM/DD/YYYY --> 01/15/2023</option>
          <option value="DD/MM/YYYY">DD/MM/YYYY --> 15/01/2023</option>
          <option value="ddd, MMM D, YYYY">ddd, MMM D, YYYY --> Sun, Jan 15 2023</option>
          <!-- ... other common date format options -->
        </select>

        <label for="customDateFormat">Custom Date Format:</label>
        <input type="text" id="customDateFormat" placeholder="Enter your custom date format" class="form-control mb-3">

        <small class="form-text text-muted">
          For custom date formats, use the following tokens: YYYY for four-digit year, MM for two-digit month, DD for two-digit day, etc.

        </small>

        <label for="timeFormatOptions" class="mt-3">Time Format:</label>
        <select id="timeFormatOptions" class="form-control">
          <option value="HH:mm:ss (ZZ)">HH:mm:ss (ZZ) --> 13:23:56 (+0000)</option>
          <option value="h:mm:ss a (ZZ)">h:mm:ss a (ZZ) --> 1:23:56 pm (+0000)</option>
          <!-- ... other common time format options -->
        </select>

      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
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
            // Get selected date and time formats from the dropdowns
            var selectedDateFormat = $('#dateFormatOptions').val();
            var selectedTimeFormat = $('#timeFormatOptions').val();
        
            // If the user has entered a custom date format, use that instead
            var customDateFormat = $('#customDateFormat').val();
            if (customDateFormat) {
                selectedDateFormat = customDateFormat;
            }
        
            // Update displayed formats and save to localStorage
            $('#currentDateFormat').text(selectedDateFormat);
            $('#currentTimeFormat').text(selectedTimeFormat);
            localStorage.setItem('savedDateFormat', selectedDateFormat);
            localStorage.setItem('savedTimeFormat', selectedTimeFormat);
        
            // Update the current time information and the dates across the document
            updateCurrentTimeInfo();
            updateDates();
        
            // Hide the format modal
            $('#formatModal').modal('hide');
        });
        
        $('#formatModal').on('shown.bs.modal', function () {
            var savedDateFormat = localStorage.getItem('savedDateFormat');
            var savedTimeFormat = localStorage.getItem('savedTimeFormat');

            if (savedDateFormat) {
                $('#dateFormatOptions').val(savedDateFormat);
            }
            if (savedTimeFormat) {
                $('#timeFormatOptions').val(savedTimeFormat);
            }

            var customDateFormat = localStorage.getItem('customDateFormat');
            if (customDateFormat) {
                $('#customDateFormat').val(customDateFormat);
            }
        });

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
        // Retrieve the saved formats from localStorage
        var savedTimezone = localStorage.getItem('timezone') || 'UTC';
        var savedDateFormat = localStorage.getItem('savedDateFormat') || 'YYYY-MM-DD';
        var savedTimeFormat = localStorage.getItem('savedTimeFormat') || 'HH:mm:ss (ZZ)';

        // Combine date and time formats for displaying the complete datetime
        var combinedFormat = `${savedDateFormat} ${savedTimeFormat}`;

        // Get the current time in the selected timezone
        var currentTime = moment.tz(savedTimezone);

        // Update the HTML elements with the current time information
        $('#currentTimezone').text(savedTimezone);
        $('#currentDateFormat').text(savedDateFormat);
        $('#currentTimeFormat').text(savedTimeFormat);
        $('#currentTimeISO').text(currentTime.format());
        $('#currentTimeFormatted').text(currentTime.format(combinedFormat));
    }


    function updateDates() {
        // Get the currently selected timezone and format
        var savedTimezone = localStorage.getItem('timezone') || 'UTC';
        var savedDateFormat = localStorage.getItem('savedDateFormat') || 'YYYY-MM-DD';
        var savedTimeFormat = localStorage.getItem('savedTimeFormat') || 'HH:mm:ss (ZZ)';

        // Select all divs with a data-timestamp attribute
        const datetimeDivs = document.querySelectorAll('div[data-timestamp]');
        datetimeDivs.forEach(div => {
            const timestamp = div.getAttribute('data-timestamp');
            const formattedDateTime = moment.tz(timestamp, savedTimezone).format(savedDateFormat + ' ' + savedTimeFormat);
            div.textContent = formattedDateTime;
        });

        // Select all divs with a data-date attribute
        const dateDivs = document.querySelectorAll('div[data-date]');
        dateDivs.forEach(div => {
            const datestamp = div.getAttribute('data-date');
            const formattedDate = moment(datestamp).format(savedDateFormat);
            div.textContent = formattedDate;
        });

        // Select all divs with a data-time attribute
        const timeDivs = document.querySelectorAll('div[data-time]');
        timeDivs.forEach(div => {
            const timestamp = div.getAttribute('data-time');
            const formattedTime = moment.tz(timestamp, savedTimezone).format(savedTimeFormat);
            div.textContent = formattedTime;
        });
    }
    
    // Call the function to update the dates when the page loads
    window.addEventListener('load', updateDates);



    // Set the initial state of the switch based on saved settings
    const savedRegionalFormatting = localStorage.getItem('regionalFormatting') === 'true';
    $('#regionalFormattingSwitch').prop('checked', savedRegionalFormatting);

    // Update saved settings and reformat phone numbers when the switch is toggled
    $('#regionalFormattingSwitch').on('change', function() {
        const regionalFormattingEnabled = $(this).is(':checked');
        localStorage.setItem('regionalFormatting', regionalFormattingEnabled);
        updatePhoneNumbers();
    });

    function updatePhoneNumbers() {
        // Check the state of the regional formatting switch
        const savedRegionalFormatting = localStorage.getItem('regionalFormatting') === 'true';

        // Select all divs with a data-phonenumber attribute
        const phoneNumberDivs = document.querySelectorAll('div[data-phonenumber]');

        phoneNumberDivs.forEach(div => {
            // Get the phone number from the data attribute
            const phoneNumber = div.getAttribute('data-phonenumber');

            if (savedRegionalFormatting) {
                // If regional formatting is enabled, format the phone number
                try {
                    const formattedNumber = libphonenumber.parsePhoneNumber(phoneNumber).formatInternational();
                    div.innerHTML = `<span>${formattedNumber}</span> <i data-feather="info" class="icon-info" s
                        tyle="cursor: pointer;" data-toggle="popover" data-placement="top" data-html="true"
                        title="Phone Number Info" data-phonenumber="${phoneNumber}"></i>`;
                } catch (error) {
                    div.textContent = phoneNumber;
                }
            } else {
                // If regional formatting is disabled, display the original phone number
                div.textContent = phoneNumber;
            }
        });
        feather.replace();
        initializePopovers();
    }

    function getPhoneNumberInfoHtml(phoneNumber) {
        try {
            const parsedNumber = libphonenumber.parsePhoneNumber(phoneNumber);
            return `
                <table class="table table-bordered">
                    <tr><td>Raw value</td><td>${phoneNumber}</td></tr>
                    <tr><td>Country Code</td><td>${parsedNumber.countryCallingCode}</td></tr>
                    <tr><td>Country</td><td>${parsedNumber.country}</td></tr>
                    <tr><td>Format International</td><td>${parsedNumber.formatInternational()}</td></tr>
                    <tr><td>Format National</td><td>${parsedNumber.formatNational()}</td></tr>
                    <tr><td>isPossiblePhoneNumber</td><td>${libphonenumber.isPossiblePhoneNumber(phoneNumber)}</td></tr>
                    <tr><td>isValidPhoneNumber</td><td>${libphonenumber.isValidPhoneNumber(phoneNumber)}</td></tr>
                </table>
            `;
        } catch (error) {
            return `Error parsing phone number: ${error.message}`;
        }
    }

    // Initialize the popovers
    function initializePopovers() {
        $.fn.popover.Constructor.Default.whiteList.table = [];
        $.fn.popover.Constructor.Default.whiteList.tr = [];
        $.fn.popover.Constructor.Default.whiteList.td = [];
        $.fn.popover.Constructor.Default.whiteList.th = [];
        $.fn.popover.Constructor.Default.whiteList.div = [];
        $.fn.popover.Constructor.Default.whiteList.tbody = [];
        $.fn.popover.Constructor.Default.whiteList.thead = [];

        $('[data-toggle="popover"]').popover({
            title: 'Phone Number Info',
            placement: 'top',
            html: true,
            content: function() {
                const phoneNumber = $(this).data('phonenumber');
                return getPhoneNumberInfoHtml(phoneNumber);
            }
        });
    }

    $(document).on('click', '.icon-info', function (e) {
        $(this).popover('toggle');
        e.stopPropagation();  // Prevent this click event from propagating to the document
    });

    $(document).on('click', function (e) {
        // Check if the click event target is inside a popover
        if (!$(e.target).closest('.popover').length) {
            $('[data-toggle="popover"]').popover('hide');
        }
    });
    $(document).on('click', '.popover', function (e) {
        e.stopPropagation();
    });

    // Call the function to update the phone numbers when the page loads
    window.addEventListener('load', updatePhoneNumbers);
    // set a listener for page changes
    $('#dtBasicExample').on('draw.dt', function () { updatePhoneNumbers() } );


</script>
"""

page_footer = \
"""
    </body>
</html>
"""
