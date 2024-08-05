document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append('imageFile', document.getElementById('imageFile').files[0]);
    formData.append('format', document.getElementById('format').value);
    formData.append('quality', document.getElementById('quality').value);
    formData.append('resolution', document.getElementById('resolution').value);
    
    const response = await fetch('/convert', {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'converted_image.' + document.getElementById('format').value;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
    } else {
        console.error('Error:', response.statusText);
    }
});
