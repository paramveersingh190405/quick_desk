document.addEventListener('DOMContentLoaded', function() {
    // Flash message auto-close
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.classList.add('fade-out');
            setTimeout(() => msg.remove(), 500);
        }, 3000);
    });

    // Ticket status change handler
    document.querySelectorAll('.status-select').forEach(select => {
        select.addEventListener('change', function() {
            const ticketId = this.dataset.ticketId;
            const newStatus = this.value;
            
            fetch(`/tickets/${ticketId}/status`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status: newStatus })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        });
    });
});