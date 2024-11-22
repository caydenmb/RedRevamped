async function fetchData() {
    try {
        const response = await fetch("/data");
        const data = await response.json();
        console.log("Fetched Data:", data);
        updateLeaderboard("shuffle", data.shuffle);
        updateLeaderboard("chicken", data.chicken);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

function updateLeaderboard(race, data) {
    const top3Container = document.getElementById(`${race}-top-3`);
    const standingsContainer = document.getElementById(`${race}-standings`);

    top3Container.innerHTML = "";
    standingsContainer.innerHTML = "";

    if (data.length) {
        data.slice(0, 3).forEach((user, index) => {
            const div = document.createElement("div");
            div.innerHTML = `<h3>${index + 1}: ${user.displayName}</h3><p>$${user.wager.toLocaleString()}</p>`;
            top3Container.appendChild(div);
        });

        data.slice(3).forEach((user, index) => {
            const div = document.createElement("div");
            div.innerHTML = `<p>${index + 4}: ${user.displayName} - $${user.wager.toLocaleString()}</p>`;
            standingsContainer.appendChild(div);
        });
    } else {
        top3Container.innerHTML = "<p>No data available.</p>";
        standingsContainer.innerHTML = "";
    }
}

async function toggleRace(race) {
    try {
        const response = await fetch(`/toggle/${race}`, { method: "POST" });
        const data = await response.json();
        console.log(`${race} toggled:`, data);
        fetchData(); // Refresh data after toggling
    } catch (error) {
        console.error("Error toggling race:", error);
    }
}

setInterval(fetchData, 90000); // Refresh every 90 seconds
fetchData();
