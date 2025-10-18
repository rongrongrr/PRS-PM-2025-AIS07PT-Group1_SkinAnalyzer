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
    },

    {
        "id": "unity_medical",
        "name": "Unity Medical Centre",
        "department": "Dermatology Clinic",
        "address": "253 Jurong East Street 24 #01-205, Singapore 600253",
        "phone": "+65 6560 2200",
        "website": "https://www.unitymedical.sg",
        "rating": 3.9,
        "lat": 1.3419,
        "lng": 103.7423,
        "specialties": ["Family Dermatology", "Chronic Skin Conditions", "Pediatric Care"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 9:00 PM",
            "tuesday": "8:30 AM - 9:00 PM",
            "wednesday": "8:30 AM - 9:00 PM",
            "thursday": "8:30 AM - 9:00 PM",
            "friday": "8:30 AM - 9:00 PM",
            "saturday": "8:30 AM - 5:00 PM",
            "sunday": "8:30 AM - 1:00 PM"
        }
    },
    {
        "id": "pinnacle_family",
        "name": "Pinnacle Family Clinic",
        "department": "Family Medicine & Dermatology",
        "address": "5 Yung Ho Road #01-01, Singapore 618593",
        "phone": "+65 6261 5915",
        "website": "https://www.pinnaclefamilyclinic.com.sg",
        "rating": 4.0,
        "lat": 1.4093,
        "lng": 103.8990,
        "specialties": ["Family Medicine", "Chronic Care", "Skin Health"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 9:00 PM",
            "tuesday": "8:00 AM - 9:00 PM",
            "wednesday": "8:00 AM - 9:00 PM",
            "thursday": "8:00 AM - 9:00 PM",
            "friday": "8:00 AM - 9:00 PM",
            "saturday": "8:00 AM - 5:00 PM",
            "sunday": "8:00 AM - 1:00 PM"
        }
    },
    {
        "id": "pasir_ris_clinic",
        "name": "Pasir Ris Family Clinic",
        "department": "Family Medicine & Dermatology",
        "address": "446 Pasir Ris Drive 6 #01-122, Singapore 510446",
        "phone": "+65 6582 2255",
        "website": "https://www.pasirrisfc.com",
        "rating": 3.8,
        "lat": 1.3723,
        "lng": 103.9585,
        "specialties": ["General Practice", "Skin Conditions", "Pediatric Care"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "tuesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "wednesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "thursday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "friday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "saturday": "8:30 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "sembawang_medical",
        "name": "Sembawang Medical Centre",
        "department": "Family & Community Medicine",
        "address": "604 Sembawang Road #02-13, Singapore 758459",
        "phone": "+65 6753 2244",
        "website": "https://www.sembawangmedical.sg",
        "rating": 3.9,
        "lat": 1.4417,
        "lng": 103.8248,
        "specialties": ["Primary Healthcare", "Minor Surgery", "Skin Care"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 9:00 PM",
            "tuesday": "8:30 AM - 9:00 PM",
            "wednesday": "8:30 AM - 9:00 PM",
            "thursday": "8:30 AM - 9:00 PM",
            "friday": "8:30 AM - 9:00 PM",
            "saturday": "8:30 AM - 5:00 PM",
            "sunday": "8:30 AM - 1:00 PM"
        }
    },
    {
        "id": "bukit_panjang_clinic",
        "name": "Bukit Panjang Plaza Medical",
        "department": "Family Practice",
        "address": "1 Jelebu Road #04-08 Bukit Panjang Plaza, Singapore 677743",
        "phone": "+65 6769 6636",
        "website": "https://www.bppmedical.com",
        "rating": 3.7,
        "lat": 1.3804,
        "lng": 103.7638,
        "specialties": ["General Medicine", "Basic Dermatology", "Health Screening"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 9:00 PM",
            "tuesday": "9:00 AM - 9:00 PM",
            "wednesday": "9:00 AM - 9:00 PM",
            "thursday": "9:00 AM - 9:00 PM",
            "friday": "9:00 AM - 9:00 PM",
            "saturday": "9:00 AM - 9:00 PM",
            "sunday": "9:00 AM - 5:00 PM"
        }
    },
    {
        "id": "serangoon_medical",
        "name": "Serangoon Medical Clinic",
        "department": "General Practice & Skin Care",
        "address": "263 Serangoon Central #01-43, Singapore 550263",
        "phone": "+65 6280 8808",
        "website": "https://www.serangoonmedical.com.sg",
        "rating": 3.8,
        "lat": 1.3532,
        "lng": 103.8719,
        "specialties": ["Family Medicine", "Minor Procedures", "Vaccinations"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 10:00 PM",
            "tuesday": "8:00 AM - 10:00 PM",
            "wednesday": "8:00 AM - 10:00 PM",
            "thursday": "8:00 AM - 10:00 PM",
            "friday": "8:00 AM - 10:00 PM",
            "saturday": "8:00 AM - 10:00 PM",
            "sunday": "8:00 AM - 10:00 PM"
        }
    },
    {
        "id": "ang_mo_kio_medical",
        "name": "AMK Medical Centre",
        "department": "Multi-Disciplinary Clinic",
        "address": "720 Ang Mo Kio Avenue 6 #01-4162, Singapore 560720",
        "phone": "+65 6453 2268",
        "website": "https://www.amkmedical.com",
        "rating": 3.9,
        "lat": 1.3716,
        "lng": 103.8462,
        "specialties": ["General Practice", "Dermatology Referral", "Chronic Disease"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:30 PM",
            "tuesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:30 PM",
            "wednesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:30 PM",
            "thursday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:30 PM",
            "friday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:30 PM",
            "saturday": "8:30 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "choa_chu_kang_clinic",
        "name": "CCK Family Clinic",
        "department": "Family Medicine",
        "address": "309 Choa Chu Kang Avenue 4 #01-693, Singapore 680309",
        "phone": "+65 6763 1339",
        "website": "https://www.cckfamilyclinic.com",
        "rating": 3.8,
        "lat": 1.3877,
        "lng": 103.7425,
        "specialties": ["Primary Care", "Skin Problems", "Elderly Care"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 12:30 PM, 6:00 PM - 9:00 PM",
            "tuesday": "8:00 AM - 12:30 PM, 6:00 PM - 9:00 PM",
            "wednesday": "8:00 AM - 12:30 PM, 6:00 PM - 9:00 PM",
            "thursday": "8:00 AM - 12:30 PM, 6:00 PM - 9:00 PM",
            "friday": "8:00 AM - 12:30 PM, 6:00 PM - 9:00 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "8:00 AM - 12:30 PM"
        }
    },
    {
        "id": "tiong_bahru_medical",
        "name": "Tiong Bahru Medical Centre",
        "department": "General Practice & Wellness",
        "address": "302 Tiong Bahru Road #01-108, Singapore 168732",
        "phone": "+65 6271 1221",
        "website": "https://www.tiongbahrumedical.com",
        "rating": 4.0,
        "lat": 1.2859,
        "lng": 103.8287,
        "specialties": ["Family Medicine", "Health Screening", "Basic Dermatology"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 1:00 PM, 2:00 PM - 5:00 PM",
            "tuesday": "8:30 AM - 1:00 PM, 2:00 PM - 5:00 PM",
            "wednesday": "8:30 AM - 1:00 PM, 2:00 PM - 5:00 PM",
            "thursday": "8:30 AM - 1:00 PM, 2:00 PM - 5:00 PM",
            "friday": "8:30 AM - 1:00 PM, 2:00 PM - 5:00 PM",
            "saturday": "8:30 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "dover_medical",
        "name": "Dover Medical Centre",
        "department": "Family Practice",
        "address": "3 Dover Road #01-01, Singapore 138623",
        "phone": "+65 6773 3338",
        "website": "https://www.dovermedical.sg",
        "rating": 3.9,
        "lat": 1.3053,
        "lng": 103.7783,
        "specialties": ["General Practice", "Student Health", "Travel Medicine"],
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
        "id": "holland_village_medical",
        "name": "Holland Village Medical Centre",
        "department": "Family Medicine & Aesthetics",
        "address": "3 Lorong Liput, Singapore 277725",
        "phone": "+65 6468 7828",
        "website": "https://www.hollandvillagemedical.com",
        "rating": 4.1,
        "lat": 1.3107,
        "lng": 103.7953,
        "specialties": ["Family Medicine", "Aesthetic Services", "Health Screening"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 6:00 PM",
            "tuesday": "8:30 AM - 6:00 PM",
            "wednesday": "8:30 AM - 6:00 PM",
            "thursday": "8:30 AM - 6:00 PM",
            "friday": "8:30 AM - 6:00 PM",
            "saturday": "8:30 AM - 1:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "novena_medical",
        "name": "Novena Medical Center",
        "department": "Specialist Medical Services",
        "address": "10 Sinaran Drive #09-01 Square 2, Singapore 307506",
        "phone": "+65 6397 6210",
        "website": "https://www.novenamedicalcenter.com",
        "rating": 4.2,
        "lat": 1.3208,
        "lng": 103.8438,
        "specialties": ["Multi-Specialty", "Executive Health", "Dermatology"],
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
        "id": "aljunied_medical",
        "name": "Aljunied Medical Centre",
        "department": "General Practice",
        "address": "810 Geylang Road #01-02, Singapore 409286",
        "phone": "+65 6841 1223",
        "website": "https://www.aljuniedmedical.sg",
        "rating": 3.7,
        "lat": 1.3163,
        "lng": 103.8930,
        "specialties": ["Family Medicine", "Minor Surgery", "Basic Skin Care"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 9:00 PM",
            "tuesday": "8:30 AM - 9:00 PM",
            "wednesday": "8:30 AM - 9:00 PM",
            "thursday": "8:30 AM - 9:00 PM",
            "friday": "8:30 AM - 9:00 PM",
            "saturday": "8:30 AM - 5:00 PM",
            "sunday": "8:30 AM - 1:00 PM"
        }
    },
    {
        "id": "katong_medical",
        "name": "Katong Medical Centre",
        "department": "Family Medicine",
        "address": "121 East Coast Road, Singapore 428802",
        "phone": "+65 6344 2128",
        "website": "https://www.katongmedical.com",
        "rating": 3.9,
        "lat": 1.3052,
        "lng": 103.9050,
        "specialties": ["General Practice", "Travel Medicine", "Skin Conditions"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "tuesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "wednesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "thursday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "friday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "saturday": "8:30 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "west_coast_medical",
        "name": "West Coast Medical Centre",
        "department": "Family Practice",
        "address": "727 West Coast Road #01-108, Singapore 120727",
        "phone": "+65 6779 5532",
        "website": "https://www.westcoastmedical.sg",
        "rating": 3.8,
        "lat": 1.3031,
        "lng": 103.7642,
        "specialties": ["Family Medicine", "Preventive Care", "Skin Health"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "tuesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "wednesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "thursday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "friday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM, 6:30 PM - 9:00 PM",
            "saturday": "8:30 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "lavender_medical",
        "name": "Lavender Medical Centre",
        "department": "General Practice",
        "address": "803 King George's Avenue #01-208, Singapore 200803",
        "phone": "+65 6294 3328",
        "website": "https://www.lavendermedical.com.sg",
        "rating": 3.7,
        "lat": 1.3088,
        "lng": 103.8629,
        "specialties": ["Primary Care", "Chronic Disease", "Minor Dermatology"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 12:30 PM, 5:00 PM - 9:00 PM",
            "tuesday": "8:30 AM - 12:30 PM, 5:00 PM - 9:00 PM",
            "wednesday": "8:30 AM - 12:30 PM, 5:00 PM - 9:00 PM",
            "thursday": "8:30 AM - 12:30 PM, 5:00 PM - 9:00 PM",
            "friday": "8:30 AM - 12:30 PM, 5:00 PM - 9:00 PM",
            "saturday": "8:30 AM - 12:30 PM",
            "sunday": "8:30 AM - 12:30 PM"
        }
    }
]
        "lat": 1.3398,
        "lng": 103.7251,
        "specialties": ["Basic Dermatology", "Skin Infections", "Allergies"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 9:00 PM",
            "tuesday": "8:00 AM - 9:00 PM",
            "wednesday": "8:00 AM - 9:00 PM",
            "thursday": "8:00 AM - 9:00 PM",
            "friday": "8:00 AM - 9:00 PM",
            "saturday": "8:00 AM - 5:00 PM",
            "sunday": "8:00 AM - 1:00 PM"
        }
    },
    {
        "id": "silver_cross",
        "name": "Silver Cross Medical Centre",
        "department": "Multi-Specialty Clinic",
        "address": "2 Jurong East Street 21 #01-53 IMM Building, Singapore 609601",
        "phone": "+65 6567 1188",
        "website": "https://www.silvercrossmedical.com.sg",
        "rating": 4.1,
        "lat": 1.3348,
        "lng": 103.7470,
        "specialties": ["General Practice", "Dermatology Referrals", "Health Screening"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 9:00 PM",
            "tuesday": "9:00 AM - 9:00 PM",
            "wednesday": "9:00 AM - 9:00 PM",
            "thursday": "9:00 AM - 9:00 PM",
            "friday": "9:00 AM - 9:00 PM",
            "saturday": "9:00 AM - 9:00 PM",
            "sunday": "9:00 AM - 9:00 PM"
        }
    },
    {
        "id": "parkway_shenton_marina",
        "name": "Parkway Shenton Marina Bay",
        "department": "Executive Health Screening & Dermatology",
        "address": "6 Raffles Boulevard #02-10 Marina Square, Singapore 039594",
        "phone": "+65 6339 3319",
        "website": "https://www.parkwayshenton.com",
        "rating": 4.2,
        "lat": 1.2910,
        "lng": 103.8575,
        "specialties": ["Executive Health", "Skin Screening", "Preventive Care"],
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
        "id": "myhealth_medical",
        "name": "MyHealth Medical Centre",
        "department": "Family Medicine & Skin Care",
        "address": "16 Shaw Road #01-02 Singapore 367954",
        "phone": "+65 6281 3338",
        "website": "https://www.myhealthmedical.sg",
        "rating": 3.8,
        "lat": 1.3486,
        "lng": 103.8755,
        "specialties": ["General Practice", "Minor Dermatology", "Wellness"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "tuesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "wednesday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "thursday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "friday": "8:30 AM - 12:30 PM, 2:00 PM - 5:00 PM",
            "saturday": "8:30 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "lifescan_medical",
        "name": "Lifescan Medical Centre",
        "department": "Health Screening & Dermatology",
        "address": "587 Bukit Timah Road, Singapore 269707",
        "phone": "+65 6468 1633",
        "website": "https://www.lifescanmedical.sg",
        "rating": 4.0,
        "lat": 1.3334,
        "lng": 103.7883,
        "specialties": ["Health Screening", "Skin Checks", "Preventive Medicine"],
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
        "id": "minmed_clinic",
        "name": "Minmed Health Screeners",
        "department": "Screening & Dermatology Referral",
        "address": "7 Temasek Boulevard #02-05 Suntec Tower One, Singapore 038987",
        "phone": "+65 6705 8088",
        "website": "https://www.minmed.sg",
        "rating": 3.9,
        "lat": 1.2953,
        "lng": 103.8584,
        "specialties": ["Health Screening", "Basic Skin Care", "Referral Services"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 6:00 PM",
            "tuesday": "8:30 AM - 6:00 PM",
            "wednesday": "8:30 AM - 6:00 PM",
            "thursday": "8:30 AM - 6:00 PM",
            "friday": "8:30 AM - 6:00 PM",
            "saturday": "8:30 AM - 1:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "island_hospital",
        "name": "Island Hospital Singapore",
        "department": "Dermatology Department",
        "address": "1 Balmoral Park #01-09, Singapore 339487",
        "phone": "+65 6253 0000",
        "website": "https://www.islandhospital.sg",
        "rating": 4.1,
        "lat": 1.3233,
        "lng": 103.8468,
        "specialties": ["Medical Dermatology", "Surgical Dermatology", "Pediatric Skin"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 5:30 PM",
            "tuesday": "9:00 AM - 5:30 PM",
            "wednesday": "9:00 AM - 5:30 PM",
            "thursday": "9:00 AM - 5:30 PM",
            "friday": "9:00 AM - 5:30 PM",
            "saturday": "9:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "international_medical",
        "name": "International Medical Clinic",
        "department": "Multi-Specialty with Dermatology",
        "address": "1 Orchard Boulevard #14-06 Camden Medical Centre, Singapore 248649",
        "phone": "+65 6733 4440",
        "website": "https://www.imc-singapore.com",
        "rating": 4.3,
        "lat": 1.3041,
        "lng": 103.8316,
        "specialties": ["International Health", "Travel Medicine", "Skin Conditions"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 6:00 PM",
            "tuesday": "8:30 AM - 6:00 PM",
            "wednesday": "8:30 AM - 6:00 PM",
            "thursday": "8:30 AM - 6:00 PM",
            "friday": "8:30 AM - 6:00 PM",
            "saturday": "8:30 AM - 1:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "fullerton_health",
        "name": "Fullerton Health @ Raffles Place",
        "department": "Corporate Healthcare & Dermatology",
        "address": "1 Raffles Place Tower 2 #03-01, Singapore 048616",
        "phone": "+65 6333 3636",
        "website": "https://www.fullertonhealth.com",
        "rating": 4.0,
        "lat": 1.2844,
        "lng": 103.8510,
        "specialties": ["Corporate Health", "Occupational Dermatology", "Wellness"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 6:00 PM",
            "tuesday": "8:30 AM - 6:00 PM",
            "wednesday": "8:30 AM - 6:00 PM",
            "thursday": "8:30 AM - 6:00 PM",
            "friday": "8:30 AM - 6:00 PM",
            "saturday": "Closed",
            "sunday": "Closed"
        }
    },
    
    # Specialist Dermatology Practices
    {
        "id": "stephanie_ho",
        "name": "Dr Stephanie Ho Dermatology",
        "department": "Consultant Dermatologist",
        "address": "3 Mount Elizabeth #07-09, Singapore 228510",
        "phone": "+65 6734 9011",
        "website": "https://www.stephanieho.com.sg",
        "rating": 4.5,
        "lat": 1.3048,
        "lng": 103.8341,
        "specialties": ["Medical Dermatology", "Aesthetic Dermatology", "Laser Surgery"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 5:00 PM",
            "tuesday": "9:00 AM - 5:00 PM",
            "wednesday": "9:00 AM - 5:00 PM",
            "thursday": "9:00 AM - 5:00 PM",
            "friday": "9:00 AM - 5:00 PM",
            "saturday": "9:00 AM - 12:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "joyce_lim",
        "name": "Dr Joyce Lim Skin & Laser Clinic",
        "department": "Dermatology & Laser Surgery",
        "address": "6 Napier Road #07-13 Gleneagles Medical Centre, Singapore 258499",
        "phone": "+65 6472 2257",
        "website": "https://www.joycethelim.com",
        "rating": 4.4,
        "lat": 1.3078,
        "lng": 103.8201,
        "specialties": ["Laser Surgery", "Pigmentation Disorders", "Anti-Aging"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 5:30 PM",
            "tuesday": "9:00 AM - 5:30 PM",
            "wednesday": "9:00 AM - 5:30 PM",
            "thursday": "9:00 AM - 5:30 PM",
            "friday": "9:00 AM - 5:30 PM",
            "saturday": "9:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "mark_tang",
        "name": "Dr Mark Tang Dermatology",
        "department": "Specialist Dermatology Practice",
        "address": "3 Mount Elizabeth #13-14 Mount Elizabeth Medical Centre, Singapore 228510",
        "phone": "+65 6733 0519",
        "website": "https://www.marktangdermatology.com",
        "rating": 4.3,
        "lat": 1.3048,
        "lng": 103.8341,
        "specialties": ["Skin Cancer", "Complex Dermatology", "Immunodermatology"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 5:00 PM",
            "tuesday": "9:00 AM - 5:00 PM",
            "wednesday": "9:00 AM - 5:00 PM",
            "thursday": "9:00 AM - 5:00 PM",
            "friday": "9:00 AM - 5:00 PM",
            "saturday": "9:00 AM - 12:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "colin_theng",
        "name": "Dr Colin Theng Dermatology",
        "department": "Medical & Cosmetic Dermatology",
        "address": "38 Irrawaddy Road #06-21 Mount Elizabeth Novena, Singapore 329563",
        "phone": "+65 6262 6298",
        "website": "https://www.colinthengdermatology.com.sg",
        "rating": 4.4,
        "lat": 1.3216,
        "lng": 103.8433,
        "specialties": ["Psoriasis", "Eczema", "Aesthetic Procedures"],
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
        "id": "peter_lor",
        "name": "Dr Peter Lor Dermatology",
        "department": "Dermatology & Surgery",
        "address": "1 Orchard Boulevard #13-03 Camden Medical Centre, Singapore 248649",
        "phone": "+65 6735 1200",
        "website": "https://www.peterlordermatology.com",
        "rating": 4.2,
        "lat": 1.3041,
        "lng": 103.8316,
        "specialties": ["Skin Surgery", "Mole Removal", "Skin Cancer Screening"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 5:00 PM",
            "tuesday": "9:00 AM - 5:00 PM",
            "wednesday": "9:00 AM - 5:00 PM",
            "thursday": "9:00 AM - 5:00 PM",
            "friday": "9:00 AM - 5:00 PM",
            "saturday": "9:00 AM - 12:00 PM",
            "sunday": "Closed"
        }
    },
    
    # Community and Neighborhood Clinics
    {
        "id": "hougang_poly",
        "name": "Hougang Polyclinic",
        "department": "Family Medicine & Basic Dermatology",
        "address": "89 Hougang Avenue 4, Singapore 538829",
        "phone": "+65 6765 1121",
        "website": "https://www.nhgp.com.sg",
        "rating": 3.7,
        "lat": 1.3732,
        "lng": 103.8882,
        "specialties": ["Primary Care", "Basic Skin Conditions", "Referral Services"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 4:30 PM",
            "tuesday": "8:00 AM - 4:30 PM",
            "wednesday": "8:00 AM - 4:30 PM",
            "thursday": "8:00 AM - 4:30 PM",
            "friday": "8:00 AM - 4:30 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "toa_payoh_poly",
        "name": "Toa Payoh Polyclinic",
        "department": "Family Health & Dermatology Referral",
        "address": "2003 Toa Payoh Lorong 8, Singapore 319260",
        "phone": "+65 6354 3781",
        "website": "https://www.nhgp.com.sg",
        "rating": 3.8,
        "lat": 1.3404,
        "lng": 103.8563,
        "specialties": ["Primary Healthcare", "Common Skin Problems", "Health Education"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 4:30 PM",
            "tuesday": "8:00 AM - 4:30 PM",
            "wednesday": "8:00 AM - 4:30 PM",
            "thursday": "8:00 AM - 4:30 PM",
            "friday": "8:00 AM - 4:30 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "queenstown_poly",
        "name": "Queenstown Polyclinic",
        "department": "Multi-Disciplinary Healthcare",
        "address": "580 Stirling Road, Singapore 148874",
        "phone": "+65 6471 2282",
        "website": "https://www.singhealth.com.sg/polyclinics",
        "rating": 3.9,
        "lat": 1.2985,
        "lng": 103.8016,
        "specialties": ["Family Medicine", "Chronic Disease", "Basic Dermatology"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 4:30 PM",
            "tuesday": "8:00 AM - 4:30 PM",
            "wednesday": "8:00 AM - 4:30 PM",
            "thursday": "8:00 AM - 4:30 PM",
            "friday": "8:00 AM - 4:30 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "marine_parade_poly",
        "name": "Marine Parade Polyclinic",
        "department": "Primary Healthcare Services",
        "address": "80 Marine Parade Central, Singapore 440080",
        "phone": "+65 6344 6997",
        "website": "https://www.singhealth.com.sg/polyclinics",
        "rating": 3.8,
        "lat": 1.3028,
        "lng": 103.9074,
        "specialties": ["Family Medicine", "Geriatric Care", "Skin Health"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 4:30 PM",
            "tuesday": "8:00 AM - 4:30 PM",
            "wednesday": "8:00 AM - 4:30 PM",
            "thursday": "8:00 AM - 4:30 PM",
            "friday": "8:00 AM - 4:30 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "punggol_poly",
        "name": "Punggol Polyclinic",
        "department": "Family & Community Medicine",
        "address": "681 Punggol Drive, Singapore 820681",
        "phone": "+65 6643 6969",
        "website": "https://www.singhealth.com.sg/polyclinics",
        "rating": 3.9,
        "lat": 1.4041,
        "lng": 103.9124,
        "specialties": ["Primary Care", "Preventive Health", "Skin Conditions"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 4:30 PM",
            "tuesday": "8:00 AM - 4:30 PM",
            "wednesday": "8:00 AM - 4:30 PM",
            "thursday": "8:00 AM - 4:30 PM",
            "friday": "8:00 AM - 4:30 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    
    # Aesthetic and Wellness Centers
    {
        "id": "wellaholic",
        "name": "Wellaholic",
        "department": "Aesthetic & Wellness",
        "address": "435 Orchard Road Wisma Atria #04-09, Singapore 238877",
        "phone": "+65 8856 0000",
        "website": "https://www.wellaholic.com",
        "rating": 4.2,
        "lat": 1.3036,
        "lng": 103.8326,
        "specialties": ["Hair Removal", "Body Treatments", "Facial Services"],
        "insurance_accepted": False,
        "opening_hours": {
            "monday": "11:00 AM - 9:00 PM",
            "tuesday": "11:00 AM - 9:00 PM",
            "wednesday": "11:00 AM - 9:00 PM",
            "thursday": "11:00 AM - 9:00 PM",
            "friday": "11:00 AM - 9:00 PM",
            "saturday": "10:00 AM - 9:00 PM",
            "sunday": "10:00 AM - 9:00 PM"
        }
    },
    {
        "id": "kuko_beauty",
        "name": "Kuko Beauty",
        "department": "Medical Aesthetics",
        "address": "545 Orchard Road #02-28 Far East Shopping Centre, Singapore 238882",
        "phone": "+65 6738 2188",
        "website": "https://www.kukobeauty.com",
        "rating": 4.1,
        "lat": 1.3056,
        "lng": 103.8303,
        "specialties": ["Laser Treatments", "Skin Rejuvenation", "Body Contouring"],
        "insurance_accepted": False,
        "opening_hours": {
            "monday": "10:00 AM - 8:00 PM",
            "tuesday": "10:00 AM - 8:00 PM",
            "wednesday": "10:00 AM - 8:00 PM",
            "thursday": "10:00 AM - 8:00 PM",
            "friday": "10:00 AM - 8:00 PM",
            "saturday": "10:00 AM - 7:00 PM",
            "sunday": "10:00 AM - 7:00 PM"
        }
    },
    {
        "id": "aesthetic_central",
        "name": "Aesthetic Central Clinic",
        "department": "Medical Aesthetics",
        "address": "277 Orchard Road #02-11 Orchard Gateway, Singapore 238858",
        "phone": "+65 6735 7228",
        "website": "https://www.aestheticcentral.sg",
        "rating": 4.0,
        "lat": 1.3009,
        "lng": 103.8391,
        "specialties": ["Nose Thread Lift", "Chin Augmentation", "Skin Boosters"],
        "insurance_accepted": False,
        "opening_hours": {
            "monday": "10:00 AM - 7:00 PM",
            "tuesday": "10:00 AM - 7:00 PM",
            "wednesday": "10:00 AM - 7:00 PM",
            "thursday": "10:00 AM - 7:00 PM",
            "friday": "10:00 AM - 7:00 PM",
            "saturday": "10:00 AM - 5:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "skintech_medical",
        "name": "SkinTech Medical Aesthetics",
        "department": "Laser & Aesthetic Medicine",
        "address": "1 Grange Road #10-03 Orchard Building, Singapore 239693",
        "phone": "+65 6834 0788",
        "website": "https://www.skintechmedical.com",
        "rating": 4.3,
        "lat": 1.3015,
        "lng": 103.8357,
        "specialties": ["Pico Laser", "HIFU Treatment", "Cryolipolysis"],
        "insurance_accepted": False,
        "opening_hours": {
            "monday": "10:00 AM - 7:00 PM",
            "tuesday": "10:00 AM - 7:00 PM",
            "wednesday": "10:00 AM - 7:00 PM",
            "thursday": "10:00 AM - 7:00 PM",
            "friday": "10:00 AM - 7:00 PM",
            "saturday": "10:00 AM - 6:00 PM",
            "sunday": "Closed"
        }
    },
    
    # Regional Medical Centers
    {
        "id": "bishan_medical",
        "name": "OneCare Medical",
        "department": "Family Practice & Skin Care",
        "address": "9 Bishan Place #05-01 Junction 8, Singapore 579837",
        "phone": "+65 6358 4133",
        "website": "https://www.onecare.sg",
        "rating": 3.9,
        "lat": 1.3506,
        "lng": 103.8487,
        "specialties": ["Family Medicine", "Minor Procedures", "Health Screening"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 10:00 PM",
            "tuesday": "8:00 AM - 10:00 PM",
            "wednesday": "8:00 AM - 10:00 PM",
            "thursday": "8:00 AM - 10:00 PM",
            "friday": "8:00 AM - 10:00 PM",
            "saturday": "8:00 AM - 10:00 PM",
            "sunday": "8:00 AM - 10:00 PM"
        }
    },
    {
        "id": "northeast_medical",
        "name": "Northeast Medical Group",
        "department": "Multi-Specialty Clinic",
        "address": "598 Punggol Waterway #01-04, Singapore 820598",
        "phone": "+65 6312 8081",
        "website": "https://www.northeastmedical.com.sg",
        "rating": 4.0,SINGAPORE_MEDICAL_FACILITIES = [
    # Public Hospitals and Medical Centers
    {
        "id": "skh",
        "name": "Sengkang General Hospital",
        "department": "Dermatology Department",
        "address": "110 Sengkang East Way, Singapore 544886",
        "phone": "+65 6930 6000",
        "website": "https://www.skh.com.sg",
        "rating": 4.2,
        "lat": 1.3946,
        "lng": 103.8939,
        "specialties": ["General Dermatology", "Skin Allergies", "Pediatric Dermatology"],
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
        "id": "kkh",
        "name": "KK Women's and Children's Hospital",
        "department": "Dermatology Service",
        "address": "100 Bukit Timah Road, Singapore 229899",
        "phone": "+65 6225 5554",
        "website": "https://www.kkh.com.sg",
        "rating": 4.3,
        "lat": 1.3108,
        "lng": 103.8464,
        "specialties": ["Pediatric Dermatology", "Neonatal Skin Conditions", "Genetic Skin Disorders"],
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
        "id": "alexandra",
        "name": "Alexandra Hospital",
        "department": "Specialist Outpatient Clinic - Dermatology",
        "address": "378 Alexandra Road, Singapore 159964",
        "phone": "+65 6472 2000",
        "website": "https://www.ah.com.sg",
        "rating": 4.1,
        "lat": 1.2866,
        "lng": 103.8013,
        "specialties": ["General Dermatology", "Geriatric Skin Care", "Chronic Skin Conditions"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:30 AM - 5:00 PM",
            "tuesday": "8:30 AM - 5:00 PM",
            "wednesday": "8:30 AM - 5:00 PM",
            "thursday": "8:30 AM - 5:00 PM",
            "friday": "8:30 AM - 5:00 PM",
            "saturday": "8:30 AM - 12:00 PM",
            "sunday": "Closed"
        }
    },
    
    # Private Hospitals and Medical Centers
    {
        "id": "mount_alvernia",
        "name": "Mount Alvernia Hospital",
        "department": "Medical Centre A - Dermatology",
        "address": "820 Thomson Road, Singapore 574623",
        "phone": "+65 6347 6688",
        "website": "https://www.mtalvernia.sg",
        "rating": 4.3,
        "lat": 1.3419,
        "lng": 103.8378,
        "specialties": ["Skin Surgery", "Cosmetic Dermatology", "Skin Cancer Screening"],
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
        "id": "farrer_park",
        "name": "Farrer Park Hospital",
        "department": "Dermatology & Aesthetic Centre",
        "address": "1 Farrer Park Station Road, Singapore 217562",
        "phone": "+65 6363 1818",
        "website": "https://www.farrerpark.com",
        "rating": 4.4,
        "lat": 1.3124,
        "lng": 103.8542,
        "specialties": ["Aesthetic Dermatology", "Laser Surgery", "Anti-Aging Treatments"],
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
    
    # Specialist Clinics - Central Region
    {
        "id": "tsk_skin",
        "name": "TSK Skin Specialist Clinic",
        "department": "Dermatology",
        "address": "1 Orchard Boulevard #03-02, Singapore 248649",
        "phone": "+65 6235 5312",
        "website": "https://www.tskskin.com",
        "rating": 4.3,
        "lat": 1.3041,
        "lng": 103.8316,
        "specialties": ["Acne Treatment", "Pigmentation", "Skin Rejuvenation"],
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
        "id": "dermatology_associates",
        "name": "Dermatology Associates",
        "department": "Specialist Dermatology",
        "address": "3 Mount Elizabeth #14-11, Singapore 228510",
        "phone": "+65 6737 8006",
        "website": "https://www.dermatologyassociates.sg",
        "rating": 4.5,
        "lat": 1.3048,
        "lng": 103.8341,
        "specialties": ["Medical Dermatology", "Surgical Dermatology", "Cosmetic Procedures"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 5:30 PM",
            "tuesday": "9:00 AM - 5:30 PM",
            "wednesday": "9:00 AM - 5:30 PM",
            "thursday": "9:00 AM - 5:30 PM",
            "friday": "9:00 AM - 5:30 PM",
            "saturday": "9:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "david_liew",
        "name": "David Liew Dermatology",
        "department": "Dermatology & Laser Centre",
        "address": "6 Napier Road #10-06 Gleneagles, Singapore 258499",
        "phone": "+65 6474 3118",
        "website": "https://www.davidliewdermatology.com",
        "rating": 4.4,
        "lat": 1.3078,
        "lng": 103.8201,
        "specialties": ["Skin Cancer", "Mohs Surgery", "General Dermatology"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 5:00 PM",
            "tuesday": "9:00 AM - 5:00 PM",
            "wednesday": "9:00 AM - 5:00 PM",
            "thursday": "9:00 AM - 5:00 PM",
            "friday": "9:00 AM - 5:00 PM",
            "saturday": "9:00 AM - 12:00 PM",
            "sunday": "Closed"
        }
    },
    
    # Polyclinics with Dermatology Services
    {
        "id": "bedok_poly",
        "name": "Bedok Polyclinic",
        "department": "Family Medicine with Dermatology Service",
        "address": "11 Bedok North Street 1, Singapore 469662",
        "phone": "+65 6343 1121",
        "website": "https://www.singhealth.com.sg/polyclinics",
        "rating": 3.8,
        "lat": 1.3266,
        "lng": 103.9311,
        "specialties": ["Basic Dermatology", "Eczema", "Common Skin Conditions"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 4:30 PM",
            "tuesday": "8:00 AM - 4:30 PM",
            "wednesday": "8:00 AM - 4:30 PM",
            "thursday": "8:00 AM - 4:30 PM",
            "friday": "8:00 AM - 4:30 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "tampines_poly",
        "name": "Tampines Polyclinic",
        "department": "Family Medicine with Dermatology Referral",
        "address": "1 Tampines Street 41, Singapore 529203",
        "phone": "+65 6788 0833",
        "website": "https://www.singhealth.com.sg/polyclinics",
        "rating": 3.9,
        "lat": 1.3578,
        "lng": 103.9452,
        "specialties": ["Primary Dermatology Care", "Skin Infections", "Allergies"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "8:00 AM - 4:30 PM",
            "tuesday": "8:00 AM - 4:30 PM",
            "wednesday": "8:00 AM - 4:30 PM",
            "thursday": "8:00 AM - 4:30 PM",
            "friday": "8:00 AM - 4:30 PM",
            "saturday": "8:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    
    # East Region Clinics
    {
        "id": "clifford_dispensary",
        "name": "Clifford Dispensary Pte Ltd",
        "department": "Dermatology Clinic",
        "address": "24 Raffles Place #01-27, Singapore 048621",
        "phone": "+65 6532 2489",
        "website": "https://www.clifforddispensary.com",
        "rating": 4.0,
        "lat": 1.2844,
        "lng": 103.8520,
        "specialties": ["Occupational Dermatology", "STD Screening", "General Skin Care"],
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
        "id": "skin_physicians",
        "name": "The Skin Physicians",
        "department": "Dermatology & Aesthetic Medicine",
        "address": "50 East Coast Road #01-01, Singapore 428769",
        "phone": "+65 6348 4688",
        "website": "https://www.theskinphysicians.com",
        "rating": 4.2,
        "lat": 1.3051,
        "lng": 103.9042,
        "specialties": ["Acne Scar Treatment", "Melasma", "Hair Loss"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:30 AM - 6:30 PM",
            "tuesday": "9:30 AM - 6:30 PM",
            "wednesday": "9:30 AM - 6:30 PM",
            "thursday": "9:30 AM - 6:30 PM",
            "friday": "9:30 AM - 6:30 PM",
            "saturday": "9:30 AM - 1:00 PM",
            "sunday": "Closed"
        }
    },
    
    # West Region Clinics
    {
        "id": "jurong_medical",
        "name": "Jurong Medical Centre",
        "department": "Skin & Aesthetic Clinic",
        "address": "2 Venture Drive #01-02, Singapore 608526",
        "phone": "+65 6265 7981",
        "website": "https://www.jurongmedical.com",
        "rating": 4.1,
        "lat": 1.3320,
        "lng": 103.7471,
        "specialties": ["General Dermatology", "Wart Removal", "Skin Tags"],
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
        "id": "clementi_derma",
        "name": "Clementi Dermatology Clinic",
        "department": "Specialist Dermatology",
        "address": "442 Clementi Avenue 3 #01-95, Singapore 120442",
        "phone": "+65 6774 1121",
        "website": "https://www.clementiderma.com",
        "rating": 4.0,
        "lat": 1.3144,
        "lng": 103.7651,
        "specialties": ["Psoriasis", "Vitiligo", "Autoimmune Skin Conditions"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 5:00 PM",
            "tuesday": "9:00 AM - 5:00 PM",
            "wednesday": "9:00 AM - 5:00 PM",
            "thursday": "9:00 AM - 5:00 PM",
            "friday": "9:00 AM - 5:00 PM",
            "saturday": "9:00 AM - 12:00 PM",
            "sunday": "Closed"
        }
    },
    
    # North Region Clinics
    {
        "id": "woodlands_health",
        "name": "Woodlands Health Campus",
        "department": "Integrated Dermatology Services",
        "address": "2 Yishun Central 2, Singapore 768024",
        "phone": "+65 6363 6363",
        "website": "https://www.wh.com.sg",
        "rating": 4.1,
        "lat": 1.4304,
        "lng": 103.8363,
        "specialties": ["Community Dermatology", "Preventive Skin Care", "Chronic Disease Management"],
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
        "id": "yishun_specialist",
        "name": "Yishun Specialist Clinic",
        "department": "Dermatology Unit",
        "address": "101 Yishun Avenue 5 #01-35, Singapore 760101",
        "phone": "+65 6758 3636",
        "website": "https://www.yishunspecialist.com",
        "rating": 3.9,
        "lat": 1.4290,
        "lng": 103.8350,
        "specialties": ["Family Dermatology", "Pediatric Skin", "Elderly Care"],
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
    
    # Additional Specialist Clinics
    {
        "id": "apex_derma",
        "name": "Apex Dermatology & Skin Surgery Centre",
        "department": "Dermatological Surgery",
        "address": "6 Shenton Way #15-08 OUE Downtown, Singapore 068809",
        "phone": "+65 6222 2238",
        "website": "https://www.apexderma.com",
        "rating": 4.4,
        "lat": 1.2783,
        "lng": 103.8492,
        "specialties": ["Mohs Surgery", "Skin Cancer", "Reconstructive Surgery"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 5:30 PM",
            "tuesday": "9:00 AM - 5:30 PM",
            "wednesday": "9:00 AM - 5:30 PM",
            "thursday": "9:00 AM - 5:30 PM",
            "friday": "9:00 AM - 5:30 PM",
            "saturday": "9:00 AM - 12:30 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "skin_met",
        "name": "SkinMet Medical & Aesthetic Clinic",
        "department": "Medical Aesthetics",
        "address": "111 Somerset Road #04-36, Singapore 238164",
        "phone": "+65 6836 0123",
        "website": "https://www.skinmet.com.sg",
        "rating": 4.3,
        "lat": 1.3007,
        "lng": 103.8368,
        "specialties": ["Chemical Peels", "Laser Therapy", "Injectables"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "10:00 AM - 7:00 PM",
            "tuesday": "10:00 AM - 7:00 PM",
            "wednesday": "10:00 AM - 7:00 PM",
            "thursday": "10:00 AM - 7:00 PM",
            "friday": "10:00 AM - 7:00 PM",
            "saturday": "10:00 AM - 5:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "dermlove",
        "name": "DermLove Skin Clinic",
        "department": "Dermatology & Aesthetics",
        "address": "391B Orchard Road #08-04 Ngee Ann City, Singapore 238874",
        "phone": "+65 6734 1089",
        "website": "https://www.dermlove.com.sg",
        "rating": 4.2,
        "lat": 1.3025,
        "lng": 103.8347,
        "specialties": ["K-Beauty Treatments", "Hydrafacial", "Skin Brightening"],
        "insurance_accepted": False,
        "opening_hours": {
            "monday": "10:00 AM - 7:00 PM",
            "tuesday": "10:00 AM - 7:00 PM",
            "wednesday": "10:00 AM - 7:00 PM",
            "thursday": "10:00 AM - 7:00 PM",
            "friday": "10:00 AM - 7:00 PM",
            "saturday": "10:00 AM - 6:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "sozo_aesthetic",
        "name": "SOZO Aesthetic Clinic",
        "department": "Aesthetic Medicine",
        "address": "1 Raffles Place #05-19 One Raffles Place, Singapore 048616",
        "phone": "+65 6935 7920",
        "website": "https://www.sozoclinic.sg",
        "rating": 4.5,
        "lat": 1.2844,
        "lng": 103.8510,
        "specialties": ["Non-Surgical Facelifts", "Body Contouring", "Thread Lifts"],
        "insurance_accepted": False,
        "opening_hours": {
            "monday": "10:00 AM - 7:00 PM",
            "tuesday": "10:00 AM - 7:00 PM",
            "wednesday": "10:00 AM - 7:00 PM",
            "thursday": "10:00 AM - 7:00 PM",
            "friday": "10:00 AM - 7:00 PM",
            "saturday": "10:00 AM - 4:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "cambridge_medical",
        "name": "Cambridge Medical Group",
        "department": "Aesthetic & Laser Centre",
        "address": "391A Orchard Road #15-02/03 Tower A, Singapore 238873",
        "phone": "+65 6733 0777",
        "website": "https://www.cambridgemedical.com.sg",
        "rating": 4.4,
        "lat": 1.3025,
        "lng": 103.8347,
        "specialties": ["Aesthetic Medicine", "Laser Treatments", "Body Sculpting"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:00 AM - 6:00 PM",
            "tuesday": "9:00 AM - 6:00 PM",
            "wednesday": "9:00 AM - 6:00 PM",
            "thursday": "9:00 AM - 6:00 PM",
            "friday": "9:00 AM - 6:00 PM",
            "saturday": "9:00 AM - 4:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "oasis_medical",
        "name": "Oasis Medical & Aesthetics Clinic",
        "department": "Medical Aesthetics",
        "address": "Camden Medical Centre #13-05, Singapore 248649",
        "phone": "+65 6235 5566",
        "website": "https://www.oasismedical.sg",
        "rating": 4.2,
        "lat": 1.3041,
        "lng": 103.8316,
        "specialties": ["Botox", "Fillers", "Skin Tightening"],
        "insurance_accepted": False,
        "opening_hours": {
            "monday": "10:00 AM - 6:00 PM",
            "tuesday": "10:00 AM - 6:00 PM",
            "wednesday": "10:00 AM - 6:00 PM",
            "thursday": "10:00 AM - 6:00 PM",
            "friday": "10:00 AM - 6:00 PM",
            "saturday": "10:00 AM - 4:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "astute_medical",
        "name": "Astute Medical & Aesthetic Clinic",
        "department": "Dermatology & Aesthetics",
        "address": "350 Orchard Road #11-08 Shaw House, Singapore 238868",
        "phone": "+65 6732 3801",
        "website": "https://www.astutemedical.com",
        "rating": 4.3,
        "lat": 1.3056,
        "lng": 103.8316,
        "specialties": ["Medical Aesthetics", "Skin Analysis", "Customized Treatments"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "9:30 AM - 6:30 PM",
            "tuesday": "9:30 AM - 6:30 PM",
            "wednesday": "9:30 AM - 6:30 PM",
            "thursday": "9:30 AM - 6:30 PM",
            "friday": "9:30 AM - 6:30 PM",
            "saturday": "9:30 AM - 2:00 PM",
            "sunday": "Closed"
        }
    },
    {
        "id": "radium_medical",
        "name": "Radium Medical Aesthetics",
        "department": "Aesthetic Medicine",
        "address": "3 Temasek Boulevard #03-06 Suntec City, Singapore 038983",
        "phone": "+65 6837 0507",
        "website": "https://www.radiumaesthetics.com",
        "rating": 4.1,
        "lat": 1.2955,
        "lng": 103.8599,
        "specialties": ["Radiofrequency Treatments", "IPL", "Skin Resurfacing"],
        "insurance_accepted": False,
        "opening_hours": {
            "monday": "11:00 AM - 8:00 PM",
            "tuesday": "11:00 AM - 8:00 PM",
            "wednesday": "11:00 AM - 8:00 PM",
            "thursday": "11:00 AM - 8:00 PM",
            "friday": "11:00 AM - 8:00 PM",
            "saturday": "10:00 AM - 7:00 PM",
            "sunday": "10:00 AM - 7:00 PM"
        }
    },
    {
        "id": "one_face",
        "name": "One Face Clinic",
        "department": "Plastic Surgery & Aesthetics",
        "address": "1 Orchard Boulevard #13-01, Singapore 248649",
        "phone": "+65 6222 2262",
        "website": "https://www.oneface.sg",
        "rating": 4.4,
        "lat": 1.3041,
        "lng": 103.8316,
        "specialties": ["Facial Contouring", "Rhinoplasty", "Aesthetic Dermatology"],
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
        "id": "lim_clinic",
        "name": "Dr Lim & Partners Aesthetics",
        "department": "Medical Aesthetics",
        "address": "140 Arab Street, Singapore 199827",
        "phone": "+65 6298 5173",
        "website": "https://www.drlimandpartners.com",
        "rating": 4.0,
        "lat": 1.3019,
        "lng": 103.8594,
        "specialties": ["STD Treatment", "Men's Health", "Aesthetic Medicine"],
        "insurance_accepted": True,
        "opening_hours": {
            "monday": "10:00 AM - 9:00 PM",
            "tuesday": "10:00 AM - 9:00 PM",
            "wednesday": "10:00 AM - 9:00 PM",
            "thursday": "10:00 AM - 9:00 PM",
            "friday": "10:00 AM - 9:00 PM",
            "saturday": "10:00 AM - 9:00 PM",
            "sunday": "10:00 AM - 9:00 PM"
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
