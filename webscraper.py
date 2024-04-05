"""Web scraper for Art Sci Course Calendar"""
from typing import Any, Union
import pandas as pd
from IPython.core.display import HTML
from IPython.display import display
import requests
import bs4
from dataclasses import dataclass, field


def name_finder(collection: dict[str, Any], html_value: bs4.PageElement) -> None:
    """
    Given an BeautifulSoup Element, appends the course name value to the collection.
    """
    value = html_value.find("h3", class_="js-views-accordion-group-header")
    if value is not None:
        text = value.find("div").text.strip()
        text = text.split()
        collection["Course Name"] = text[0]


def course_desc_finder(collection: dict[str, Any], html_value: bs4.PageElement) -> None:
    """
    Given an BeautifulSoup Element, appends the course description value to the collection.
    """
    value = html_value.find("div", class_="field-content")
    if value is not None:
        collection["Course Description"] = value.find("p").text.strip()


def hours_finder(collection: dict[str, Any], html_value: bs4.PageElement) -> None:
    """
    Given an BeautifulSoup Element, appends the hours value to the collection.
    """
    value = html_value.find("span", class_="views-field views-field-field-hours")
    if value is not None:
        collection["Hours"] = value.find("span", class_="field-content").text.strip()


def course_code_identifier(potential: str) -> bool:
    """checks whether a string is a valid course code"""
    if len(potential) != 8:
        return False
    start_code = potential[:3]
    if not str.isalpha(start_code) or not str.isupper(start_code):
        return False
    number_code = potential[3:6]
    if not str.isdigit(number_code):
        return False
    sem_loc_code = potential[6:]
    if sem_loc_code[0] not in "HY" or sem_loc_code[1] not in "01":
        return False
    return True


def prerequisite_finder(collection: dict[str, Any], html_value: bs4.PageElement) -> None:
    """
    Given an BeautifulSoup Element, appends a list of prereq codes to the collection.
    """
    value = html_value.find("span", class_="views-field views-field-field-prerequisite")
    if value is not None:
        clean_text = value.get_text()
        clean_text_remove_tag = clean_text.replace("Prerequisite: ", "")
        clean_text_min_grade_clean = (clean_text_remove_tag.replace("(minimum ", "{").replace("grade ", "")
                                      .replace("%)", "}")).replace(".", "")
        clean_text_separation = ((clean_text_min_grade_clean.replace("/", " / ").replace(",", " , ")
                                 .replace(";", " , ")).replace("(", " ( ").replace(")", " ) ")
                                 .replace("[", " ( ").replace("]", " ) ").split())
        clean_text_separation = [item for item in clean_text_separation if item in "()/,"
                                 or course_code_identifier(item)]

        collection["Prerequisites"] = " ".join(clean_text_separation)


def corequisite_finder(collection: dict[str, Any], html_value: bs4.PageElement) -> None:
    """
    Given an BeautifulSoup Element, appends a list of coreq codes to the collection.
    """
    value = html_value.find("span", class_="views-field views-field-field-corequisite")
    if value is not None:
        clean_text = value.get_text()
        clean_text_remove_tag = clean_text.replace("Corequisite: ", "")
        clean_text_min_grade_clean = (clean_text_remove_tag.replace("(minimum ", "{").replace("grade ", "")
                                      .replace("%)", "}")).replace(".", "")
        clean_text_separation = ((clean_text_min_grade_clean.replace("/", " / ").replace(",", " , ")
                                 .replace(";", " , ")).replace("(", " ( ").replace(")", " ) ")
                                 .replace("[", " ( ").replace("]", " ) ").split())
        clean_text_separation = [item for item in clean_text_separation if item in "()/,"
                                 or course_code_identifier(item)]
        collection["Corequisites"] = " ".join(clean_text_separation)


def exclusion_finder(collection: dict[str, Any], html_value: bs4.PageElement) -> None:
    """
    Given an BeautifulSoup Element, appends a list of exclusion codes to the collection.
    """
    value = html_value.find("span", class_="views-field views-field-field-exclusion")
    if value is not None:
        clean_text = value.get_text()
        clean_text_remove_tag = clean_text.replace("Exclusion: ", "")
        clean_text_min_grade_clean = (clean_text_remove_tag.replace("(minimum ", "{").replace("grade ", "")
                                      .replace("%)", "}")).replace(".", "")
        clean_text_separation = ((clean_text_min_grade_clean.replace("/", " / ").replace(",", " , ")
                                 .replace(";", " , ")).replace("(", " ( ").replace(")", " ) ")
                                 .replace("[", " ( ").replace("]", " ) ").split())
        clean_text_separation = [item for item in clean_text_separation if item in "()/,"
                                 or course_code_identifier(item)]
        collection["Exclusion"] = " ".join(clean_text_separation)


def distribution_finder(collection: dict[str, Any], html_value: bs4.PageElement) -> None:
    """
    Given an BeautifulSoup Element, appends distribution type to the collection.
    """
    value = html_value.find("span", class_="views-field views-field-field-distribution-requirements")
    if value is not None:
        clean_text = value.get_text()
        clean_text_remove_tag = (clean_text.replace(" ", "").replace("Distribution", "")
                                 .replace("Requirements", "").replace(":", "")).replace(".", "")
        collection["Distribution Requirements"] = clean_text_remove_tag


def breadth_finder(collection: dict[str, Any], html_value: bs4.PageElement) -> None:
    """
    Given an BeautifulSoup Element, appends breadth requirement type to the collection.
    """
    value = html_value.find("span", class_="views-field views-field-field-breadth-requirements")
    if value is not None:
        clean_text = value.get_text().replace("(", "").replace(")", "").replace(".", "").split()[-1]
        collection["Breadth Requirements"] = clean_text


base_URL = "https://artsci.calendar.utoronto.ca/search-courses?page="


def course_collector(element: bs4.PageElement, collector: dict[str, str]) -> Union[dict[str, Any], None]:
    """given a page element, returns all contained elements within the course"""
    name_finder(collector, element)
    if not collector:
        return None
    course_desc_finder(collector, element)
    hours_finder(collector, element)
    prerequisite_finder(collector, element)
    corequisite_finder(collector, element)
    exclusion_finder(collector, element)
    distribution_finder(collector, element)
    breadth_finder(collector, element)
    names.append(collector)
    return collector


if __name__ == "__main__":
    dataframe = pd.DataFrame(columns=["Course Name", "Course Description", "Hours", "Prerequisites", "Corequisites",
                     "Distribution Requirements", "Breadth Requirements", "Exclusion"])

    for i in range(0, 170):
        URL = base_URL + str(i)
        page = requests.get(URL)
        soup = bs4.BeautifulSoup(page.content, "html.parser")
        class_elements = soup.find_all("div", class_="views-row")
        names = []
        for element in class_elements:
            collector = {"Course Name": "",
                         "Course Description": "",
                         "Hours": "",
                         "Prerequisites": "",
                         "Corequisites": "",
                         "Distribution Requirements": "",
                         "Breadth Requirements": "",
                         "Exclusion": ""}
            course_collector(element, collector)
            if collector["Course Name"] == "" or not course_code_identifier(collector["Course Name"]):
                continue
            dataframe.loc[len(dataframe.index)] = [collector["Course Name"],
                                                   collector["Course Description"],
                                                   collector["Hours"],
                                                   collector["Prerequisites"],
                                                   collector["Corequisites"],
                                                   collector["Distribution Requirements"],
                                                   collector["Breadth Requirements"],
                                                   collector["Exclusion"]]
    dataframe.to_excel('output.xlsx', index=False)

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pandas', 'graph_course'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4
    })
