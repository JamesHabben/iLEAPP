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

    $(document).ready(function() {
        // Update saved settings and reformat phone numbers when the switch is toggled
        $('#regionalFormattingSwitch').on('change', function() {
            const regionalFormattingEnabled = $(this).is(':checked');
            localStorage.setItem('regionalFormatting', regionalFormattingEnabled);
            updatePhoneNumbers();
        });

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

        // Update phone numbers on page draw
        $('#dtBasicExample').on('draw.dt', function () {
            updatePhoneNumbers();
        });

        // Call the function to update the phone numbers when the page loads
        updatePhoneNumbers();
    });
