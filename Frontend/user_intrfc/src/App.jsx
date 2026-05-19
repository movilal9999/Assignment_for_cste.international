import { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function App() {
  const [itemName, setItemName] = useState('');
  const [results, setResults] = useState([]);
  const [userLocation, setUserLocation] = useState(null);   // null = not set yet
  const [loading, setLoading] = useState(false);
  const [mapCenter, setMapCenter] = useState([28.6139, 77.2090]); // Default: Delhi (India Gate)


  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const loc = {
            lat: position.coords.latitude,
            lon: position.coords.longitude
          };
          setUserLocation(loc);
          setMapCenter([loc.lat, loc.lon]);
          console.log("Auto location got:", loc);
        },
        (error) => {
          console.log("Location denied or error:", error.message);
          // Do nothing - user can click manual button
        }
      );
    }
  }, []);

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const loc = { lat: position.coords.latitude, lon: position.coords.longitude };
          setUserLocation(loc);
          setMapCenter([loc.lat, loc.lon]);
          alert("Location updated successfully!");
        },
        (error) => {
          alert("Could not get location. Please allow permission or use default Delhi location.");
        }
      );
    } else {
      alert("Geolocation is not supported by your browser.");
    }
  };

  const handleSearch = async () => {
    console.log("Enter name of items requires")
    if (!itemName.trim()) {
      alert("Please enter item name (e.g. A4 notebook)");
      return;
    }

    // Use default Delhi location if user didn't allow
    const searchLat = userLocation ? userLocation.lat : 28.6139;
    const searchLon = userLocation ? userLocation.lon : 77.2090;

    setLoading(true);
    setResults([]);

    try {
      const res = await axios.get(`/api/search`, {
        params: { 
          item_name: itemName.trim(), 
          user_lat: searchLat, 
          user_lon: searchLon 
        }
      });

      if (res.data.results && res.data.results.length > 0) {
        setResults(res.data.results);
      } else {
        alert("No shops found near you. Try a different item or check spelling.");
      }
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Server error. Make sure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <h1 className="text-4xl font-bold text-emerald-600 mb-6 text-center">
        InstantMarket 🛒 - Find Nearby Shops
      </h1>

      <div className="max-w-2xl mx-auto bg-white p-6 rounded-3xl shadow">
        <div className="flex gap-3 mb-4">
          <input
            type="text"
            placeholder="What do you need urgently? (A4 notebook)"
            value={itemName}
            onChange={(e) => setItemName(e.target.value)}
            className="flex-1 p-4 text-lg border rounded-2xl focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <button 
            onClick={handleSearch}
            disabled={loading}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-4 rounded-2xl font-semibold disabled:opacity-50"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>

        <button
          onClick={getCurrentLocation}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-2xl font-medium mb-4"
        >
          Use My Current Location (Allow if asked)
        </button>

        <p className="text-center text-sm text-gray-500">
          {userLocation 
            ? `Using your location (${userLocation.lat.toFixed(3)}, ${userLocation.lon.toFixed(3)})` 
            : "Using default Delhi location. Click above to use your exact location."}
        </p>
      </div>

      {/* Results + Map */}
      {results.length > 0 && (
        <div className="mt-8 max-w-4xl mx-auto">
          {/* Map */}
          <MapContainer center={mapCenter} zoom={13} className="h-96 w-full rounded-3xl shadow-lg mb-6">
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {results.map((r, index) => (
              <Marker key={index} position={[28.6, 77.2]}> {/* Replace with real shop lat/lon later */}
                <Popup>
                  <b>{r.shop_name}</b><br />
                  {r.address}<br />
                  ₹{r.price} • {r.distance_km} km
                </Popup>
              </Marker>
            ))}
          </MapContainer>

          {/* Shop List */}
          <div className="space-y-4">
            {results.map((r, index) => (
              <div key={index} className="bg-white p-6 rounded-3xl shadow flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <h3 className="font-semibold text-xl">{r.shop_name}</h3>
                  <p className="text-gray-600">{r.address}</p>
                  <p className="text-3xl font-bold text-emerald-600 mt-1">₹{r.price}</p>
                  <p className="text-sm text-gray-500">{r.distance_km} km away</p>
                </div>
                <a 
                  href={r.whatsapp_link} 
                  target="_blank" 
                  className="bg-green-500 hover:bg-green-600 text-white px-8 py-4 rounded-2xl font-medium whitespace-nowrap"
                >
                 Bargain on WhatsApp
                </a>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

