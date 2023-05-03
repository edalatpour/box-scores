# function to get reservations from ClubLocker
import requests
def get_reservations(club_locker_id):
    reservations = []
    try:
        response = requests.get(
            f"{CLUB_LOCKER_API_URL}/reservations?club_locker_id={club_locker_id}"
        )
        if response.status_code == 200:
            reservations = response.json()
    except Exception as e:
        print(e)
    return reservations

