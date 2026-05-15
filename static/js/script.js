document.addEventListener('DOMContentLoaded', fetchRecords);

const form = document.getElementById('attendanceForm');
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById('studentName').value,
        date: document.getElementById('date').value,
        subject: document.getElementById('subject').value,
        status: document.getElementById('status').value
    };

    await fetch('/api/attendance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    form.reset();
    fetchRecords();
});

async function fetchRecords() {
    const res = await fetch('/api/attendance');
    const records = await res.json();
    const body = document.getElementById('attendanceBody');
    body.innerHTML = '';

    records.forEach(record => {
        body.innerHTML += `
            <tr>
                <td>${record.name}</td>
                <td>${record.date}</td>
                <td>${record.subject}</td>
                <td class="status-${record.status.toLowerCase()}">${record.status}</td>
                <td>
                    <button onclick="deleteRecord('${record._id}')" style="background:#ef4444">Delete</button>
                </td>
            </tr>
        `;
    });
}

async function deleteRecord(id) {
    if(confirm('Delete this record?')) {
        await fetch(`/api/attendance/${id}`, { method: 'DELETE' });
        fetchRecords();
    }
}