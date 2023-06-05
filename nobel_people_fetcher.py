import requests
import logging
import sys

logging.basicConfig(level=logging.INFO)


class NobelApiFetcher:
    """
    Class to fetch and display information about Nobel Prize laureates.

    This class sends a GET request to the Nobel Prize API, fetches data about the laureates,
    and includes functionality to search for laureates by the year they won the prize.

    Attributes:
        _category (str): The category of the Nobel Prize (default is "phy" for Physics).
        _api_version (str): The version of the Nobel Prize API (default is "2.1").
        _laureates_api_url (str): The URL of the Nobel Prize API for fetching laureate's data.
        _api_params (str): The parameters to be included in the API request.
        _all_laureates_data (list[dict]): List of all laureates data fetched from the API.
    """

    def __init__(self, category: str = "phy", api_version: str = "2.1", year_from: int = 2000, year_to: int = 2023):
        self._category: str = category
        self._api_version: str = api_version
        self._laureates_api_url: str = f"https://api.nobelprize.org/{self._api_version}/laureates"
        self._api_params: str =\
            f"limit=5000&nobelPrizeYear={year_from}&yearTo={year_to}&format=json&nobelPrizeCategory={self._category}"
        self._all_laureates_data: list[dict] = []

    def find_specific_year_laureates_info(self, award_year: int) -> None:
        """
        Searches the dataset downloaded from the Nobel Prize API in order to find information about people who won
        the Nobel Prize in a given year. If no laureates are found for the given year, a log message will be generated.

        :param award_year: The year from which we want to obtain data on the winners.
        :type award_year: int
        :return: None
        """
        self._all_laureates_data = self._get_laureates_data()

        laureate_found = False

        if self._all_laureates_data:
            for laureate_data in self._all_laureates_data:
                if int(laureate_data['nobelPrizes'][0]['awardYear']) == award_year:
                    self._print_single_laureate_info(laureate_data)
                    laureate_found = True
            if not laureate_found:
                logging.info(f"No laureates were found in {award_year}!")
        else:
            logging.error("Laureates data not found!")

    def _get_laureates_data(self) -> list[dict]:
        """
        Sends a GET request to the specified API endpoint to fetch data on Nobel Laureates from Nobel Prize API.
        This method combines the APIs base URL and parameters to form complete API request URL. It then sends a GET
        request to this URL and checks the response status code.

        If any error occurs during the request or the parsing of the response (e.g. network issues or invalid response
        format), an exception will be raised and caught, with an error message.

        :return: Laureates data fetched from the API.
        :rtype: list[dict]
        """
        url_with_params = f"{self._laureates_api_url}?{self._api_params}"
        laureates_data = []

        try:
            response = requests.get(url_with_params, timeout=8)
            response.raise_for_status()
            data = response.json()

            if "laureates" in data:
                laureates_data = data["laureates"]
            else:
                logging.warning("No 'laureates' in response data")

        except requests.exceptions.Timeout:
            logging.error("Request timed out")
            sys.exit(1)

        except requests.exceptions.TooManyRedirects:
            logging.error("Too many redirects")
            sys.exit(1)

        except requests.exceptions.RequestException as e:
            logging.error("A request error occurred:", e)
            sys.exit(1)

        except Exception as e:
            logging.error("An unexpected error occurred:", e)
            sys.exit(1)

        return laureates_data

    @staticmethod
    def _print_single_laureate_info(laureate_data: dict) -> None:
        """
        Extracts specific data from the laureate's data downloaded from the API. Displays data about a specific laureate
        such as full name, year of winning the Nobel Prize and related institutions with the laureate.

        :param laureate_data: Details of specific Nobel laureate.
        :type laureate_data: dict
        :return: None
        """

        try:
            full_name = laureate_data['knownName']['en']
            if 'nobelPrizes' in laureate_data:
                award_year = laureate_data['nobelPrizes'][0]['awardYear']
                affiliations = laureate_data['nobelPrizes'][0]['affiliations'][0]['name']['en']
            else:
                raise KeyError("'nobelPrizes' not found in laureate data")
        except KeyError as e:
            logging.error(f"Failed to print laureate info: {e}")
        else:
            print("---------------------------------")
            print(f"Full name: {full_name}")
            print(f"Award year: {award_year}")
            print(f"Affiliations: {affiliations}")
            print()


def get_year_from_user() -> int:
    """
    Prompts the user to enter a year and validates the input.
    The function keeps asking for input until a valid year between 2000 and 2023 is entered.

    :return: The valid year entered by the user.
    :rtype: int
    """
    while True:
        try:
            year = int(input("Enter the year from which to search for Nobel Prize winners: "))

            if 2000 <= year <= 2023:
                return year
            else:
                print("Entered number is not a year between 2000 and 2023!")
                print("Try again.\n")

        except ValueError:
            print("Entered value is not a number! Try again.\n")


if __name__ == "__main__":
    year = get_year_from_user()
    nobel_fetcher = NobelApiFetcher()
    nobel_fetcher.find_specific_year_laureates_info(year)
