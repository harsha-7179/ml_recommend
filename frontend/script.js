async function getRecommendations() {
    const id = document.getElementById("studentId").value;
    const resultsDiv = document.getElementById("results");

    if (!id) {
        alert("Enter a Student ID");
        return;
    }

    resultsDiv.innerHTML = "<p>Loading...</p>";

    const res = await fetch(`/recommend?student_id=${id}`);
    const data = await res.json();

    resultsDiv.innerHTML = "";

    data.forEach(student => {
        resultsDiv.innerHTML += `
            <div class="card">
                <h3>${student.name} (ID: ${student.id})</h3>
                <p><b>Skills:</b> ${student.skills}</p>
                <p><b>Project:</b> ${student.project_title}</p>
                <p>${student.project_description}</p>
                <p><b>Passing Year:</b> ${student.passing_year}</p>
            </div>
        `;
    });
}
