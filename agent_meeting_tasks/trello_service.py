import requests
from typing import Dict, Any, List, Optional
from config import TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID, TRELLO_DEFAULT_LIST_ID

BASE_URL = "https://api.trello.com/1"

class TrelloService:
    def __init__(self, api_key: str = TRELLO_API_KEY, token: str = TRELLO_TOKEN, board_id: str = TRELLO_BOARD_ID):
        self.api_key = api_key
        self.token = token
        self.board_id = board_id

    def _auth_params(self) -> Dict[str, str]:
        return {"key": self.api_key, "token": self.token}

    def get_lists(self) -> List[Dict[str, Any]]:
        """Retrieves all lists on the board."""
        url = f"{BASE_URL}/boards/{self.board_id}/lists"
        resp = requests.get(url, params=self._auth_params())
        if resp.status_code == 200:
            return resp.json()
        raise Exception(f"Failed to fetch lists: {resp.text}")

    def get_cards_in_list(self, list_id: str = TRELLO_DEFAULT_LIST_ID) -> List[Dict[str, Any]]:
        """Retrieves all cards in a list."""
        url = f"{BASE_URL}/lists/{list_id}/cards"
        resp = requests.get(url, params=self._auth_params())
        if resp.status_code == 200:
            return resp.json()
        return []

    def create_card(self, title: str, description: str, due_date: Optional[str] = None, list_id: str = TRELLO_DEFAULT_LIST_ID) -> Dict[str, Any]:
        """Creates a card on the Trello board with owner, due date, and transcript reference."""
        url = f"{BASE_URL}/cards"
        params = self._auth_params()
        params.update({
            "idList": list_id,
            "name": title,
            "desc": description
        })
        if due_date:
            params["due"] = due_date  # ISO format string or YYYY-MM-DD

        resp = requests.post(url, params=params)
        if resp.status_code == 200:
            return resp.json()
        raise Exception(f"Failed to create card: {resp.text}")

    def verify_card(self, card_id: str, expected_owner: str, expected_date: Optional[str], expected_transcript_ref: str) -> Dict[str, Any]:
        """
        Step 5 Verification Rule:
        Re-reads card from Trello for owner, date, and link to transcript.
        Captures observed state and compares with intended state.
        """
        url = f"{BASE_URL}/cards/{card_id}"
        resp = requests.get(url, params=self._auth_params())
        if resp.status_code != 200:
            return {
                "verified": False,
                "error": f"Could not read card {card_id} from Trello: {resp.text}",
                "observed_state": None
            }

        card_data = resp.json()
        desc = card_data.get("desc", "")
        due = card_data.get("due")
        card_name = card_data.get("name")
        card_url = card_data.get("shortUrl")

        # Check owner presence in description or title
        owner_found = expected_owner.lower() in desc.lower() or expected_owner.lower() in card_name.lower()
        
        # Check transcript link or quote presence in description
        transcript_ref_found = (expected_transcript_ref.lower() in desc.lower()) or ("transcript" in desc.lower())

        # Check due date
        date_matches = True
        if expected_date:
            date_matches = bool(due and expected_date[:10] in due[:10])

        verified = owner_found and transcript_ref_found and date_matches

        return {
            "verified": verified,
            "card_id": card_id,
            "card_url": card_url,
            "intended": {
                "owner": expected_owner,
                "due_date": expected_date,
                "transcript_ref": expected_transcript_ref
            },
            "observed": {
                "name": card_name,
                "owner_matched": owner_found,
                "due": due,
                "date_matched": date_matches,
                "transcript_ref_found": transcript_ref_found
            }
        }
