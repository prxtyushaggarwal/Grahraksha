"""
Indian Mountain Road Networks, Historical Landslide Datasets (GSI & ISRO Bhuvan),
and Sensor Telemetry Configurations for GiriRaksha.
"""

# Major Indian Mountain Highway Corridors
CORRIDORS = {
    "NH-58": {
        "name": "NH-58 / NH-107 (Rishikesh - Badrinath / Kedarnath Highway)",
        "state": "Uttarakhand",
        "region": "Garhwal Himalayas",
        "danger_level": "Critical",
        "origin": {"name": "Rishikesh", "lat": 30.0869, "lon": 78.2676},
        "destination": {"name": "Badrinath", "lat": 30.7433, "lon": 79.4938},
        "waypoints": [
            {"name": "Rishikesh", "lat": 30.0869, "lon": 78.2676, "elevation_m": 372, "slope_deg": 12},
            {"name": "Byasi", "lat": 30.0898, "lon": 78.4382, "elevation_m": 460, "slope_deg": 28},
            {"name": "Devprayag (Alaknanda Confluence)", "lat": 30.1459, "lon": 78.5989, "elevation_m": 610, "slope_deg": 35},
            {"name": "Srinagar Garhwal", "lat": 30.2224, "lon": 78.7844, "elevation_m": 560, "slope_deg": 22},
            {"name": "Sirobagarh (Chronic Landslide Zone)", "lat": 30.2451, "lon": 78.8920, "elevation_m": 720, "slope_deg": 52},
            {"name": "Rudraprayag", "lat": 30.2858, "lon": 78.9811, "elevation_m": 895, "slope_deg": 38},
            {"name": "Karnaprayag", "lat": 30.2600, "lon": 79.2180, "elevation_m": 1050, "slope_deg": 40},
            {"name": "Nandaprayag", "lat": 30.3312, "lon": 79.3242, "elevation_m": 1180, "slope_deg": 34},
            {"name": "Chamoli Gopeshwar", "lat": 30.4072, "lon": 79.3308, "elevation_m": 1300, "slope_deg": 39},
            {"name": "Helang Active Slide Zone", "lat": 30.5284, "lon": 79.5162, "elevation_m": 1550, "slope_deg": 56},
            {"name": "Joshimath Subsidence Zone", "lat": 30.5566, "lon": 79.5667, "elevation_m": 1890, "slope_deg": 46},
            {"name": "Lambagar Torrential Slide", "lat": 30.6510, "lon": 79.5390, "elevation_m": 2400, "slope_deg": 54},
            {"name": "Hanuman Chatti", "lat": 30.7020, "lon": 79.5080, "elevation_m": 2750, "slope_deg": 41},
            {"name": "Badrinath Temple Zone", "lat": 30.7433, "lon": 79.4938, "elevation_m": 3133, "slope_deg": 30}
        ]
    },
    "NH-44": {
        "name": "NH-44 (Jammu - Srinagar National Highway)",
        "state": "Jammu & Kashmir",
        "region": "Pir Panjal Range",
        "danger_level": "High",
        "origin": {"name": "Jammu", "lat": 32.7266, "lon": 74.8570},
        "destination": {"name": "Srinagar", "lat": 34.0837, "lon": 74.7973},
        "waypoints": [
            {"name": "Jammu Tawi", "lat": 32.7266, "lon": 74.8570, "elevation_m": 327, "slope_deg": 10},
            {"name": "Udhampur", "lat": 32.9250, "lon": 75.1416, "elevation_m": 756, "slope_deg": 24},
            {"name": "Chenani-Nashri Tunnel Portal", "lat": 33.0560, "lon": 75.2910, "elevation_m": 1200, "slope_deg": 32},
            {"name": "Chanderkote", "lat": 33.2010, "lon": 75.1950, "elevation_m": 880, "slope_deg": 37},
            {"name": "Ramban District HQ", "lat": 33.2428, "lon": 75.2444, "elevation_m": 1150, "slope_deg": 43},
            {"name": "Mehar Active Shooting Stone Zone", "lat": 33.2562, "lon": 75.2415, "elevation_m": 1180, "slope_deg": 55},
            {"name": "Cafeteria Morh Slide", "lat": 33.2710, "lon": 75.2380, "elevation_m": 1220, "slope_deg": 58},
            {"name": "Digdol Rockfall Zone", "lat": 33.3120, "lon": 75.2010, "elevation_m": 1350, "slope_deg": 61},
            {"name": "Panthyal (Historic Shooting Stones)", "lat": 33.3340, "lon": 75.1900, "elevation_m": 1420, "slope_deg": 63},
            {"name": "Ramsu", "lat": 33.3620, "lon": 75.1850, "elevation_m": 1560, "slope_deg": 45},
            {"name": "Banihal", "lat": 33.4286, "lon": 75.2033, "elevation_m": 1730, "slope_deg": 33},
            {"name": "Qazigund", "lat": 33.5939, "lon": 75.1614, "elevation_m": 1670, "slope_deg": 18},
            {"name": "Anantnag", "lat": 33.7311, "lon": 75.1522, "elevation_m": 1600, "slope_deg": 12},
            {"name": "Srinagar Lal Chowk", "lat": 34.0837, "lon": 74.7973, "elevation_m": 1585, "slope_deg": 8}
        ]
    },
    "NH-5": {
        "name": "NH-5 (Hindustan-Tibet Road: Shimla - Kinnaur)",
        "state": "Himachal Pradesh",
        "region": "Kinnaur Himalayas",
        "danger_level": "Critical",
        "origin": {"name": "Shimla", "lat": 31.1048, "lon": 77.1734},
        "destination": {"name": "Reckong Peo (Kinnaur)", "lat": 31.5395, "lon": 78.2754},
        "waypoints": [
            {"name": "Shimla Mall Road", "lat": 31.1048, "lon": 77.1734, "elevation_m": 2206, "slope_deg": 25},
            {"name": "Kufri", "lat": 31.0980, "lon": 77.2678, "elevation_m": 2630, "slope_deg": 29},
            {"name": "Narkanda", "lat": 31.2590, "lon": 77.4578, "elevation_m": 2708, "slope_deg": 32},
            {"name": "Kingal", "lat": 31.3210, "lon": 77.5120, "elevation_m": 1400, "slope_deg": 41},
            {"name": "Rampur Bushahr", "lat": 31.4497, "lon": 77.6300, "elevation_m": 1005, "slope_deg": 38},
            {"name": "Jhakri Hydro Project", "lat": 31.4920, "lon": 77.7010, "elevation_m": 1150, "slope_deg": 45},
            {"name": "Jeori Hotspring Pass", "lat": 31.5270, "lon": 77.7850, "elevation_m": 1400, "slope_deg": 48},
            {"name": "Bhabanagar", "lat": 31.5640, "lon": 77.9320, "elevation_m": 1520, "slope_deg": 44},
            {"name": "Nigulsari (Tragic 2021 Landslide Site)", "lat": 31.5798, "lon": 77.9890, "elevation_m": 1780, "slope_deg": 62},
            {"name": "Urni Overhanging Cliff", "lat": 31.5420, "lon": 78.1430, "elevation_m": 1950, "slope_deg": 59},
            {"name": "Tapri", "lat": 31.5160, "lon": 78.1880, "elevation_m": 1650, "slope_deg": 49},
            {"name": "Karcham Confluence", "lat": 31.5010, "lon": 78.2160, "elevation_m": 1800, "slope_deg": 42},
            {"name": "Powari", "lat": 31.5280, "lon": 78.2610, "elevation_m": 1900, "slope_deg": 40},
            {"name": "Reckong Peo / Kalpa", "lat": 31.5395, "lon": 78.2754, "elevation_m": 2290, "slope_deg": 36}
        ]
    },
    "NH-10": {
        "name": "NH-10 (Siliguri - Kalimpong - Gangtok)",
        "state": "West Bengal / Sikkim",
        "region": "Eastern Himalayas",
        "danger_level": "High",
        "origin": {"name": "Siliguri", "lat": 26.7271, "lon": 88.3953},
        "destination": {"name": "Gangtok", "lat": 27.3389, "lon": 88.6065},
        "waypoints": [
            {"name": "Siliguri Junction", "lat": 26.7271, "lon": 88.3953, "elevation_m": 125, "slope_deg": 5},
            {"name": "Sevoke Coronation Bridge", "lat": 26.8830, "lon": 88.4730, "elevation_m": 230, "slope_deg": 33},
            {"name": "Kalijhora Rockslide Zone", "lat": 26.9380, "lon": 88.4550, "elevation_m": 310, "slope_deg": 49},
            {"name": "Setijhora", "lat": 26.9650, "lon": 88.4410, "elevation_m": 340, "slope_deg": 52},
            {"name": "29th Mile (Chronic Breached Zone)", "lat": 27.0210, "lon": 88.4350, "elevation_m": 420, "slope_deg": 58},
            {"name": "Teesta Bazaar", "lat": 27.0650, "lon": 88.4280, "elevation_m": 210, "slope_deg": 44},
            {"name": "Melli Border Checkpost", "lat": 27.0940, "lon": 88.4520, "elevation_m": 240, "slope_deg": 38},
            {"name": "Rangpo (Sikkim Entry)", "lat": 27.1770, "lon": 88.5310, "elevation_m": 330, "slope_deg": 31},
            {"name": "Singtam", "lat": 27.2340, "lon": 88.5020, "elevation_m": 400, "slope_deg": 36},
            {"name": "Ranipool", "lat": 27.2910, "lon": 88.5830, "elevation_m": 880, "slope_deg": 34},
            {"name": "Gangtok MG Marg", "lat": 27.3389, "lon": 88.6065, "elevation_m": 1650, "slope_deg": 28}
        ]
    },
    "NH-766": {
        "name": "NH-766 / Thamarassery Churam & Wayanad Ghats",
        "state": "Kerala",
        "region": "Western Ghats",
        "danger_level": "High",
        "origin": {"name": "Kozhikode", "lat": 11.2588, "lon": 75.7804},
        "destination": {"name": "Kalpetta (Wayanad)", "lat": 11.6103, "lon": 76.0827},
        "waypoints": [
            {"name": "Kozhikode Beach", "lat": 11.2588, "lon": 75.7804, "elevation_m": 15, "slope_deg": 4},
            {"name": "Kunnamangalam", "lat": 11.3060, "lon": 75.8770, "elevation_m": 48, "slope_deg": 8},
            {"name": "Thamarassery Town", "lat": 11.4170, "lon": 75.9340, "elevation_m": 85, "slope_deg": 15},
            {"name": "Adivaram (Foot of Ghat Pass)", "lat": 11.4920, "lon": 76.0020, "elevation_m": 160, "slope_deg": 29},
            {"name": "Churam Hairpin Bend 5", "lat": 11.5120, "lon": 76.0210, "elevation_m": 480, "slope_deg": 47},
            {"name": "Churam Hairpin Bend 9 (View Point)", "lat": 11.5280, "lon": 76.0280, "elevation_m": 720, "slope_deg": 53},
            {"name": "Lakkidi Pass (Gateway of Wayanad)", "lat": 11.5150, "lon": 76.0400, "elevation_m": 700, "slope_deg": 36},
            {"name": "Vythiri Rain Shadow Ridge", "lat": 11.5510, "lon": 76.0420, "elevation_m": 750, "slope_deg": 39},
            {"name": "Chooralmala-Mundakkai High Susceptibility Sector", "lat": 11.5240, "lon": 76.1550, "elevation_m": 940, "slope_deg": 57},
            {"name": "Kalpetta Town", "lat": 11.6103, "lon": 76.0827, "elevation_m": 780, "slope_deg": 20}
        ]
    }
}

