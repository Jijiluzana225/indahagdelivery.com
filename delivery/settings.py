{% extends 'store/base.html' %}

{% block content %}

<title>Store Location</title>
<style>
    /* General styles */
    body {
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f9f9f9;
        color: #333;
    }

    h1 {
        text-align: center;
        color: #444;
        margin-top: 20px;
    }

    .container {
        width: 90vw;
        margin: 0 auto;
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Map styles */
    #map {
        height: 600px;
        width: 100%;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 20px;
        border: 2px solid #ddd;
    }

    /* InfoBox styling */
    .info-box {
        text-align: center;
    }

    .info-box h3 {
        margin: 10px 0;
        font-size: 1.5rem;
        color: #555;
    }

    .info-box img {
        max-width: 150px;
        height: auto;
        border-radius: 10px;
        margin: 10px 0;
        cursor: pointer;
    }

    .info-box a {
        text-decoration: none;
        color: #007bff;
        font-weight: bold;
    }

    .info-box a:hover {
        color: #0056b3;
    }
</style>

<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAp38ahRHi7YSU7iDITGyvJSHT6uo8-RFE&callback=initMap&v=weekly" 
        async defer></script>
<script>
    let map, marker;

    function initMap() {
        // Store data passed from the Django context
        const store = {
            name: "{{ store.name|escapejs }}",
            location: "{{ store.location|escapejs }}",
            contact_number: "{{ store.contact_number|escapejs }}",
            facebook_page: "{{ store.facebook_page|escapejs }}",
            picture: "{{ store.picture.url|escapejs }}",
            id: "{{ store.id|escapejs }}"
        };

        const [latitude, longitude] = store.location.split(',');
        const storeLatLng = { lat: parseFloat(latitude), lng: parseFloat(longitude) };

        map = new google.maps.Map(document.getElementById("map"), {
            center: storeLatLng,
            zoom: 15,
        });

        marker = new google.maps.Marker({
            position: storeLatLng,
            map: map,
            title: store.name,
        });

        const infoWindowContent = `
            <div class="info-box">
                <h3>${store.name}</h3>
                <a href="#" onclick="openModal('${store.picture}')">
                    <img src="${store.picture}" alt="${store.name}" class="store-img">
                </a>
                <p><strong>Contact:</strong> ${store.contact_number}</p>
                <p><a href="${store.facebook_page}" target="_blank">Visit Facebook Page</a></p>
            </div>
        `;

        const infoWindow = new google.maps.InfoWindow({
            content: infoWindowContent,
        });

        infoWindow.open(map, marker);

        marker.addListener('click', () => {
            if (infoWindow.getMap()) {
                infoWindow.close();
            } else {
                infoWindow.open(map, marker);
            }
        });
    }

    // Function to open the modal and display the image in full screen
    function openModal(imageUrl) {
        const modal = document.getElementById('myModal');
        const modalImg = document.getElementById("img01");
        const span = document.getElementsByClassName("close")[0];

        modal.style.display = "block";
        modalImg.src = imageUrl;

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
            modal.style.display = "none";
        }
    }
</script>

<h1>Store Location</h1>
<div id="map"></div>

<!-- The Modal -->
<div id="myModal" class="modal" style="display: none;">
    <span class="close">&times;</span>
    <img class="modal-content" id="img01">
</div>

{% endblock content %}
