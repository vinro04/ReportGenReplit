document.addEventListener('DOMContentLoaded', function() {
    const reportForm = document.getElementById('report-form');
    if (reportForm) {
        reportForm.addEventListener('submit', function(e) {
            const startDate = new Date(document.getElementById('start_date').value);
            const endDate = new Date(document.getElementById('end_date').value);
            
            if (startDate > endDate) {
                e.preventDefault();
                alert('Start date must be before end date');
            }
        });
    }
});