# Real-time Hazard Watch Points (High-Priority Sensors & Warning Nodes)
REALTIME_HAZARDS = [
    {
        "id": "HAZ-UK-01",
        "title": "Sirobagarh Chronic Slide",
        "corridor": "NH-58 Rishikesh-Badrinath",
        "state": "Uttarakhand",
        "lat": 30.2451,
        "lon": 78.8920,
        "severity": "Severe",
        "risk_score": 88,
        "slope_deg": 52.4,
        "soil_moisture_pct": 86.5,
        "rainfall_3d_mm": 142.8,
        "rainfall_forecast_24h_mm": 64.0,
        "sensor_status": "CRITICAL_TILT_EXCEEDED",
        "displacement_rate_mm_hr": 4.2,
        "road_status": "Traffic restricted to one lane; SDRF standby",
        "last_updated": "2026-09-10 13:45 IST"
    },
    {
        "id": "HAZ-HP-02",
        "title": "Nigulsari Rockfall & Debris Flow Zone",
        "corridor": "NH-5 Hindustan-Tibet Road",
        "state": "Himachal Pradesh",
        "lat": 31.5798,
        "lon": 77.9890,
        "severity": "Severe",
        "risk_score": 92,
        "slope_deg": 61.8,
        "soil_moisture_pct": 91.2,
        "rainfall_3d_mm": 185.0,
        "rainfall_forecast_24h_mm": 78.5,
        "sensor_status": "PIEZOMETER_SATURATION_SPIKE",
        "displacement_rate_mm_hr": 6.8,
        "road_status": "Red Alert: Night travel prohibited; heavy rockfall",
        "last_updated": "2026-09-10 14:00 IST"
    },
    {
        "id": "HAZ-JK-03",
        "title": "Panthyal - Mehar Shooting Stone Corridor",
        "corridor": "NH-44 Jammu-Srinagar",
        "state": "Jammu & Kashmir",
        "lat": 33.3340,
        "lon": 75.1900,
        "severity": "High",
        "risk_score": 79,
        "slope_deg": 63.0,
        "soil_moisture_pct": 74.0,
        "rainfall_3d_mm": 110.4,
        "rainfall_forecast_24h_mm": 45.0,
        "sensor_status": "ACOUSTIC_EMISSION_DETECTED",
        "displacement_rate_mm_hr": 2.9,
        "road_status": "Convoy escorted; steel shed maintenance active",
        "last_updated": "2026-09-10 13:30 IST"
    },
    {
        "id": "HAZ-SK-04",
        "title": "29th Mile Teesta Gorge Slide",
        "corridor": "NH-10 Siliguri-Gangtok",
        "state": "West Bengal / Sikkim",
        "lat": 27.0210,
        "lon": 88.4350,
        "severity": "High",
        "risk_score": 75,
        "slope_deg": 57.5,
        "soil_moisture_pct": 82.0,
        "rainfall_3d_mm": 164.2,
        "rainfall_forecast_24h_mm": 52.0,
        "sensor_status": "RIVER_TOE_EROSION_ELEVATED",
        "displacement_rate_mm_hr": 3.1,
        "road_status": "Heavy commercial vehicles diverted via Lava-Gorubathan",
        "last_updated": "2026-09-10 12:50 IST"
    },
    {
        "id": "HAZ-KL-05",
        "title": "Chooralmala Debris Sector",
        "corridor": "NH-766 Wayanad Ghats",
        "state": "Kerala",
        "lat": 11.5240,
        "lon": 76.1550,
        "severity": "Severe",
        "risk_score": 85,
        "slope_deg": 56.8,
        "soil_moisture_pct": 94.1,
        "rainfall_3d_mm": 210.6,
        "rainfall_forecast_24h_mm": 85.0,
        "sensor_status": "PORE_WATER_PRESSURE_THRESHOLD",
        "displacement_rate_mm_hr": 5.4,
        "road_status": "Disaster Response Force on site; early warning sirens armed",
        "last_updated": "2026-09-10 13:55 IST"
    },
    {
        "id": "HAZ-AS-06",
        "title": "Bongaigaon Valley Slip (GSI 2023 Inventory)",
        "corridor": "Assam Foothills Corridor",
        "state": "Assam",
        "lat": 26.4056,
        "lon": 90.5785,
        "severity": "Moderate",
        "risk_score": 58,
        "slope_deg": 38.0,
        "soil_moisture_pct": 69.5,
        "rainfall_3d_mm": 88.0,
        "rainfall_forecast_24h_mm": 35.0,
        "sensor_status": "NORMAL_MONITORING",
        "displacement_rate_mm_hr": 0.8,
        "road_status": "Normal transit with cautionary speed limit (30 km/h)",
        "last_updated": "2026-09-10 11:20 IST"
    }
]

