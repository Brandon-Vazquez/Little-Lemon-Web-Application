document.addEventListener('DOMContentLoaded', function () {
  var dateInput = document.getElementById('id_reservation_date');
  var slotSelect = document.getElementById('id_reservation_slot');

  if (!dateInput || !slotSelect) {
    return;
  }

  function todayISO() {
    var today = new Date();
    var month = String(today.getMonth() + 1).padStart(2, '0');
    var day = String(today.getDate()).padStart(2, '0');
    return today.getFullYear() + '-' + month + '-' + day;
  }

  function updateSlots() {
    var date = dateInput.value || todayISO();
    fetch('/bookings?date=' + date)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        var bookings = JSON.parse(data);
        var bookedSlots = bookings.map(function (booking) {
          return booking.fields.reservation_slot;
        });

        Array.prototype.forEach.call(slotSelect.options, function (option) {
          if (!option.value) {
            return;
          }
          var slot = parseInt(option.value, 10);
          if (bookedSlots.indexOf(slot) !== -1) {
            option.disabled = true;
            option.style.color = 'grey';
          } else {
            option.disabled = false;
            option.style.color = '';
          }
        });
      });
  }

  if (!dateInput.value) {
    dateInput.value = todayISO();
  }

  updateSlots();
  dateInput.addEventListener('change', updateSlots);
});
