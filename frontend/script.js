async function getRecommendations() {
    const id = document.getElementById("studentId").value;
    const resultsDiv = document.getElementById("results");

    if (!id) {
        resultsDiv.innerHTML = `
            <div class="error-message"><p>Please enter a Student ID.</p></div>
        `;
        return;
    }

    resultsDiv.innerHTML = "<p>Loading...</p>";

    const res = await fetch(`/recommend?student_id=${id}`);

    // --- Handle API Errors ---
    if (!res.ok) {
        const errorData = await res.json().catch(() => ({ error: "Unknown API Error" }));
        resultsDiv.innerHTML = `
            <div class="error-message">
                <h3>API Error (Status ${res.status})</h3>
                <p>${errorData.error}</p>
            </div>
        `;
        return;
    }

    const data = await res.json();
    resultsDiv.innerHTML = "";

    // --- No Results ---
    if (data.length === 0) {
        resultsDiv.innerHTML = `
            <div class="info-message">
                <p>No similar students found.</p>
            </div>
        `;
        return;
    }

    // --- Display Cards ---
    data.forEach(student => {
        let similarity = student.similarity * 100;
        let simText = isNaN(similarity) ? "N/A" : similarity.toFixed(2) + "%";

        // BADGE COLOR
        let badgeClass = "red-badge";
        if (similarity >= 75) badgeClass = "green-badge";
        else if (similarity >= 45) badgeClass = "yellow-badge";

        // BORDER COLOR
        let borderColor = "#dc3545"; // red
        if (similarity >= 75) borderColor = "#28a745"; // green
        else if (similarity >= 45) borderColor = "#ffc107"; // yellow

        resultsDiv.innerHTML += `
            <div class="card" style="border-left: 4px solid ${borderColor};">
                <h3>
                    ${student.name} (ID: ${student.id})
                    <span class="badge ${badgeClass}">${simText}</span>
                </h3>

                <p><b>Skills:</b> ${student.skills}</p>
                <p><b>Project:</b> ${student.project_title}</p>
                <p>${student.project_description}</p>
                <p><b>Passing Year:</b> ${student.passing_year}</p>
            </div>
        `;
    });
}