# 72-Hour Threat Forecast Database for Regions
THREAT_FORECAST_72H = [
    {
        "region": "Garhwal & Kumaon Himalayas (Uttarakhand)",
        "corridor": "NH-58 & NH-107",
        "points": [
            {"name": "Chamoli-Joshimath", "lat": 30.5566, "lon": 79.5667, "h0_risk": 55, "h24_risk": 72, "h48_risk": 86, "h72_risk": 70, "predicted_rainfall_mm": 112},
            {"name": "Devprayag-Sirobagarh", "lat": 30.2451, "lon": 78.8920, "h0_risk": 68, "h24_risk": 85, "h48_risk": 91, "h72_risk": 65, "predicted_rainfall_mm": 135},
            {"name": "Lambagar-Badrinath", "lat": 30.6510, "lon": 79.5390, "h0_risk": 60, "h24_risk": 78, "h48_risk": 89, "h72_risk": 75, "predicted_rainfall_mm": 128}
        ]
    },
    {
        "region": "Kinnaur & Kullu High Belts (Himachal Pradesh)",
        "corridor": "NH-5 & NH-3",
        "points": [
            {"name": "Nigulsari-Urni", "lat": 31.5798, "lon": 77.9890, "h0_risk": 75, "h24_risk": 92, "h48_risk": 96, "h72_risk": 82, "predicted_rainfall_mm": 160},
            {"name": "Rampur-Jhakri", "lat": 31.4920, "lon": 77.7010, "h0_risk": 48, "h24_risk": 66, "h48_risk": 79, "h72_risk": 62, "predicted_rainfall_mm": 95}
        ]
    },
    {
        "region": "Pir Panjal & Ramban Sector (Jammu & Kashmir)",
        "corridor": "NH-44",
        "points": [
            {"name": "Ramban-Banihal Corridor", "lat": 33.3340, "lon": 75.1900, "h0_risk": 62, "h24_risk": 79, "h48_risk": 84, "h72_risk": 68, "predicted_rainfall_mm": 105},
            {"name": "Nashri-Chanderkote", "lat": 33.1500, "lon": 75.2200, "h0_risk": 42, "h24_risk": 58, "h48_risk": 65, "h72_risk": 50, "predicted_rainfall_mm": 72}
        ]
    },
    {
        "region": "Teesta River Valley (Sikkim / West Bengal)",
        "corridor": "NH-10",
        "points": [
            {"name": "Kalijhora to 29th Mile", "lat": 27.0210, "lon": 88.4350, "h0_risk": 64, "h24_risk": 81, "h48_risk": 88, "h72_risk": 74, "predicted_rainfall_mm": 145}
        ]
    },
    {
        "region": "Wayanad Western Ghats Ridge (Kerala)",
        "corridor": "NH-766",
        "points": [
            {"name": "Thamarassery Churam - Chooralmala", "lat": 11.5240, "lon": 76.1550, "h0_risk": 70, "h24_risk": 88, "h48_risk": 93, "h72_risk": 80, "predicted_rainfall_mm": 190}
        ]
    }
]
