import math
from typing import List, Optional, Dict, Any
import logging 
logging.basicConfig(level=logging.INFO)
CLINICS_DATA = [
    {
        "id": "sgh",
        "name": "Singapore General Hospital",
        "department": "Dermatology Department",
        "address": "Outram Road, Singapore 169608",
        "phone": "+65 6222 3322",
        "website": "https://www.sgh.com.sg",
        "rating": 4.2,
        "lat": 1.2789,
        "lng": 103.8345,
        "specialties": ["General Dermatology", "Skin Cancer", "Psoriasis"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 5:30 PM",
            "tuesday": "8:00 AM - 5:30 PM",
            "wednesday": "8:00 AM - 5:30 PM",
            "thursday": "8:00 AM - 5:30 PM",
            "friday": "8:00 AM - 5:30 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "nsc",
        "name": "National Skin Centre",
        "department": "Specialist Dermatology Clinic",
        "address": "1 Mandalay Road, Singapore 308205",
        "phone": "+65 6350 6868",
        "website": "https://www.nsc.com.sg",
        "rating": 4.5,
        "lat": 1.3211,
        "lng": 103.8483,
        "specialties": ["Dermatology", "Skin Surgery", "Laser Treatment"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 5:30 PM",
            "tuesday": "8:00 AM - 5:30 PM",
            "wednesday": "8:00 AM - 5:30 PM",
            "thursday": "8:00 AM - 5:30 PM",
            "friday": "8:00 AM - 5:30 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "memc",
        "name": "Mount Elizabeth Medical Centre",
        "department": "Private Dermatology Practice",
        "address": "3 Mount Elizabeth, Singapore 228510",
        "phone": "+65 6731 2218",
        "website": "https://www.mountelizabeth.com.sg",
        "rating": 4.3,
        "lat": 1.3048,
        "lng": 103.8341,
        "specialties": ["Cosmetic Dermatology", "Anti-aging", "Acne Treatment"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 6:00 PM",
            "tuesday": "9:00 AM - 6:00 PM",
            "wednesday": "9:00 AM - 6:00 PM",
            "thursday": "9:00 AM - 6:00 PM",
            "friday": "9:00 AM - 6:00 PM",
            "saturday": "9:00 AM - 1:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "raffles",
        "name": "Raffles Hospital",
        "department": "Dermatology & Skin Clinic",
        "address": "585 North Bridge Road, Singapore 188770",
        "phone": "+65 6311 1111",
        "website": "https://www.rafflesmedicalgroup.com",
        "rating": 4.4,
        "lat": 1.3000,
        "lng": 103.8580,
        "specialties": ["General Dermatology", "Pediatric Dermatology", "Allergy Testing"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 5:30 PM",
            "tuesday": "8:30 AM - 5:30 PM",
            "wednesday": "8:30 AM - 5:30 PM",
            "thursday": "8:30 AM - 5:30 PM",
            "friday": "8:30 AM - 5:30 PM",
            "saturday": "8:30 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "ttsh",
        "name": "Tan Tock Seng Hospital",
        "department": "Dermatology Department",
        "address": "11 Jalan Tan Tock Seng, Singapore 308433",
        "phone": "+65 6357 7000",
        "website": "https://www.ttsh.com.sg",
        "rating": 4.1,
        "lat": 1.3210,
        "lng": 103.8456,
        "specialties": ["General Dermatology", "Infectious Skin Diseases", "Immunodermatology"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 5:00 PM",
            "tuesday": "8:00 AM - 5:00 PM",
            "wednesday": "8:00 AM - 5:00 PM",
            "thursday": "8:00 AM - 5:00 PM",
            "friday": "8:00 AM - 5:00 PM",
            "saturday": "8:00 AM - 12:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "nuh",
        "name": "National University Hospital",
        "department": "Division of Dermatology",
        "address": "5 Lower Kent Ridge Road, Singapore 119074",
        "phone": "+65 6779 5555",
        "website": "https://www.nuh.com.sg",
        "rating": 4.3,
        "lat": 1.2936,
        "lng": 103.7831,
        "specialties": ["Academic Dermatology", "Complex Cases", "Research Studies"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 5:30 PM",
            "tuesday": "8:30 AM - 5:30 PM",
            "wednesday": "8:30 AM - 5:30 PM",
            "thursday": "8:30 AM - 5:30 PM",
            "friday": "8:30 AM - 5:30 PM",
            "saturday": "8:30 AM - 12:30 PM",
            "sunday": "Closed"
        }
    }
]

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance


def validate_coordinates(lat: float, lng: float) -> tuple[bool, Optional[str]]:
    if not (-90 <= lat <= 90):
        return False, "Invalid latitude. Must be between -90 and 90"
    if not (-180 <= lng <= 180):
        return False, "Invalid longitude. Must be between -180 and 180"
    return True, None


def find_nearest_clinics(
    user_lat: float, 
    user_lng: float, 
) -> List[Dict[str, Any]]:
    clinics = CLINICS_DATA
    clinics_with_distance = []
 
    
    for clinic in clinics:
        clinic_copy = clinic.copy()
        distance = calculate_distance(
            user_lat, user_lng, 
            clinic['lat'], clinic['lng']
        )        
        clinic_copy['distance_km'] = round(distance, 2)
        clinic_copy['distance_text'] = f"{round(distance, 1)} km away"
        clinic_copy['rating'] = f"⭐ {clinic['rating']}"
        
        clinics_with_distance.append(clinic_copy)
    
    clinics_with_distance.sort(key=lambda x: x['distance_km'])
    return clinics_with_distance
