// ========================================
// timezone and date format handler
// ========================================
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

function getDateTimeFormats() {
    formats = []
    formats['savedTimezone'] = localStorage.getItem('timezone') || 'UTC';
    formats['savedDateFormat'] = localStorage.getItem('savedDateFormat') || 'YYYY-MM-DD';
    formats['savedTimeFormat'] = localStorage.getItem('savedTimeFormat') || 'HH:mm:ss (ZZ)';
    return formats;
}

function formatDateTime(timestamp, shiftTz='saved') {
    formats = getDateTimeFormats()
    if (shiftTz === 'saved') {
        value = moment.tz(timestamp, formats.savedTimezone).format(formats.savedDateFormat + ' ' + formats.savedTimeFormat);
        return value;
    } else if (shiftTz === 'local') {
        value = moment(timestamp).format(formats.savedDateFormat + ' ' + formats.savedTimeFormat);
        return value;
    } else {
        value = moment.utc(timestamp).format(formats.savedDateFormat + ' ' + formats.savedTimeFormat);
        return value;
    }
}

function formatDate(timestamp) {
    formats = getDateTimeFormats()
    return moment(timestamp).format(formats.savedDateFormat);
}

function formatTime(timestamp, shiftTz='saved') {
    formats = getDateTimeFormats()
    if (shiftTz === 'saved') {
        value = moment.tz(timestamp, formats.savedTimezone).format(formats.savedTimeFormat);
        return value;
    } else if (shiftTz === 'local') {
        value = moment(timestamp).format(formats.savedTimeFormat);
        return value;
    } else {
        value = moment.utc(timestamp).format(formats.savedTimeFormat);
        return value;
    }
}

function convertIsoToUnix(isoDate) {
    const date = new Date(isoDate);
    const unixTimestamp = Math.floor(date.getTime() / 1000);
    return unixTimestamp;
}

function formatDistanceToDate(targetDate) {
    const target = moment(targetDate);
    const now = moment();
    const difference = moment.duration(target.diff(now));
    const formattedDifference = difference.format("y [years], M [months], d [days]");
    return formattedDifference;
}

function getDateInfo(date) {
    const momentDate = moment(date);
    const info = {
        dayOfWeek: momentDate.format('dddd'),
        weekNumber: momentDate.week(),
        quarter: momentDate.quarter(),
        isDST: momentDate.isDST(),
        isLeapYear: momentDate.isLeapYear(),
    };
    return info;
}

function updateDates() {
    formats = getDateTimeFormats();

    // Select all divs with a data-timestamp attribute
    const datetimeDivs = document.querySelectorAll('div[data-datetime]');
    datetimeDivs.forEach(div => {
        const timestamp = div.getAttribute('data-datetime');
        try {
            createInfoIcon(div, 'datetime', formatDateTime(timestamp));
        } catch (error) {
            div.textContent = timestamp;
        }
    });

    // Select all divs with a data-date attribute
    const dateDivs = document.querySelectorAll('div[data-date]');
    dateDivs.forEach(div => {
        const datestamp = div.getAttribute('data-date');
        try {
            createInfoIcon(div, 'date', formatDate(datestamp))
        } catch (error) {
            div.textContent = formattedDate;
        }
    });

    // Select all divs with a data-time attribute
    const timeDivs = document.querySelectorAll('div[data-time]');
    timeDivs.forEach(div => {
        const timestamp = div.getAttribute('data-time');
        try {
            createInfoIcon(div, 'datetime', formatTime(timestamp));
        } catch (error) {
            div.textContent = timestamp;
        }
    });
}

// Call the function to update the dates when the page loads
window.addEventListener('load', updateDates);

function getDateTimePopContent(dateTime) {
    try {
        momentDate = getDateInfo(dateTime)
        return `
            <table class="table table-bordered">
                <tr><td>ISO UTC</td><td>${dateTime}</td>
                    <td>Day</td><td>${momentDate.dayOfWeek}</td></tr>
                <tr><td>Formatted UTC</td><td>${formatDateTime(dateTime, 'utc')}</td>
                    <td>Week</td><td>${momentDate.weekNumber}</td></tr>
                <tr><td>Formatted saved TZ</td><td>${formatDateTime(dateTime)}</td>
                    <td>Quarter</td><td>${momentDate.quarter}</td></tr>
                <tr><td>Formatted local TZ</td><td>${formatDateTime(dateTime, 'local')}</td>
                    <td>DST</td><td>${momentDate.isDST}</td></tr>
                <tr><td>Unix Epoch UTC</td><td>${convertIsoToUnix(dateTime)}</td>
                    <td>Leap Year</td><td>${momentDate.isLeapYear}</td></tr>
                <tr><td>From Today</td><td>${formatDistanceToDate(dateTime)}</td>
                    <td></td><td></td></tr>
            </table>
        `;
    } catch (error) {
        return `Error parsing: ${error.message}`;
    }
}

