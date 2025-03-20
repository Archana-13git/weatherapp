document.getElementById("searchBtn").addEventListener("click", function () {
    const city = document.getElementById("cityInput").value;
    
    fetch(`/get_weather/?city=${city}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("City not found!");
            } else {
                // 🌤️ Update current weather
                document.getElementById("cityName").innerText = data.city;
                document.getElementById("temp").innerText = `${data.temperature}°C`;
                document.getElementById("humidity").innerText = `${data.humidity}%`;
                document.getElementById("description").innerText = data.description;
                const weatherIcon = document.getElementById("weatherIcon");
const weatherEmoji = document.getElementById("weatherEmoji");

const iconCode = data.icon;

// 🌦️ Map Weather Conditions to Emojis
const emojiMap = {
    "01d": "☀️",  "01n": "🌙",  
    "02d": "🌤️", "02n": "☁️",
    "03d": "☁️",  "03n": "☁️",
    "04d": "🌥️", "04n": "☁️",
    "09d": "🌧️", "09n": "🌧️",
    "10d": "🌦️", "10n": "🌧️",
    "11d": "⛈️", "11n": "⛈️",
    "13d": "❄️", "13n": "❄️",
    "50d": "🌫️", "50n": "🌫️"
};

// ✨ Update UI
if (emojiMap[iconCode]) {
    weatherEmoji.innerText = emojiMap[iconCode]; // Show Emoji
    weatherIcon.style.display = "none"; // Hide Image
} else {
    weatherIcon.src = "C:\\Users\\ethical\\Downloads\\weather1.png"; 
    weatherIcon.style.display = "block"; // Show Image
    weatherEmoji.style.display = "none"; // Hide Emoji
}

                

                // 🔥 Update 5-day forecast
                let forecastHTML = "";
                data.forecast.forEach((day, index) => {
                    forecastHTML += `
                        <div class="day" data-index="${index}">
                            ${new Date(day.date).toLocaleDateString("en-US", { weekday: "short" })} <br>
                            <img src="https://openweathermap.org/img/wn/${day.icon}.png" alt="Weather Icon"><br>
                            ${day.temperature}°C
                        </div>
                    `;
                });
                document.getElementById("forecastContainer").innerHTML = forecastHTML;

                // ⭐ Hover Effect: Show details when hovering over a day
                document.querySelectorAll(".day").forEach(day => {
                    day.addEventListener("mouseenter", function () {
                        const index = this.getAttribute("data-index");
                        document.getElementById("description").innerText = data.forecast[index].description;
                        document.getElementById("temp").innerText = `${data.forecast[index].temperature}°C`;
                    });

                    day.addEventListener("mouseleave", function () {
                        document.getElementById("description").innerText = data.description;
                        document.getElementById("temp").innerText = `${data.temperature}°C`;
                    });
                });
            }
        })
        .catch(error => console.error("Error fetching weather:", error));
});
