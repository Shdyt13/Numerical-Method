function displayResults(data) {
    const solutionSteps = document.getElementById('solution-steps');
    const tableBody = document.getElementById('result-table').getElementsByTagName('tbody')[0];

    solutionSteps.innerHTML = '';
    tableBody.innerHTML = '';

    data.forEach(row => {
        // Display formula steps
        const stepDiv = document.createElement('div');
        stepDiv.innerHTML = `
            <p><strong>Iteration ${row.iteration}</strong></p>
            <p>Formula: \\(${row.formula}\\)</p>
            <p>Update: \\(${row.update}\\)</p>
        `;
        solutionSteps.appendChild(stepDiv);

        // Add table rows
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.iteration}</td>
            <td>${row.xl.toFixed(6)}</td>
            <td>${row.xu.toFixed(6)}</td>
            <td>${row.xr.toFixed(6)}</td>
            <td>${row.fxl.toFixed(6)}</td>
            <td>${row.fxu.toFixed(6)}</td>
            <td>${row.fxr.toFixed(6)}</td>
            <td>${row.fxl_fxr.toFixed(6)}</td>
        `;
        tableBody.appendChild(tr);
    });

    // Update MathJax to render the formulas
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}

document.getElementById('calculate-form').onsubmit = async function (e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    
    // Mengirim Data Ke Server
    const response = await fetch('/calculate', {
        method: 'POST',
        body: new URLSearchParams(formData)
    });

    const result = await response.json();
    
    if (response.ok) {
        // Menampilkan hasil jika response sukses
        displayResults(result.steps);
    } else {
        // Menampilkan pesan error jika ada
        alert(result.error);
    }
};