function getTimePopContent(dateTime) {
    try {
        const momentDateTime = moment(dateTime);
        formats = getDateTimeFormats();

        // Convert to local time
        const localTime24 = momentDateTime.format('HH:mm:ss');
        const localTime12 = momentDateTime.format('hh:mm:ss A');

        // Convert to UTC
        const utcTime24 = momentDateTime.utc().format('HH:mm:ss');
        const utcTime12 = momentDateTime.utc().format('hh:mm:ss A');

        // Convert to a saved time zone (e.g., 'America/New_York')
        const savedTimeZone = formats.savedTimezone;
        const savedTime24 = momentDateTime.tz(savedTimeZone).format('HH:mm:ss');
        const savedTime12 = momentDateTime.tz(savedTimeZone).format('hh:mm:ss A');

        return `
            <table class="table table-bordered">
                <tr><td>UTC</td><td>${utcTime24}</td><td>${utcTime12}</td></tr>
                <tr><td>Local</td><td>${localTime24}</td><td>${localTime12}</td></tr>
                <tr><td>Saved (${savedTimeZone})</td><td>${savedTime24}</td><td>${savedTime12}</td></tr>
            </table>
        `;
    } catch (error) {
        return `Error parsing: ${error.message}`;
    }
}


// ========================================
// phone number format handler
// ========================================
// Set the initial state of the switch based on saved settings
const savedRegionalFormatting = localStorage.getItem('regionalFormatting') === 'true';
$('#regionalFormattingSwitch').prop('checked', savedRegionalFormatting);

$(document).ready(function() {
    // Update saved settings and reformat phone numbers when the switch is toggled
    $('#regionalFormattingSwitch').on('change', function() {
        const regionalFormattingEnabled = $(this).is(':checked');
        localStorage.setItem('regionalFormatting', regionalFormattingEnabled);
        updatePhoneNumbers();
    });

    // Update phone numbers on page draw
    $('#dtBasicExample').on('draw.dt', function () {
        updatePhoneNumbers();
    });

    // Call the function to update the phone numbers when the page loads
    updatePhoneNumbers();
});

function updatePhoneNumbers() {
    const savedRegionalFormatting = localStorage.getItem('regionalFormatting') === 'true';
    const phoneNumberDivs = document.querySelectorAll('div[data-phonenumber]');

    phoneNumberDivs.forEach(div => {
        const phoneNumber = div.getAttribute('data-phonenumber');
        if (savedRegionalFormatting) {
            try {
                const formattedNumber = libphonenumber.parsePhoneNumber(phoneNumber).formatInternational();
                createInfoIcon(div, 'phonenumber', formattedNumber);
            } catch (error) {
                div.textContent = phoneNumber;
            }
        } else {
            div.textContent = phoneNumber;
        }
    });
    feather.replace();
    initializePopovers();
}

function getPhoneNumberPopContent(phoneNumber) {
    try {
        const parsedNumber = libphonenumber.parsePhoneNumber(phoneNumber);
        return `
            <table class="table table-bordered">
                <tr><td>Raw value</td><td>${phoneNumber}</td></tr>
                <tr><td>Country Code</td><td>${parsedNumber.countryCallingCode}</td></tr>
                <tr><td>Country</td><td>${parsedNumber.country}</td></tr>
                <tr><td>Format International</td><td>${parsedNumber.formatInternational()}</td></tr>
                <tr><td>Format National</td><td>${parsedNumber.formatNational()}</td></tr>
            </table>
        `;
    } catch (error) {
        return `Error parsing phone number: ${error.message}`;
    }
}


// ===============================================
// Popover code
// ===============================================

// Determine which content callback function to use based on the data type
function getContentCallback(dataType) {
    switch (dataType) {
        case 'phonenumber':
            return getPhoneNumberPopContent;
        case 'datetime':
            return getDateTimePopContent;
        case 'date':
            return getDateTimePopContent;
        default:
            throw new Error(`Unsupported data type: ${dataType}`);
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
        title: 'Info',
        placement: 'top',
        html: true,
        content: function() {
            const parentDiv = $(this).parent()[0];
            const dataType = Object.keys(parentDiv.dataset)[0];
            const dataValue = parentDiv.dataset[dataType];

            const contentCallback = getContentCallback(dataType);
            return contentCallback(dataValue);
        }
    });
}

$(document).ready(function() {
    // Initialize the popover for icons
    $(document).on('click', '.icon-info', function (e) {
        $('[data-toggle="popover"]').popover('hide');
        $(this).popover('toggle');
        e.stopPropagation();  // Prevent this click event from propagating to the document
    });

    // Hide the popover when clicking outside of it
    $(document).on('click', function (e) {
        if (!$(e.target).closest('.popover').length) {
            $('[data-toggle="popover"]').popover('hide');
        }
    });

    // Stop propagation when clicking inside the popover
    $(document).on('click', '.popover', function (e) {
        e.stopPropagation();
    });

    // Hide popover on pagination
    $('#dtBasicExample').on('page.dt', function () {
        $('[data-toggle="popover"]').popover('hide');
    });

    feather.replace();
});

function createInfoIcon(parentDiv, dataType, dataValue) {
    // Create a new span element
    const span = document.createElement('span');
    span.textContent = dataValue;

    // Create a new icon element
    const icon = document.createElement('i');
    icon.setAttribute('data-feather', 'info');
    icon.classList.add('icon-info');
    icon.style.cursor = 'pointer';
    icon.style.marginLeft = '.2rem'
    icon.setAttribute('data-toggle', 'popover');
    icon.setAttribute('data-placement', 'top');
    icon.setAttribute('data-html', 'true');
    icon.setAttribute('title', `Extra Info`);

    // Add elements to parent
    parentDiv.innerHTML = '';
    parentDiv.appendChild(span);
    parentDiv.appendChild(icon);
}